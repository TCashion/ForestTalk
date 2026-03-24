from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import settings
from app.schemas.prediction import PredictionResponse
from app.services.deepforest_service import (
    DeepForestModelUnavailableError,
    DeepForestPredictionError,
    deepforest_service,
)
from app.utils.image_utils import save_annotated_image

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
FORMAT_TO_EXTENSION = {"JPEG": ".jpg", "PNG": ".png"}

router = APIRouter(tags=["predict"])


def _build_upload_path(original_filename: str | None) -> Path:
    extension = Path(original_filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        extension = ".png"
    return settings.uploads_dir / f"upload_{uuid4().hex}{extension}"


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile | None = File(default=None)) -> PredictionResponse:
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An image file is required.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PNG and JPEG images are supported.",
        )

    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty.",
            )

        upload_path = _build_upload_path(file.filename)
        settings.uploads_dir.mkdir(parents=True, exist_ok=True)
        upload_path.write_bytes(file_bytes)

        with Image.open(upload_path) as uploaded_image:
            image_format = (uploaded_image.format or "").upper()
        expected_extension = FORMAT_TO_EXTENSION.get(image_format)
        if expected_extension is None:
            upload_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PNG and JPEG images are supported.",
            )

        if upload_path.suffix.lower() != expected_extension:
            corrected_path = upload_path.with_suffix(expected_extension)
            upload_path.rename(corrected_path)
            upload_path = corrected_path

        detections = deepforest_service.predict_image(upload_path)
        annotated_path = save_annotated_image(
            source_image_path=upload_path,
            detections=detections,
            output_dir=settings.outputs_dir,
        )
    except UnidentifiedImageError as exc:
        upload_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid image.",
        ) from exc
    except DeepForestModelUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"DeepForest model is unavailable: {exc}",
        ) from exc
    except DeepForestPredictionError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    finally:
        await file.close()

    if not annotated_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Annotated output image was not created.",
        )

    return PredictionResponse(
        tree_count=len(detections),
        detections=detections,
        annotated_image_url=f"{settings.outputs_url_path}/{annotated_path.name}",
    )
