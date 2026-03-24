# ForestTalk

ForestTalk is a simple web app for detecting and counting trees in aerial imagery using DeepForest.

The current target MVP lets a user:

- upload an aerial image
- run tree detection
- view an estimated tree count
- view an annotated image with detected tree crowns

## Repository Structure

```text
ForestTalk/
  README.md
  AGENT.md
  frontend/
  backend/
  docs/
  scripts/
```

## Local Setup

ForestTalk's frontend expects a modern Node runtime. If you're using `nvm`, Node 20 is a good stable choice for this project.

### Install backend dependencies

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Run backend

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

The backend exposes `GET /health`, `POST /predict`, and static annotated outputs under `/outputs/...`.

### Run frontend

```bash
nvm install 20
nvm use 20
cd frontend
npm install
npm run dev
```

## Prediction Flow

The backend saves uploads to `backend/uploads/`, loads the pretrained DeepForest tree crown model once at startup, writes annotated PNG results to `backend/outputs/`, and returns a response like:

```json
{
  "tree_count": 42,
  "detections": [
    {
      "xmin": 100.0,
      "ymin": 120.0,
      "xmax": 180.0,
      "ymax": 210.0,
      "score": 0.91,
      "label": "tree"
    }
  ],
  "annotated_image_url": "/outputs/result_123.png"
}
```

## Manual Test

1. Start the backend and frontend.
2. Open the frontend in your browser, usually `http://127.0.0.1:5173`.
3. Pick one aerial JPG or PNG image with visible tree crowns.
4. Click `Count Trees`.
5. Confirm the UI shows a non-placeholder `tree_count` and an annotated image loaded from the backend.
6. Optionally open the returned `annotated_image_url` directly in the browser, for example `http://127.0.0.1:8000/outputs/<generated-file>.png`.

## Where Things Happen

- Model loading happens once during FastAPI startup in [backend/app/main.py](/Users/traviscashion/code/travis-cashion/ForestTalk/backend/app/main.py) through [backend/app/services/deepforest_service.py](/Users/traviscashion/code/travis-cashion/ForestTalk/backend/app/services/deepforest_service.py).
- Single-image inference happens in [backend/app/services/deepforest_service.py](/Users/traviscashion/code/travis-cashion/ForestTalk/backend/app/services/deepforest_service.py).
- Upload validation and response shaping happen in [backend/app/api/routes/predict.py](/Users/traviscashion/code/travis-cashion/ForestTalk/backend/app/api/routes/predict.py).
- Bounding box drawing happens in [backend/app/utils/image_utils.py](/Users/traviscashion/code/travis-cashion/ForestTalk/backend/app/utils/image_utils.py).
