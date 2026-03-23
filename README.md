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

## Local Development

### Frontend

```bash
nvm install 20
nvm use 20
cd frontend
npm install
npm run dev
```

ForestTalk's frontend expects a modern Node runtime. If you're using `nvm`, Node 20 is a good stable choice for this project.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

The frontend starts on Vite's default local port, and the backend exposes a minimal health endpoint at `GET /health`.
