from datetime import datetime, timezone
from typing import TYPE_CHECKING, cast
from fastapi import UploadFile
from qrcode.main import QRCode
import requests
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from io import BytesIO

from strawberry.file_uploads import Upload


from veecert_backend.constants.urls import Urls

if TYPE_CHECKING:
    from veecert_backend.apps.assets.models import IPFSAsset

QRCODE_LOGO_WIDTH = 40


async def generate_nft_image(
    id: int, name: str, unit_name: str, url: str
) -> "IPFSAsset":
    from veecert_backend.apps.assets.models import IPFSAsset

    font_url = "https://github.com/google/fonts/blob/main/apache/roboto/Roboto-Bold.ttf?raw=true"
    font_path = "Roboto-Bold.ttf"

    # Download the font file if it does not exist
    if not os.path.exists(font_path):
        response = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(response.content)

    # Colors and image size
    background_color = (230, 202, 255)
    image_width = 1200
    image_height = 800

    # Font sizes
    large_font_size = 80
    medium_font_size = 40
    small_font_size = 30

    # Create a blank image with the specified background color
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        large_font = ImageFont.truetype(font_path, large_font_size)
        medium_font = ImageFont.truetype(font_path, medium_font_size)
        small_font = ImageFont.truetype(font_path, small_font_size)
    except IOError:
        large_font = medium_font = small_font = None

    # Texts and positions
    texts = [
        (name, (50, 50), large_font),
        (unit_name, (50, 200), medium_font),
        (f"#{id}", (50, 270), medium_font),
        (datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"), (1000, 50), small_font),
    ]

    # Draw texts
    for text, position, font in texts:
        draw.text(position, text, fill="black", font=font)

    res = requests.get(Urls.VEE_CERT_LOGO)
    logo = Image.open(BytesIO(res.content))
    w_percent = QRCODE_LOGO_WIDTH / logo.size[0]
    logo_height = int(logo.size[1] * w_percent)
    logo = logo.resize((QRCODE_LOGO_WIDTH, logo_height), Image.Resampling.LANCZOS)

    # Generate the QR code
    qr = QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Resize QR code and paste it on the image
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    pos = (
        (qr_img.size[0] - logo.size[0]) // 2,
        (qr_img.size[1] - logo.size[1]) // 2,
    )
    qr_img.paste(logo, pos)
    qr_position = (800, 400)
    image.paste(qr_img, qr_position)

    bytes_io = BytesIO()
    # Save the image
    image.save(bytes_io, "png")
    bytes_io.seek(0)
    asset = await IPFSAsset.manager.new(cast(Upload, UploadFile(file=bytes_io)))
    return asset
