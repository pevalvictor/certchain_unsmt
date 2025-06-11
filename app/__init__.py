from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'auth.login'  # Redirección si no está logueado

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Importar y registrar blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.certs import bp as certs_bp
    from app.routes.cursos import bp as cursos_bp
    from app.routes.admin import admin_bp
    from app.routes.public import public as public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(certs_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    
   

    return app
