from app import db
from flask_login import UserMixin
from datetime import datetime
import hashlib

# Tabla intermedia: Participantes ⇄ Cursos (N:M)
participantes_cursos = db.Table(
    'participantes_cursos',
    db.Column('participante_id', db.Integer, db.ForeignKey('participantes.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True)
)

# -------------------------- CERTIFICADO --------------------------
class Certificado(db.Model):
    __tablename__ = 'certificados'

    id = db.Column(db.Integer, primary_key=True)
    nombre_participante = db.Column(db.String(100), nullable=False)
    nombre_evento = db.Column(db.String(150), nullable=False)
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    duracion_horas = db.Column(db.Integer)
    archivo_nombre = db.Column(db.String(200))
    archivo_hash = db.Column(db.String(64), unique=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    participante_id = db.Column(db.Integer, db.ForeignKey('participantes.id'))
    token_descarga = db.Column(db.String(120), unique=True)
    expira_en = db.Column(db.DateTime)
    descargado = db.Column(db.Boolean, default=False)
    correo_destino = db.Column(db.String(120), nullable=True)
    fecha_descarga = db.Column(db.DateTime)
    ip_descarga = db.Column(db.String(45))

    def generar_hash(self, contenido_binario):
        self.archivo_hash = hashlib.sha256(contenido_binario).hexdigest()

# -------------------------- CURSO --------------------------
class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    duracion_horas = db.Column(db.Integer, nullable=False)
    responsable_firma = db.Column(db.String(100), nullable=False)
    cargo_responsable = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(20), default='activo')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    participantes = db.relationship('Participante', secondary=participantes_cursos, back_populates='cursos')
    certificados = db.relationship('Certificado', backref='curso', lazy=True)

# -------------------------- PARTICIPANTE --------------------------
class Participante(db.Model):
    __tablename__ = 'participantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(12), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    celular = db.Column(db.String(20), nullable=True)
    foto_nombre = db.Column(db.String(200), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    cursos = db.relationship('Curso', secondary=participantes_cursos, back_populates='participantes')
    certificados = db.relationship('Certificado', backref='participante', lazy=True)

# -------------------------- USUARIO --------------------------
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(512), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.contrasena_hash, password)

# -------------------------- EMISOR --------------------------
class Emisor(db.Model):
    __tablename__ = 'emisores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(128))


