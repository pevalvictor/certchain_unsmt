import os
import uuid
import hashlib
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
    jsonify, send_from_directory, send_file
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app import db, mail
from app.models import Certificado, Curso, Participante
from app.utils.decorators import roles_required
from app.utils.certificados_qr import generar_qr_pdf
from app.utils.pdf_utils import incrustar_qr_y_firmar

from itsdangerous import URLSafeTimedSerializer
serializer = URLSafeTimedSerializer("clave-secreta")


bp = Blueprint('certs', __name__)
UPLOAD_FOLDER = 'app/static/uploads'
serializer = URLSafeTimedSerializer("clave-secreta")

@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('certs.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    total_emitidos = Certificado.query.filter_by(emisor_id=current_user.id).count() if current_user.rol in ['admin', 'emisor'] else None
    return render_template('dashboard.html', total_emitidos=total_emitidos)

@bp.route('/emitir-certificado', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'emisor')
def emitir_certificado():
    if request.method == 'POST':
        participante_id = request.form.get('participante_id')
        curso_id = request.form.get('curso_id')
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        horas = request.form.get('horas')
        archivo = request.files.get('archivo')

        if not all([participante_id, curso_id, nombre, correo, horas, archivo]):
            flash('Faltan campos obligatorios.', 'danger')
            return redirect(url_for('certs.emitir_certificado'))

        curso = Curso.query.get_or_404(curso_id)
        evento = curso.nombre

        nombre_base = secure_filename(archivo.filename)
        ruta_subida = os.path.join(UPLOAD_FOLDER, nombre_base)
        archivo.save(ruta_subida)

        # TOKEN y enlace público
        token = serializer.dumps(participante_id, salt='cert-descarga')
        enlace_verificacion = url_for('public.verificar_qr', token=token, _external=True)

        # Generar PDF final con QR incrustado + HASH real
        nombre_final, hash_cert, ruta_final = incrustar_qr_y_firmar(ruta_subida, enlace_verificacion)

        # Guardar en la BD
        nuevo_cert = Certificado(
            nombre_participante=nombre,
            nombre_evento=evento,
            duracion_horas=horas,
            archivo_nombre=nombre_final,
            archivo_hash=hash_cert,
            participante_id=participante_id,
            curso_id=curso_id,
            emisor_id=current_user.id,
            token_descarga=token,
            correo_destino=correo
        )
        db.session.add(nuevo_cert)
        db.session.commit()

        try:
            with open(ruta_final, 'rb') as f:
                adjunto = f.read()

            msg = Message("🎓 Tu certificado UNSM-T", recipients=[correo])
            msg.html = render_template("email/correo_certificado.html", nombre=nombre, evento=evento, enlace=enlace_verificacion)
            msg.attach(nombre_final, "application/pdf", adjunto)
            mail.send(msg)
            flash('✅ Certificado emitido y enviado correctamente.', 'success')
        except Exception as e:
            flash(f'Certificado generado pero falló el envío de correo: {e}', 'warning')

        # Aquí se puede calcular el total si lo usas en el dashboard
        total_emitidos = Certificado.query.count()
        return render_template('dashboard.html', total_emitidos=total_emitidos)

    return render_template('certs/emitir.html')


#-------------------------------------------------------------------------
@bp.route('/descargar-certificado/<token>')
def descargar_certificado(token):
    try:
        participante_id = serializer.loads(token, salt='cert-descarga', max_age=604800)

        cert = Certificado.query.filter_by(participante_id=participante_id, token_descarga=token).first()

        if not cert:
            flash("El certificado no existe.", "danger")
            return redirect(url_for('certs.verificacion_publica'))

        ruta_pdf = os.path.join(UPLOAD_FOLDER, cert.archivo_nombre)

        if not os.path.exists(ruta_pdf):
            flash("Archivo no encontrado.", "danger")
            return redirect(url_for('certs.verificacion_publica'))

        if not cert.descargado:
            cert.descargado = True
            cert.fecha_descarga = datetime.utcnow()
            cert.ip_descarga = request.remote_addr
            db.session.commit()

        return send_file(ruta_pdf, as_attachment=True)

    except Exception as e:
        flash("Enlace inválido o vencido.", "danger")
        return redirect(url_for('certs.verificacion_publica'))

    
    

@bp.route('/verificacion_publica', methods=['GET', 'POST'])
def verificacion_publica():
    mensaje = None
    resultado = None
    certificados = []
    dni = request.args.get('dni')

    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if archivo and archivo.filename.endswith('.pdf'):
            contenido = archivo.read()
            hash_archivo = hashlib.sha256(contenido).hexdigest()
            resultado = Certificado.query.filter_by(archivo_hash=hash_archivo).first()
            mensaje = "✅ Certificado válido" if resultado else "❌ Certificado no válido o alterado"

    if dni:
        certificados = Certificado.query.join(Participante).filter(Participante.dni == dni).all()
        if not certificados:
            mensaje = f"No se encontraron certificados con el DNI {dni}"

    return render_template('verificacion_publica.html', resultado=resultado, mensaje=mensaje, certificados=certificados)

@bp.route('/qr/<token>')
def verificacion_qr(token):
    try:
        cert_id = serializer.loads(token, salt='cert-descarga')
        cert = Certificado.query.get_or_404(cert_id)
        return render_template('qr_verificado.html', certificado=cert)
    except:
       # flash("Token inválido o vencido", "danger")
        return redirect(url_for('certs.verificacion_publica'))

@bp.route('/historial')
@login_required
def historial_certificados():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    nombre = request.args.get('nombre', '', type=str)
    evento = request.args.get('evento', '', type=str)
    fecha_inicio = request.args.get('fecha_inicio', '', type=str)
    fecha_fin = request.args.get('fecha_fin', '', type=str)

    query = Certificado.query.filter_by(emisor_id=current_user.id)

    if nombre:
        query = query.filter(Certificado.nombre_participante.ilike(f"%{nombre}%"))
    if evento:
        query = query.filter(Certificado.nombre_evento.ilike(f"%{evento}%"))
    if fecha_inicio:
        try:
            f_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            query = query.filter(Certificado.fecha_emision >= f_ini)
        except ValueError:
            flash("Fecha de inicio inválida", "warning")
    if fecha_fin:
        try:
            f_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            query = query.filter(Certificado.fecha_emision <= f_fin)
        except ValueError:
            flash("Fecha de fin inválida", "warning")

    certificados = query.order_by(Certificado.fecha_emision.desc()).paginate(page=page, per_page=per_page)

    return render_template(
        'certs/historial.html',
        certificados=certificados.items,
        paginacion=certificados,
        nombre=nombre,
        evento=evento,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        per_page=per_page
    )



@bp.route('/verificar', methods=['GET', 'POST'])
@login_required
def verificar_certificado():
    mensaje = None
    resultado = None

    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if archivo and archivo.filename.endswith('.pdf'):
            contenido = archivo.read()
            hash_archivo = hashlib.sha256(contenido).hexdigest()
            resultado = Certificado.query.filter_by(archivo_hash=hash_archivo).first()
            mensaje = "✅ Certificado válido" if resultado else "❌ Certificado no válido o alterado"

    #return render_template('participantes/verify.html', resultado=resultado, mensaje=mensaje)
    return render_template('certs/verificar.html', resultado=resultado, mensaje=mensaje)


