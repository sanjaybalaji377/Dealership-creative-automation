import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
ASSET_DIR = os.path.join(STATIC_DIR, "assets")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
GENERATED_DIR = os.path.join(STATIC_DIR, "generated")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
OUTPUT_SIZES = {
    "instagram_square": (1080, 1080),
    "instagram_portrait": (1080, 1350),
    "instagram_story": (1080, 1920),
}
