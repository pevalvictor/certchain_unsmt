import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Participante, Curso
from app.utils.decorators import roles_required

bp = Blueprint('participantes', __name__)
UPLOAD_FOLDER = 'app/static/fotos_participantes'

# ---------------------- REGISTRO DE PARTICIPANTE ----------------------
@bp.route('/participantes/registrar', methods=['GET', 'POST'])
@login_required
def registrar_participante():
    cursos = Curso.query.all()

    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        dni = request.form['dni']
        correo = request.form['correo']
        celular = request.form['celular']
        curso_id = request.form['curso_id']
        foto = request.files.get('foto')

        nombre_archivo = None
        if foto and foto.filename:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            nombre_archivo = secure_filename(f"{dni}_{foto.filename}")
            ruta_foto = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            foto.save(ruta_foto)

        participante = Participante(
            nombre_completo=nombre_completo,
            dni=dni,
            correo=correo,
            celular=celular,
            foto_nombre=nombre_archivo
        )

        if curso_id:
            curso = Curso.query.get(int(curso_id))
            if curso:
                participante.cursos.append(curso)

        db.session.add(participante)
        db.session.commit()

        flash('Participante registrado exitosamente.', 'success')
        return redirect(url_for('admin.gestionar_participantes'))

    return render_template('participantes/registrar.html', cursos=cursos)

# ---------------------- GESTIÓN DE PARTICIPANTES ----------------------
@bp.route('/admin/participantes')
@login_required
@roles_required('admin')
def gestionar_participantes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    nombre = request.args.get('nombre', '', type=str)
    dni = request.args.get('dni', '', type=str)

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

# ---------------------- OBTENER PARTICIPANTE (AJAX) ----------------------
@bp.route('/participantes/obtener/<int:id>')
@login_required
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

# ---------------------- EDITAR PARTICIPANTE ----------------------
@bp.route('/participantes/editar/<int:id>', methods=['POST'])
@login_required
def editar_participante(id):
    participante = Participante.query.get_or_404(id)

    participante.nombre_completo = request.form['nombre_completo']
    participante.dni = request.form['dni']
    participante.correo = request.form['correo']
    participante.celular = request.form['celular']

    curso_id = request.form['curso_id']
    participante.cursos = []
    if curso_id:
        curso = Curso.query.get(int(curso_id))
        if curso:
            participante.cursos.append(curso)

    foto = request.files.get('foto')
    if foto and foto.filename:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        nombre_archivo = secure_filename(f"{participante.dni}_{foto.filename}")
        ruta_foto = os.path.join(UPLOAD_FOLDER, nombre_archivo)
        foto.save(ruta_foto)
        participante.foto_nombre = nombre_archivo

    db.session.commit()
    flash('Participante actualizado correctamente.', 'success')
    return redirect(url_for('admin.gestionar_participantes'))
