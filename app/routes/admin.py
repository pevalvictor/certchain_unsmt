import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from app.models import db, Usuario, Curso, Participante, Certificado
from app.utils.decorators import roles_required

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from app.models import db, Usuario, Curso, Participante, Certificado
from app.utils.decorators import roles_required
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/fotos_participantes'


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# --------------------------- Gestión de Usuarios ---------------------------
@admin_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def gestionar_usuarios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        rol = request.form['rol']
        contrasena = generate_password_hash(request.form['contrasena'])

        nuevo_usuario = Usuario(
            nombre_completo=nombre,
            correo=correo,
            contrasena_hash=contrasena,
            rol=rol
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('admin.gestionar_usuarios'))

    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/eliminar-usuario/<int:id>')
@login_required
@roles_required('admin')
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('admin.gestionar_usuarios'))

@admin_bp.route('/desactivar-usuario/<int:id>')
@login_required
@roles_required('admin')
def desactivar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.activo = False
    db.session.commit()
    flash('Usuario desactivado.', 'warning')
    return redirect(url_for('admin.gestionar_usuarios'))

@admin_bp.route('/activar-usuario/<int:id>')
@login_required
@roles_required('admin')
def activar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.activo = True
    db.session.commit()
    flash('Usuario activado.', 'success')
    return redirect(url_for('admin.gestionar_usuarios'))

# --------------------------- Gestión de Cursos ---------------------------
@admin_bp.route('/cursos', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def gestionar_cursos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
        duracion_horas = int(request.form['duracion_horas'])
        responsable_firma = request.form['responsable_firma']
        cargo_responsable = request.form['cargo_responsable']

        curso = Curso(
            nombre=nombre,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            duracion_horas=duracion_horas,
            responsable_firma=responsable_firma,
            cargo_responsable=cargo_responsable
        )
        db.session.add(curso)
        db.session.commit()
        flash('Curso registrado correctamente.', 'success')
        return redirect(url_for('admin.gestionar_cursos'))

    cursos = Curso.query.order_by(Curso.fecha_inicio.desc()).all()
    return render_template('admin/cursos.html', cursos=cursos)

@admin_bp.route('/cursos/editar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def editar_curso(id):
    curso = Curso.query.get_or_404(id)
    curso.nombre = request.form['nombre']
    curso.tipo = request.form['tipo']
    curso.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
    curso.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
    curso.duracion_horas = int(request.form['duracion_horas'])
    curso.responsable_firma = request.form['responsable_firma']
    curso.cargo_responsable = request.form['cargo_responsable']
    curso.estado = request.form.get('estado', 'activo')
    db.session.commit()
    flash('Curso actualizado correctamente.', 'success')
    return redirect(url_for('admin.gestionar_cursos'))

@admin_bp.route('/cursos/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado correctamente.', 'info')
    return redirect(url_for('admin.gestionar_cursos'))

@admin_bp.route('/cursos/toggle-estado/<int:id>')
@login_required
@roles_required('admin')
def toggle_estado_curso(id):
    curso = Curso.query.get_or_404(id)
    curso.estado = 'inactivo' if curso.estado == 'activo' else 'activo'
    db.session.commit()
    flash(f"Curso {'desactivado' if curso.estado == 'inactivo' else 'activado'}.", 'info')
    return redirect(url_for('admin.gestionar_cursos'))

@admin_bp.route('/cursos/obtener/<int:id>')
@login_required
@roles_required('admin')
def obtener_curso(id):
    curso = Curso.query.get_or_404(id)
    return jsonify({
        'id': curso.id,
        'nombre': curso.nombre,
        'tipo': curso.tipo,
        'fecha_inicio': curso.fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': curso.fecha_fin.strftime('%Y-%m-%d'),
        'duracion_horas': curso.duracion_horas,
        'responsable_firma': curso.responsable_firma,
        'cargo_responsable': curso.cargo_responsable
    })

# --------------------------- Gestión de Participantes ---------------------------
@admin_bp.route('/participantes')
@login_required
@roles_required('admin')
def gestionar_participantes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    nombre = request.args.get('nombre', '', type=str)
    dni = request.args.get('dni', '', type=str)

    # ✅ AQUÍ ESTABA EL ERROR: esta línea debe estar presente
    query = Participante.query

    if nombre:
        query = query.filter(Participante.nombre_completo.ilike(f"%{nombre}%"))
    if dni:
        query = query.filter(Participante.dni.ilike(f"%{dni}%"))

    paginacion = query.order_by(Participante.fecha_registro.desc()).paginate(page=page, per_page=per_page)
    participantes = paginacion.items
    cursos = Curso.query.all()

    return render_template(
        'admin/participantes.html',
        participantes=participantes,
        paginacion=paginacion,
        nombre=nombre,
        dni=dni,
        per_page=per_page,
        cursos=cursos
    )


#----------registro de participantes---------------

@admin_bp.route('/participantes/registrar', methods=['POST'])
@login_required
@roles_required('admin')
def registrar_participante():
    nombre = request.form['nombre_completo']
    dni = request.form['dni']
    correo = request.form['correo']
    celular = request.form.get('celular')
    curso_id = request.form['curso_id']
    foto = request.files.get('foto')

    curso = Curso.query.get_or_404(curso_id)

    nombre_foto = None
    if foto and foto.filename != '':
        nombre_foto = secure_filename(f"{dni}_{foto.filename}")
        ruta = os.path.join(UPLOAD_FOLDER, nombre_foto)
        foto.save(ruta)

    participante = Participante(
        nombre_completo=nombre,
        dni=dni,
        correo=correo,
        celular=celular,
        foto_nombre=nombre_foto
    )
    participante.cursos.append(curso)
    db.session.add(participante)
    db.session.commit()

    flash('Participante registrado correctamente y vinculado al curso.', 'success')
    return redirect(url_for('admin.gestionar_participantes'))




#----------------------EDICION------------------

@admin_bp.route('/participantes/editar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def editar_participante(id):
    participante = Participante.query.get_or_404(id)
    participante.nombre_completo = request.form['nombre_completo']
    participante.dni = request.form['dni']
    participante.correo = request.form['correo']
    participante.celular = request.form.get('celular')
    
    # Reemplazar curso anterior (si corresponde)
    nuevo_curso_id = request.form.get('curso_id')
    if nuevo_curso_id:
        nuevo_curso = Curso.query.get(nuevo_curso_id)
        participante.cursos = [nuevo_curso]

    # Actualizar foto si se proporciona una nueva
    if 'foto' in request.files:
        nueva_foto = request.files['foto']
        if nueva_foto and nueva_foto.filename != '':
            nombre_foto = secure_filename(f"{participante.dni}_{nueva_foto.filename}")
            ruta = os.path.join(UPLOAD_FOLDER, nombre_foto)
            nueva_foto.save(ruta)
            participante.foto_nombre = nombre_foto

    db.session.commit()
    flash('Participante actualizado correctamente.', 'success')
    return redirect(url_for('admin.gestionar_participantes'))


#--------------ELIMINAR PARTICIPANETES DEL REGISTRO--------------
@admin_bp.route('/participantes/eliminar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def eliminar_participante(id):
    participante = Participante.query.get_or_404(id)
    db.session.delete(participante)
    db.session.commit()
    flash('Participante eliminado correctamente.', 'info')
    return redirect(url_for('admin.gestionar_participantes'))

# --------------------------- Auditoría ---------------------------
@admin_bp.route('/auditoria')
@login_required
@roles_required('admin')
def auditoria_certificados():
    certificados = Certificado.query.order_by(Certificado.fecha_emision.desc()).all()
    cursos = Curso.query.order_by(Curso.nombre.asc()).all()
    return render_template('admin/auditoria.html', certificados=certificados, cursos=cursos)

@admin_bp.route('/auditoria/detalle/<int:id>')
@login_required
@roles_required('admin')
def detalle_certificado(id):
    cert = Certificado.query.get_or_404(id)
    return jsonify({
        'nombre_participante': cert.nombre_participante,
        'nombre_evento': cert.nombre_evento,
        'duracion_horas': cert.duracion_horas,
        'fecha_emision': cert.fecha_emision.strftime('%d/%m/%Y'),
        'archivo_hash': cert.archivo_hash,
        'emisor': cert.emisor.nombre_completo,
        'archivo_url': url_for('static', filename='uploads/' + cert.archivo_nombre)
    })

@admin_bp.route('/auditoria/filtro', methods=['POST'])
@login_required
@roles_required('admin')
def filtrar_auditoria():
    curso_id = request.form.get('curso_id')
    if not curso_id:
        return jsonify({'error': 'ID de curso no proporcionado'}), 400

    certificados = Certificado.query.filter_by(nombre_evento=Curso.query.get(curso_id).nombre).all()

    datos = [{
        'participante': cert.nombre_participante,
        'evento': cert.nombre_evento,
        'horas': cert.duracion_horas,
        'fecha_emision': cert.fecha_emision.strftime('%d/%m/%Y'),
        'archivo': cert.archivo_nombre,
        'emisor': cert.emisor.nombre_completo if cert.emisor else 'N/A'
    } for cert in certificados]

    return jsonify({'certificados': datos})

# --------------------------- Buscar Participante por DNI ---------------------------
@admin_bp.route('/certificados/buscar_participante', methods=['GET'])
@login_required
@roles_required('admin')
def buscar_participante():
    dni = request.args.get('dni')
    participante = Participante.query.filter_by(dni=dni).first()

    if not participante:
        return jsonify({'error': 'Participante no encontrado'}), 404

    cursos = [
        {'id': c.id, 'nombre': c.nombre, 'duracion': c.duracion_horas}
        for c in participante.cursos
    ]

    return jsonify({
        'id': participante.id,
        'nombre': participante.nombre_completo,
        'correo': participante.correo,
        'cursos': cursos
    })

@admin_bp.route('/participantes/obtener/<int:id>')
@login_required
@roles_required('admin')
def obtener_participante(id):
    p = Participante.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'nombre_completo': p.nombre_completo,
        'dni': p.dni,
        'correo': p.correo,
        'celular': p.celular,
        'curso_id': p.cursos[0].id if p.cursos else ''
    })