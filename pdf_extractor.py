import io
from PyPDF2 import PdfReader, PdfWriter
def extract_pages(files):
    keywords = ['COLOR COMBO','COLOR COMBO DETAILS']
    out_writer = PdfWriter()
    for f in files:
        data = f.read()
        reader = PdfReader(io.BytesIO(data))
        for i in range(len(reader.pages)):
            try:
                text = reader.pages[i].extract_text() or ''
            except:
                text = ''
            if any(k in text.upper() for k in keywords):
                out_writer.add_page(reader.pages[i])
    out_io = io.BytesIO()
    out_writer.write(out_io)
    out_io.seek(0)
    return out_io.read()
