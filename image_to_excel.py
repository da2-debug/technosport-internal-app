import io, pandas as pd, pytesseract, PIL.Image as Image
def process_images_to_excel(files):
    rows = []
    for f in files:
        image = Image.open(f)
        text = pytesseract.image_to_string(image)
        rows.append({'file': getattr(f,'name','image'), 'text': text.replace('\n',' | ')})
    df = pd.DataFrame(rows)
    out = io.BytesIO()
    df.to_excel(out, index=False, sheet_name='ImageText')
    out.seek(0)
    return out.read()
