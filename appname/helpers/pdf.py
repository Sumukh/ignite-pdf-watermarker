import pikepdf
from io import BytesIO
from pikepdf import Pdf, Rectangle
from reportlab.pdfgen import canvas

def generate_watermark(msg, xy):
    x, y = xy
    buf = BytesIO()
    c = canvas.Canvas(buf, bottomup=0)
    c.setFontSize(32)
    c.setFillColorCMYK(0, 0, 0, 0, alpha=0.4)
    c.rect(204, 199, 157, 15, stroke=0, fill=1)
    c.setFillColorCMYK(0, 0, 0, 100, alpha=0.4)
    c.drawString(x, y, msg)
    c.save()
    buf.seek(0)
    return buf

def concatenate_pdf(files):
    pdf_file = Pdf.new()
    for single_file in files:
        src = Pdf.open(single_file)
        pdf_file.pages.extend(src.pages)
    return pdf_file

def password_pdf(file, password, extraction=True):
    permissions = pikepdf.Permissions(extract=extraction)

    pdf_file = pikepdf.open(file)
    pdf_file.save('encrypted.pdf', encryption=pikepdf.Encryption(
        user=password, owner=password, allow=permissions
    ))

def watermark_pdf(watermark_text, document_file):
    wm = generate_watermark(watermark_text, (100, 100))
    pdf_txt = pikepdf.open(document_file)

    with pikepdf.open(wm) as pdf_wm:
        for page in pdf_txt.pages:
            wm_page = pikepdf.Page(pdf_wm.pages[0])
            pdf_txt_page = pikepdf.Page(page)
            pdf_txt_page.add_overlay(wm_page, Rectangle(0, 0, 300, 300))

    return pdf_txt
