# AGENT.md

## Project Overview

ForestTalk is a monorepo web application for analyzing aerial imagery with DeepForest.

Current MVP goal:

- User uploads an aerial image
- Backend runs DeepForest tree crown detection
- App returns:
  - estimated tree count
  - detected bounding boxes
  - annotated output image

This project is intentionally small and beginner-friendly. Favor simple, readable implementations over abstraction-heavy designs.

---

## Primary Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

### Backend

- Python 3.11.15
- FastAPI
- Uvicorn
- DeepForest
- Pillow

---

## Repository Structure

Use a monorepo structure like this:

```text
ForestTalk/
  README.md
  AGENT.md
  frontend/
  backend/
  docs/
  scripts/
```

Preferred backend structure:

```text
backend/
  app/
    main.py
    api/
      routes/
        health.py
        predict.py
    services/
      deepforest_service.py
    schemas/
      prediction.py
    utils/
      image_utils.py
    core/
      config.py
  uploads/
  outputs/
  pyproject.toml
```

Preferred frontend structure:

```text
frontend/
  src/
    components/
    pages/
    lib/
    types/
  public/
  package.json
  tsconfig.json
  vite.config.ts
  tailwind.config.js
```

## Engineering Principles

1. Keep the MVP narrow.
   - Do not add authentication, databases, background workers, cloud infra, or map integrations unless explicitly requested.
   - Focus on upload -> predict -> count -> visualize.
2. Optimize for clarity.
   - Prefer straightforward functions and file organization.
   - Avoid over-engineering, premature abstraction, and unnecessary design patterns.
3. Keep frontend and backend loosely coupled.
   - The frontend should consume backend APIs cleanly.
   - The backend should expose a minimal, stable API.
4. Make local development easy.
   - Assume one developer on a local machine.
   - Favor simple commands and clear setup steps.
5. Fail safely and visibly.
   - Validate file types and file sizes.
   - Return clear error messages.
   - Avoid silent failures.

## MVP Product Requirements

### Required MVP Functionality

- Upload a PNG or JPEG aerial image
- Submit image to backend
- Run DeepForest inference
- Return tree count
- Return bounding box detections
- Return an annotated image with boxes drawn

### Nice-to-Have Later

- Confidence threshold control
- Better result visualization
- Download annotated image
- Image metadata display
- Map-based selection workflow

### Explicitly Out of Scope for Now

- Training custom models
- User accounts
- Persistent storage
- Job queues
- Batch uploads
- Realtime inference on map tiles
- Production deployment infrastructure

## Backend Guidelines

### Python Version

Assume Python 3.11.15.

### Framework

Use FastAPI.

### API Endpoints

Start with only these endpoints:

- `GET /health`
  - Returns basic status JSON
- `POST /predict`
  - Accepts one image upload
  - Runs DeepForest prediction
  - Returns:
    - `tree_count`
    - `detections`
    - annotated image reference or payload

### Model Loading

- Load the DeepForest model once at app startup
- Do not reload the model per request

### File Handling

- Save uploads and outputs to local directories for MVP
- Keep file handling simple and explicit
- Clean up only if needed; do not overbuild lifecycle management initially

### Suggested Response Shape

```json
{
  "tree_count": 42,
  "detections": [
    {
      "xmin": 100,
      "ymin": 120,
      "xmax": 180,
      "ymax": 210,
      "score": 0.91,
      "label": "tree"
    }
  ],
  "annotated_image_url": "/outputs/result_123.png"
}
```

### Backend Coding Preferences

- Use type hints
- Use Pydantic models where helpful
- Keep route handlers thin
- Put DeepForest logic in `services/`
- Put image drawing helpers in `utils/`

## Frontend Guidelines

### Framework

Use React + TypeScript + Vite.

### Styling

- Use Tailwind CSS
- Prefer simple, clean, minimal styling
- Avoid heavy UI libraries unless explicitly requested
- Reuse the shared ForestTalk color system defined in `frontend/src/index.css`
- Prefer CSS variables and the existing utility/component classes such as `surface`, `surface-soft`, `text-muted`, and `text-accent`
- Keep the visual direction calm and nature-inspired: deep blue-green backgrounds, soft panel surfaces, muted text, and jade accents

### MVP UI Requirements

Include only:

- page title / app header
- image upload control
- selected image preview
- "Count Trees" submit button
- loading state
- result display:
  - tree count
  - annotated image

### Frontend Architecture Preferences

- Keep state management simple
- Prefer React hooks and local component state
- Do not add Redux, Zustand, or other state libraries unless needed

### API Integration

- Centralize API calls in a small utility module
- Keep response types explicit in TypeScript

## Dependency Management

### Backend

Preferred:

- `uv` for Python dependency management if convenient

Acceptable:

- standard `venv` + `pip` workflow

### Frontend

- use `npm`

Do not introduce multiple package managers unless there is a clear reason.

## Testing Guidance

For the MVP, light testing is sufficient.

### Backend

Prioritize a small number of tests for:

- health endpoint
- predict endpoint validation
- response shape

### Frontend

- only add tests if explicitly requested
- prioritize implementation speed and clarity first

## Documentation Expectations

When making meaningful changes:

- update `README.md` if setup or commands change
- keep setup instructions accurate
- document any non-obvious environment or dependency issues

## Constraints for the Coding Agent

When editing this project:

- Preserve the monorepo structure
- Do not perform broad refactors unless requested
- Do not introduce new infrastructure by default
- Prefer minimal viable implementations
- Keep all code readable by a beginner learning ML/web integration
- Explain major technical choices in comments only when helpful, not excessively
- When uncertain, choose the simpler path

## Immediate Build Priorities

In order of priority:

~~1. Scaffold frontend and backend folders~~ COMPLETE
~~2. Create FastAPI app with `/health`~~ COMPLETE
3. Create React app shell with Tailwind
4. Create upload flow from frontend to backend
5. Stub `POST /predict` with fake response
6. Integrate DeepForest prediction
7. Add annotated image output
8. Improve UX and error handling

## Definition of Success for MVP

A successful MVP is:

- easy to run locally
- easy to understand
- able to accept one aerial image
- able to produce a believable tree count and visual output
- structured cleanly enough to extend later
