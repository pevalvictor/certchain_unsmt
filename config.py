import os

class Config:
    # Seguridad
    SECRET_KEY = os.environ.get("SECRET_KEY", "devsecretkey")

    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:73461697@localhost/certchaindb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo (Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "pevalvictor.19@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "wxhw jfii ttrr japu")
    MAIL_DEFAULT_SENDER = ("CertChain UNSM-T", MAIL_USERNAME)
