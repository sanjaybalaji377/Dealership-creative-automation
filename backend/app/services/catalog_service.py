import os
from typing import Dict, List
from ..config import ASSET_DIR

PANELS_ROOT = os.path.join(ASSET_DIR, "Dealership-panels")

ACCOUNT_FOLDER_MAP = {
    "Tata-dealers": "Tata",
    "VW-dealers": "Volkswagen",
    "Kia-dealers": "Kia",
}

def _public_asset_path(abs_path: str) -> str:
    rel = os.path.relpath(abs_path, ASSET_DIR).replace(os.sep, "/")
    return f"/api/assets/{rel}"

def scan_catalog() -> List[Dict]:
    accounts = []
    if not os.path.isdir(PANELS_ROOT):
        return accounts

    for account_folder in sorted(os.listdir(PANELS_ROOT)):
        account_path = os.path.join(PANELS_ROOT, account_folder)
        if not os.path.isdir(account_path):
            continue
        account_name = ACCOUNT_FOLDER_MAP.get(account_folder, account_folder.replace("-dealers", "").replace("-", " ").title())
        dealerships = []
        for dealer_folder in sorted(os.listdir(account_path)):
            dealer_path = os.path.join(account_path, dealer_folder)
            if not os.path.isdir(dealer_path):
                continue
            files = {name: os.path.join(dealer_path, name) for name in os.listdir(dealer_path)}
            template = files.get("template.png") or files.get("template1.png")
            logo_light = files.get("logo-light.png")
            logo_dark = files.get("logo-dark.png")
            dealerships.append({
                "id": f"{account_folder}/{dealer_folder}",
                "name": dealer_folder.replace("-", " ").title(),
                "folder": dealer_folder,
                "template_path": template,
                "template1_path": files.get("template1.png"),
                "logo_light_path": logo_light,
                "logo_dark_path": logo_dark,
                "template_url": _public_asset_path(template) if template else None,
                "logo_light_url": _public_asset_path(logo_light) if logo_light else None,
                "logo_dark_url": _public_asset_path(logo_dark) if logo_dark else None,
            })
        accounts.append({
            "id": account_folder,
            "name": account_name,
            "dealerships": dealerships,
        })
    return accounts

def get_dealer(dealer_id: str):
    for account in scan_catalog():
        for dealer in account["dealerships"]:
            if dealer["id"] == dealer_id:
                return dealer
    return None
