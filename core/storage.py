"""core/storage.py — Cloudinary image storage (replaces local assets/images/items)."""
import re
import uuid
import cloudinary
import cloudinary.uploader

# Reads CLOUDINARY_URL from the environment automatically.
cloudinary.config(secure=True)

FOLDER = "lknstock/items"


def _public_id(item_code: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", item_code or "").strip("_")
    return safe or uuid.uuid4().hex[:10]


def upload_item_image(file_or_path, item_code: str):
    """Upload an image; returns (secure_url, public_id)."""
    res = cloudinary.uploader.upload(
        file_or_path,
        folder=FOLDER,
        public_id=_public_id(item_code),
        overwrite=True,
        invalidate=True,
        resource_type="image",
        transformation=[{"width": 900, "height": 900, "crop": "limit",
                         "quality": "auto", "fetch_format": "auto"}],
    )
    return res["secure_url"], res["public_id"]


def delete_image(public_id: str):
    if not public_id:
        return
    try:
        cloudinary.uploader.destroy(public_id, invalidate=True)
    except Exception:
        pass


def thumb(url: str, size=80) -> str:
    """Insert a Cloudinary resize transform into a delivery URL."""
    if url and "/upload/" in url:
        return url.replace("/upload/", f"/upload/c_fill,w_{size},h_{size},q_auto,f_auto/", 1)
    return url or ""
