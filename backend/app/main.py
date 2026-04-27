import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .config import UPLOAD_DIR, GENERATED_DIR
from .routes.account_routes import account_bp
from .routes.creative_routes import creative_bp
from .routes.auth_routes import auth_bp
from .services.db_service import init_db

app = Flask(__name__)
CORS(app)
init_db()

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(account_bp, url_prefix="/api")
app.register_blueprint(creative_bp, url_prefix="/api")

@app.route("/")
def index():
    return {
        "message": "Dealership Creative Automation API is running",
        "endpoints": {
            "health": "/api/health",
            "accounts": "/api/accounts",
            "upload_background": "/api/upload/background (POST)",
            "generate_creatives": "/api/generate-creatives (POST)"
        }
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/generated/<path:filename>")
def generated_file(filename):
    return send_from_directory(GENERATED_DIR, filename, as_attachment=False)

@app.get("/api/assets/<path:filename>")
def asset_file(filename):
    return send_from_directory(os.path.join(STATIC_DIR, "assets"), filename, as_attachment=False)

@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)
