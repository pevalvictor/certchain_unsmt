from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        user = Usuario.query.filter_by(correo=correo).first()
        if user and user.check_password(contrasena):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('certs.dashboard'))
        flash('Correo o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))

