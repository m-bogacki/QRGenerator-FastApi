from fastapi import FastAPI
import qrcode
from qrcode.image.pure import PyPNGImage
from base64 import b64encode
from io import BytesIO
import barcode
from barcode.writer import ImageWriter

app = FastAPI()


def buffer_to_base64(img):
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    return b64encode(buffer.read()).decode("utf-8")


def generate_qr_code(input_text):
    img = qrcode.make(input_text, image_factory=PyPNGImage)
    return buffer_to_base64(img)


def generate_barcode(input_text):
    """
    Generates a Code128 barcode from the given input_text.

    :param input_text: The string to be encoded as a barcode.
    :return: A base64 encoded PNG image of the barcode.
    """
    code128 = barcode.get_barcode_class("code128")
    img = code128(input_text, writer=ImageWriter())
    return buffer_to_base64(img)


@app.post("/qr/generate/{format}")
async def generate_qr(input_text: str, format: str):
    if format == "qr":
        return generate_qr_code(input_text)
    elif format == "barcode":
        return generate_barcode(input_text)
    return "Invalid format"
