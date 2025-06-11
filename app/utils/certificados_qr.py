import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

def generar_qr_pdf(pdf_path, token, output_path):
    dominio = "http://127.0.0.1:5000"  # Cambia por tu dominio real en producción
    url_qr = f"{dominio}/qr/{token}"

    # Generar QR con la URL completa
    qr = qrcode.make(url_qr)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    # Convertir la imagen del QR a formato que acepte ReportLab
    qr_image = ImageReader(qr_buffer)

    # Crear nuevo PDF y colocar el QR
    c = canvas.Canvas(output_path, pagesize=letter)

    qr_width = 1.5 * inch
    qr_height = 1.5 * inch
    margin_x = 0.5 * inch
    margin_y = 0.5 * inch

    # Insertar QR en el PDF
    c.drawImage(qr_image, x=margin_x, y=margin_y, width=qr_width, height=qr_height, mask='auto')

    # Aquí podrías agregar más contenido al PDF si es necesario

    c.save()
