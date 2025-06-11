from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.utils.decorators import roles_required
from app.models import db, Usuario
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/emisores', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def gestionar_emisores():
    if request.method == 'POST':
        emisor_id = request.form.get('id')
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form.get('contrasena')

        if emisor_id:
            emisor = Usuario.query.get(emisor_id)
            if emisor:
                emisor.nombre_completo = nombre
                emisor.correo = correo
                if contrasena:
                    emisor.set_password(contrasena)
                flash('Emisor actualizado correctamente.', 'success')
        else:
            nuevo = Usuario(
                nombre_completo=nombre,
                correo=correo,
                rol='emisor'
            )
            nuevo.set_password(contrasena)
            db.session.add(nuevo)
            flash('Emisor registrado correctamente.', 'success')

        db.session.commit()
        return redirect(url_for('admin.gestionar_emisores'))

    emisores = Usuario.query.filter_by(rol='emisor').all()
    return render_template('admin/emisores.html', emisores=emisores)


@admin_bp.route('/eliminar-emisor/<int:id>')
@login_required
@roles_required('admin')
def eliminar_emisor(id):
    emisor = Usuario.query.get_or_404(id)
    if emisor.rol == 'emisor':
        db.session.delete(emisor)
        db.session.commit()
        flash('Emisor eliminado correctamente.', 'success')
    else:
        flash('No se puede eliminar este usuario.', 'danger')
    return redirect(url_for('admin.gestionar_emisores'))
