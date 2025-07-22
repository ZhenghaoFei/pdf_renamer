

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_pdf(path, title, content):
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, title)
    text = c.beginText(100, 730)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()

if __name__ == "__main__":
    create_dummy_pdf("/home/zfei/tmp/pdf_renamer/pdfs/dummy_pdf.pdf", "My Dummy PDF Title", "This is the content of the dummy PDF.")

