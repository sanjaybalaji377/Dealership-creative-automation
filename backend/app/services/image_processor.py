import os
import uuid
import zipfile
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps
from .catalog_service import get_dealer
from ..config import GENERATED_DIR, OUTPUT_SIZES

def cover_resize(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """Smart scaling with centering offset."""
    image = ImageOps.exif_transpose(image).convert("RGB")
    # Using high-quality LANCZOS for premium results and slight offset up
    return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))

def contain_resize(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    image = image.convert("RGBA")
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return image

def paste_rgba(base: Image.Image, overlay: Image.Image, xy: Tuple[int, int]) -> None:
    base.paste(overlay, xy, overlay if overlay.mode == "RGBA" else None)

def generate_for_dealer(background_path: str, dealer_id: str, output_key: str, include_logo: bool, logo_type: str, job_dir: str) -> Dict:
    """Generation logic with format-aware positioning."""
    if output_key not in OUTPUT_SIZES:
        raise ValueError("Invalid output size")

    dealer = get_dealer(dealer_id)
    if not dealer:
        raise ValueError(f"Dealer not found: {dealer_id}")

    canvas_size = OUTPUT_SIZES[output_key]
    bg = Image.open(background_path)
    canvas = cover_resize(bg, canvas_size).convert("RGBA")
    width, height = canvas_size

    # Adjust panel size/pos based on height
    is_story = height > width
    
    panel_path = dealer.get("template_path") or dealer.get("template1_path")
    if panel_path and os.path.exists(panel_path):
        panel = Image.open(panel_path).convert("RGBA")
        
        # Scaling logic: Panels look better slightly wider on stories
        scale_factor = 0.95 if is_story else 0.92
        panel_max_width = int(width * scale_factor)
        panel_max_height = int(height * (0.35 if is_story else 0.28))
        
        panel = contain_resize(panel, panel_max_width, panel_max_height)
        panel_x = (width - panel.width) // 2
        
        # Auto-Positioning: Lift slightly higher for stories to avoid overlay UI elements
        y_offset = 0.08 if is_story else 0.035
        panel_y = height - panel.height - int(height * y_offset)
        
        paste_rgba(canvas, panel, (panel_x, panel_y))

    if include_logo:
        logo_path = dealer.get("logo_light_path") if logo_type == "light" else dealer.get("logo_dark_path")
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo_max_width = int(width * 0.22)
            logo_max_height = int(height * 0.10)
            logo = contain_resize(logo, logo_max_width, logo_max_height)
            
            # Auto-alignment of logo: Top left with safe margin
            margin = int(width * 0.045)
            paste_rgba(canvas, logo, (margin, margin))

    safe_dealer = dealer["folder"].replace("/", "_").replace(" ", "_")
    filename = f"{safe_dealer}_{output_key}.png"
    out_path = os.path.join(job_dir, filename)
    
    # Save with high-quality PNG settings
    canvas.convert("RGB").save(out_path, "PNG", optimize=True)
    return {"dealer_id": dealer_id, "dealer_name": dealer["name"], "output_key": output_key, "filename": filename}

def generate_bulk(background_path: str, dealer_ids: List[str], output_keys: List[str], include_logo: bool, logo_type: str = "light") -> Dict:
    job_id = str(uuid.uuid4())[:8]
    job_dir = os.path.join(GENERATED_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    task_args = []
    for dealer_id in dealer_ids:
        for output_key in output_keys:
            task_args.append((background_path, dealer_id, output_key, include_logo, logo_type, job_dir))

    # Parallel processing for high-performance batch generation
    with ThreadPoolExecutor(max_workers=4) as executor:
        files = list(executor.map(lambda p: generate_for_dealer(*p), task_args))

    zip_name = f"creatives_{job_id}.zip"
    zip_path = os.path.join(job_dir, zip_name)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for item in files:
            file_path = os.path.join(job_dir, item["filename"])
            zipf.write(file_path, arcname=item["filename"])

    return {
        "job_id": job_id,
        "count": len(files),
        "files": [{**f, "url": f"/generated/{job_id}/{f['filename']}"} for f in files],
        "zip_url": f"/api/download/{job_id}",
    }
