<div align="center">

# 🎓 CertChain UNSM
### Sistema web de gestión y verificación de certificados digitales

**Python · Flask · PostgreSQL · SQLAlchemy · HTML · CSS · JavaScript**

![Estado](https://img.shields.io/badge/estado-prototipo%20en%20desarrollo-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Base%20de%20datos-336791)

</div>

## 📌 Descripción

**CertChain UNSM** es un proyecto de desarrollo de software orientado a apoyar la **gestión de certificados digitales** mediante una aplicación web. Su propuesta contempla el registro y administración de información, la emisión de certificados y mecanismos de consulta o verificación mediante códigos QR.

El proyecto se desarrolló como una iniciativa académica vinculada a Ingeniería de Sistemas e Informática. **No es un sistema institucional oficial de la UNSM.**

> **Estado actual:** prototipo en desarrollo. Se ha probado localmente la conexión a PostgreSQL, el inicio de sesión y parte de la interfaz. Los demás módulos aún requieren completar su implementación y pruebas.

## 🎯 Objetivo

Diseñar e implementar una solución web que permita centralizar la gestión de certificados y facilite su verificación, buscando reducir procesos manuales y mejorar la trazabilidad de la información.

## 🧩 Funcionalidades y alcance

| Componente | Estado |
|---|---|
| Conexión con base de datos PostgreSQL | ✅ Probada localmente |
| Autenticación e inicio de sesión | ✅ Probado localmente |
| Interfaz y navegación inicial | 🟡 Implementación parcial |
| Gestión administrativa de certificados | 🚧 En desarrollo |
| Generación y procesamiento de certificados | 🚧 Pendiente de validación integral |
| Verificación mediante código QR | 🚧 Pendiente de validación integral |
| Notificaciones por correo | 🚧 Pendiente de configuración y pruebas |

*Los estados reflejan el avance del prototipo, no una certificación de funcionamiento en producción.*

## 🛠️ Tecnologías

- **Backend:** Python, Flask
- **Base de datos:** PostgreSQL
- **Persistencia y migraciones:** SQLAlchemy, Flask-Migrate
- **Autenticación:** Flask-Login
- **Frontend:** HTML, CSS, JavaScript
- **Funciones complementarias:** herramientas para documentos PDF, códigos QR y correo electrónico

## 🏗️ Organización del código

```text
certchain_unsmt/
├── app/                 # Aplicación web, vistas, modelos y recursos
├── migrations/          # Migraciones de base de datos
├── config.py            # Configuración
├── crear_usuario.py     # Utilidad de creación de usuarios
├── requirements.txt     # Dependencias de Python
└── run.py               # Punto de entrada de Flask
```

## 💻 Ejecución local

**Requisitos:** Python, PostgreSQL y un entorno virtual recomendado.

1. Abrir el proyecto en Visual Studio Code.
2. Crear y activar el entorno virtual.
3. Instalar las dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Crear una base de datos PostgreSQL para el entorno de pruebas.
5. Configurar de manera privada las variables de conexión y la clave de la aplicación, de acuerdo con la versión del proyecto. **Nunca publicar contraseñas ni archivos con secretos.**
6. Aplicar las migraciones disponibles:

```powershell
$env:FLASK_APP = "run.py"
flask db upgrade
```

7. Ejecutar:

```powershell
python run.py
```

8. Abrir la dirección local mostrada por Flask (habitualmente `http://127.0.0.1:5000`).

> **Nota:** esta versión del repositorio es un prototipo académico y puede requerir ajustes de configuración y dependencias antes de instalarse desde cero. No está preparada para despliegue público.

## 📸 Capturas

Las capturas del inicio de sesión, panel principal y módulos operativos podrán incorporarse en `docs/screenshots/` una vez revisadas para evitar exponer datos personales. No se incluyen imágenes simuladas de funcionalidades pendientes.

## 🗺️ Próximos pasos

- Completar la lógica de los módulos de certificados.
- Validar de extremo a extremo la generación y verificación de códigos QR.
- Mejorar validaciones, permisos y manejo de errores.
- Incorporar pruebas funcionales y documentación técnica.
- Preparar una configuración reproducible y segura para instalación.

## 🔐 Seguridad y privacidad

Este proyecto está destinado a aprendizaje y desarrollo. Antes de utilizarlo con datos reales o exponerlo a Internet, es necesario revisar las credenciales, permisos, almacenamiento de documentos, configuraciones sensibles y dependencias. No deben incorporarse al repositorio archivos `.env`, claves privadas, certificados reales ni información personal.

## 👨‍💻 Autor

**Víctor Pérez Valqui**  
Ingeniería de Sistemas e Informática  
[GitHub: @pevalvictor](https://github.com/pevalvictor)

---

<div align="center"><sub>Proyecto académico · Prototipo en desarrollo</sub></div>
