# AR Fashion Try-On

AR Fashion Try-On is a full-stack augmented reality and AI-powered virtual garment try-on platform for fashion retail, e-commerce, and computer-vision research. It combines browser-based live AR preview, photo-realistic virtual try-on, garment classification, background removal, Cloudinary image delivery, and CatVTON inference through Gradio or Hugging Face Spaces.

This repository is optimized for modern AI discovery and developer onboarding around keywords such as virtual try-on, augmented reality fashion, AI fashion retail, garment classification, CatVTON, Stable Diffusion inpainting, FastAPI, Next.js, MediaPipe, TensorFlow, Cloudinary, Gradio, and Hugging Face Spaces.

## Main Specification

For the complete product, architecture, workflow, API, testing, and implementation specification, read:

- [Project specification](docs/PROJECT_SPEC.md)

The specification keeps the original full README-level detail while this root README stays focused on repository positioning, active services, and high-level navigation.

## What This Project Does

- Live AR garment preview using browser camera input and pose-aware overlays
- Photo-based AI virtual try-on using person and garment images
- Three photo workflows: single garment, complete outfit, and full reference image
- TensorFlow garment classification for upper/lower/unknown detection
- Background removal for transparent garment cutouts
- Outfit construction from separate upper and lower garments
- Cloudinary-backed upload, CDN delivery, and result persistence
- CatVTON-based try-on inference through Gradio or Hugging Face Spaces

## Active System

```text
web-frontend
  -> garment-processing-api
    -> CatVTON Gradio / Hugging Face Space
      -> Cloudinary
```

The deprecated backend experiments are preserved under `deprecated-backends/` for reference, but they are not part of the active runtime path.

## Repository Layout

```text
.
├── web-frontend/                 # Active Next.js app
├── garment-processing-api/       # Active FastAPI garment API
├── catvton-gradio/               # CatVTON Gradio service and model pipeline
├── deprecated-backends/          # Preserved legacy backend experiments
├── docs/                         # Project specification and roadmap
├── vton-api-notebook/            # Notebook experiments
└── docker-compose.yml
```

## Active Services

| Service | Directory | Stack | Default Port |
| --- | --- | --- | --- |
| Frontend | `web-frontend/` | Next.js, TypeScript, Tailwind | `3000` |
| Garment API | `garment-processing-api/` | FastAPI, TensorFlow, rembg, uv | `5000` |
| CatVTON service | `catvton-gradio/` | Gradio, PyTorch | `7860` |
| Cloudinary | external | Managed CDN | N/A |

## Prerequisites

**Required:**

- Node.js 18+
- Python 3.10+
- [pnpm](https://pnpm.io/installation)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

**Optional:**

- CUDA-capable GPU (8-10 GB+ VRAM recommended) for local CatVTON inference
- Docker for containerized supporting services (PostgreSQL, Redis)
- [Cloudinary](https://cloudinary.com/) account for image CDN
- Hugging Face account or token for private Spaces

## Quick Start

### 1. Frontend

```bash
cd web-frontend
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

Create `web-frontend/.env.local` with your API and Cloudinary configuration:

```bash
NEXT_PUBLIC_GARMENT_API_BASE=http://127.0.0.1:5000
NEXT_PUBLIC_VTON_API_BASE=http://127.0.0.1:7860
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your_cloud_name
NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET=your_preset
```

### 2. Garment Processing API

```bash
cd garment-processing-api
uv sync
uv run bash scripts/download_models_local.sh
```

> The download script pulls trained TensorFlow model files (`.h5`) from Google Drive. These files are excluded from Git due to size. JSON metadata files in `models/` are committed and kept in place.

Configure environment:

```bash
cp .env.example .env
# Fill in your Cloudinary credentials and optional HF_TOKEN.
```

Start the API:

```bash
uv run uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

Open [http://localhost:5000/docs](http://localhost:5000/docs) for the interactive API documentation.

### 3. CatVTON Virtual Try-On

**Option A: Hugging Face Space (no local GPU required)**

Configure a Hugging Face Space URL in the Garment API's `.env`. No local setup needed, but subject to hosted GPU quotas and cold starts.

**Option B: Local inference (requires GPU)**

```bash
cd catvton-gradio
pip install -r requirements.txt
python app.py
```

Open [http://localhost:7860](http://localhost:7860). Local inference requires 8-10 GB or more of GPU memory.

### 4. Docker (Supporting Services)

The included `docker-compose.yml` provides PostgreSQL and Redis for local development:

```bash
docker compose up -d
```

This starts:
- PostgreSQL 15 on `localhost:5432` (database: `ar_fashion`, user: `user`, password: `pass`)
- Redis 7 on `localhost:6379`

## Key API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check with model status |
| `POST` | `/detect_garment_type` | Classify garment as upper/lower/unknown |
| `POST` | `/classify_garment` | Classify garment and generate transparent cutout |
| `POST` | `/classify_garment_by_url` | Same as above, using a Cloudinary URL |
| `POST` | `/construct_outfit` | Merge upper and lower garments into an outfit |
| `POST` | `/virtual_tryon` | Run CatVTON try-on inference |

Full API reference: [API Documentation](garment-processing-api/docs/api/API_DOCUMENTATION.md)

## Technology Stack

### Frontend
Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui, Zustand, Axios, MediaPipe Pose, Three.js / React Three Fiber

### Garment API
FastAPI, TensorFlow/Keras, rembg (U2NET), OpenCV, Pillow, Cloudinary SDK, Gradio Client, Uvicorn / Gunicorn, uv

### Virtual Try-On
CatVTON, Stable Diffusion Inpainting, PyTorch, DensePose, SCHP, Gradio, Hugging Face Spaces

## Documentation

- [Project specification](docs/PROJECT_SPEC.md)
- [Frontend README](web-frontend/README.md)
- [Garment API README](garment-processing-api/README.md)
- [Garment API reference](garment-processing-api/docs/api/API_DOCUMENTATION.md)
- [Garment API deployment guide](garment-processing-api/docs/deployment/DEPLOYMENT.md)
- [CatVTON README](catvton-gradio/README.md)
- [Deprecated backends](deprecated-backends/README.md)
- [Roadmap](docs/ROADMAP.md)

## Troubleshooting

**Model not loaded on startup:**
Run `uv run bash scripts/download_models_local.sh` from `garment-processing-api/`. The `.h5` model files are not committed to Git.

**CatVTON out of memory:**
Local inference requires significant GPU VRAM. Use Option A (Hugging Face Space) if your GPU has less than 8 GB, or reduce input image resolution.

**Camera not working in browser:**
Camera access (`getUserMedia`) requires a secure context. Use `localhost` (which is exempt) or serve over HTTPS in production.

**First try-on request is slow:**
Cold start on hosted GPU services (Hugging Face Spaces) can take 30-60 seconds. Subsequent requests are faster.

**Cloudinary uploads failing:**
Verify your `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` in `garment-processing-api/.env`. Also check `NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME` and `NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET` in `web-frontend/.env.local`.

## License

MIT License.
