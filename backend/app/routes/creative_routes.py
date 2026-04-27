import os
import uuid
from flask import Blueprint, request, send_file
from werkzeug.utils import secure_filename
from ..config import UPLOAD_DIR, GENERATED_DIR, ALLOWED_IMAGE_EXTENSIONS
from ..services.image_processor import generate_bulk

creative_bp = Blueprint("creative_routes", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@creative_bp.post("/upload/background")
def upload_background():
    if "background" not in request.files:
        return {"error": "background file is required"}, 400
    file = request.files["background"]
    if not file.filename or not allowed_file(file.filename):
        return {"error": "Only JPG/PNG background images are allowed"}, 400
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    path = os.path.join(UPLOAD_DIR, filename)
    file.save(path)
    return {"filename": filename, "path": path, "url": f"/uploads/{filename}"}

@creative_bp.post("/generate-creatives")
def generate_creatives():
    data = request.get_json(silent=True) or {}
    background_filename = data.get("background_filename")
    dealer_ids = data.get("dealer_ids") or []
    output_keys = data.get("output_keys") or ["instagram_square"]
    include_logo = bool(data.get("include_logo", True))
    logo_type = data.get("logo_type", "light")

    if not background_filename:
        return {"error": "background_filename is required"}, 400
    if not dealer_ids:
        return {"error": "At least one dealership must be selected"}, 400

    background_path = os.path.join(UPLOAD_DIR, background_filename)
    if not os.path.exists(background_path):
        # Support predefined assets
        background_path = os.path.join(ASSET_DIR, background_filename)
        if not os.path.exists(background_path):
            return {"error": "Uploaded background not found"}, 404

    try:
        result = generate_bulk(background_path, dealer_ids, output_keys, include_logo, logo_type)
        return result
    except Exception as exc:
        return {"error": str(exc)}, 500

@creative_bp.get("/download/<job_id>")
def download_zip(job_id):
    job_dir = os.path.join(GENERATED_DIR, job_id)
    zip_path = os.path.join(job_dir, f"creatives_{job_id}.zip")
    if not os.path.exists(zip_path):
        return {"error": "ZIP not found"}, 404
    return send_file(zip_path, as_attachment=True, download_name=f"creatives_{job_id}.zip")
