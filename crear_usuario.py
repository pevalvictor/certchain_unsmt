from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

# Inicializar app
app = create_app()
app.app_context().push()

# Crear nuevo usuario admin
nuevo_usuario = Usuario(
    nombre_completo="Admin Principal",
    correo="admin@unsm.edu.pe",
    contrasena_hash=generate_password_hash("admin123"),
    rol="admin"
)

# Insertar en la base de datos
db.session.add(nuevo_usuario)
db.session.commit()

print("✅ Usuario admin creado correctamente.")
