from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for
from app.models import Certificado
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import os

public = Blueprint('public', __name__)
UPLOAD_FOLDER = 'app/static/uploads'
serializer = URLSafeTimedSerializer("clave-secreta")  # Puedes reemplazar con app.config['SECRET_KEY'] si lo usas dinámico

@public.route('/qr/<token>')
def verificar_qr(token):
    try:
        cert_id = serializer.loads(token, salt='cert-descarga', max_age=60 * 60 * 24 * 30)  # 30 días
        certificado = Certificado.query.get(cert_id)

        if not certificado:
            flash("El certificado no existe o ha sido eliminado.", "danger")
            return render_template("qr_verificado.html", certificado=None)

        return render_template("qr_verificado.html", certificado=certificado)

    except SignatureExpired:
        flash("⚠️ Este enlace ha expirado.", "warning")
        return render_template("qr_verificado.html", certificado=None)

    except BadSignature:
        flash("❌ Enlace inválido o manipulado.", "danger")
        return render_template("qr_verificado.html", certificado=None)


@public.route('/descargar-certificado-publico/<int:id>')
def descargar_certificado_publico(id):
    certificado = Certificado.query.get_or_404(id)
    file_path = os.path.join(UPLOAD_FOLDER, certificado.archivo_nombre)

    if not os.path.exists(file_path):
        flash("El archivo no está disponible o fue movido.", "danger")
        return redirect(url_for('public.verificar_qr', token=certificado.token_descarga))

    return send_from_directory(UPLOAD_FOLDER, certificado.archivo_nombre, as_attachment=True)
