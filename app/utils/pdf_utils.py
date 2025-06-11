import fitz  # PyMuPDF
import qrcode
import hashlib
import uuid
import os

UPLOAD_FOLDER = "app/static/uploads"

def incrustar_qr_y_firmar(path_pdf_original, enlace_qr):
    doc = fitz.open(path_pdf_original)
    page = doc[0]

    # ✅ Generar QR
    qr = qrcode.make(enlace_qr)
    qr_path = "/tmp/temp_qr.png"
    qr.save(qr_path)

    # ✅ NUEVA posición (parte inferior izquierda del certificado)
    # Ajustado según orientación A4 horizontal (landscape)
    x0 = 40    # izquierda
    y0 = 480   # arriba
    x1 = x0 + 100
    y1 = y0 + 100
    rect = fitz.Rect(x0, y0, x1, y1)

    # ✅ Insertar imagen QR en la posición corregida
    page.insert_image(rect, filename=qr_path)

    # ✅ Guardar nuevo PDF firmado
    nombre_final = f"cert_{uuid.uuid4().hex}.pdf"
    ruta_final = os.path.join(UPLOAD_FOLDER, nombre_final)
    doc.save(ruta_final)
    doc.close()

    # ✅ Hash real del contenido
    with open(ruta_final, "rb") as f:
        contenido = f.read()
        hash_pdf = hashlib.sha256(contenido).hexdigest()

    return nombre_final, hash_pdf, ruta_final
