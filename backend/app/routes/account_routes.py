import os
from flask import Blueprint, send_from_directory
from ..services.catalog_service import scan_catalog
from ..config import ASSET_DIR

account_bp = Blueprint("account_routes", __name__)

@account_bp.get("/accounts")
def accounts():
    catalog = scan_catalog()
    return {"accounts": [{"id": a["id"], "name": a["name"], "dealer_count": len(a["dealerships"])} for a in catalog]}

@account_bp.get("/accounts/<account_id>/dealerships")
def dealerships(account_id):
    for account in scan_catalog():
        if account["id"] == account_id:
            return {"dealerships": account["dealerships"]}
    return {"error": "Account not found"}, 404

@account_bp.get("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(ASSET_DIR, filename)
