try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'


def ocr_core(filename):

    text = pytesseract.image_to_string(Image.open(filename))
    print(os.path.getsize('/static/uploads/' + filename.filename))
    print(filename.filename)
    return text
