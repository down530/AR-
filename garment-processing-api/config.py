"""
Configuration and constants for the garment extraction API.
"""
import os
from pathlib import Path

# -------------------- Paths --------------------
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

# -------------------- File Upload --------------------
ALLOWED_EXTS = {"png", "jpg", "jpeg"}
MAX_CONTENT_MB = float(os.getenv("MAX_CONTENT_MB", "16"))
MAX_CONTENT_BYTES = int(MAX_CONTENT_MB * 1024 * 1024)

# -------------------- CORS --------------------
CORS_ALLOW_ORIGINS_RAW = os.getenv("CORS_ALLOW_ORIGINS", "*").strip()
if CORS_ALLOW_ORIGINS_RAW == "*":
    CORS_ALLOW_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = False
else:
    CORS_ALLOW_ORIGINS = [o.strip() for o in CORS_ALLOW_ORIGINS_RAW.split(",") if o.strip()]
    CORS_ALLOW_CREDENTIALS = True

# -------------------- Storage Mode --------------------
# Set USE_CLOUDINARY=false to use local file storage instead of Cloudinary
USE_CLOUDINARY = os.getenv("USE_CLOUDINARY", "true").lower() in ("1", "true", "yes")

# -------------------- Cloudinary --------------------
CLOUDINARY_CONFIG = {
    "cloud_name": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "api_key": os.environ.get("CLOUDINARY_API_KEY"),
    "api_secret": os.environ.get("CLOUDINARY_API_SECRET"),
    "secure": True,
}

CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "garments")
FOLDER_ORIG = f"{CLOUDINARY_FOLDER}/originals"
FOLDER_CUT = f"{CLOUDINARY_FOLDER}/cutouts"
FOLDER_TRYON = f"{CLOUDINARY_FOLDER}/tryon_results"

# -------------------- Local Storage (fallback when Cloudinary disabled) --------------------
LOCAL_STORAGE_DIR = Path(os.getenv("LOCAL_STORAGE_DIR", str(BASE_DIR / "local_storage")))
LOCAL_ORIG_DIR = LOCAL_STORAGE_DIR / "originals"
LOCAL_CUT_DIR = LOCAL_STORAGE_DIR / "cutouts"
LOCAL_TRYON_DIR = LOCAL_STORAGE_DIR / "tryon_results"
LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL", "http://127.0.0.1:5001")

# -------------------- Gradio --------------------
GRADIO_SPACE = os.getenv("GRADIO_SPACE", "zhengchong/CatVTON")
HF_TOKEN = os.getenv("HF_TOKEN")  # Optional, for private spaces

# -------------------- Model Paths --------------------
MODEL_PATH = MODELS_DIR / "best_clothing_model.h5"
LABELS_PATH = MODELS_DIR / "class_labels.json"
CONFIG_PATH = MODELS_DIR / "model_config.json"
REJECTION_PATH = MODELS_DIR / "rejection_threshold.json"
