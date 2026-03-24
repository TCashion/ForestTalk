# ForestTalk Backend

Minimal FastAPI backend for the ForestTalk MVP.

## What It Does

- Accepts one PNG or JPEG upload at `POST /predict`
- Saves the uploaded source image to `backend/uploads/`
- Loads the pretrained DeepForest tree crown model once at startup
- Runs single-image prediction through a small service module
- Draws bounding boxes with Pillow
- Saves annotated output images to `backend/outputs/`
- Serves annotated images at `/outputs/<filename>.png`

## Run It

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m uvicorn app.main:app --reload
```
