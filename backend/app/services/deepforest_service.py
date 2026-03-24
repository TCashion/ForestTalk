from __future__ import annotations

from pathlib import Path
from typing import Any

from app.schemas.prediction import Detection


class DeepForestServiceError(Exception):
    """Base error for DeepForest prediction failures."""


class DeepForestModelUnavailableError(DeepForestServiceError):
    """Raised when the model could not be loaded at startup."""


class DeepForestPredictionError(DeepForestServiceError):
    """Raised when prediction fails for an uploaded image."""


class DeepForestService:
    def __init__(self) -> None:
        self._model: Any | None = None
        self._load_error: Exception | None = None

    def load_model(self) -> None:
        if self._model is not None:
            return

        try:
            from deepforest import main

            model = main.deepforest()
            if hasattr(model, "load_model"):
                model.load_model("weecology/deepforest-tree")
            elif hasattr(model, "use_release"):
                model.use_release()
            else:
                raise RuntimeError("Unsupported DeepForest model interface.")
            self._model = model
            self._load_error = None
        except Exception as exc:  # pragma: no cover - depends on local ML runtime
            self._model = None
            self._load_error = exc

    def is_ready(self) -> bool:
        return self._model is not None

    def get_load_error_message(self) -> str:
        if self._load_error is None:
            return "The DeepForest model is not loaded."
        return str(self._load_error)

    def predict_image(self, image_path: Path) -> list[Detection]:
        if self._model is None:
            raise DeepForestModelUnavailableError(self.get_load_error_message())

        try:
            raw_predictions = self._model.predict_image(path=str(image_path))
        except Exception as exc:  # pragma: no cover - depends on local ML runtime
            raise DeepForestPredictionError(
                f"DeepForest inference failed: {exc}"
            ) from exc

        if raw_predictions is None:
            return []

        if not hasattr(raw_predictions, "to_dict"):
            raise DeepForestPredictionError(
                "DeepForest returned an unexpected prediction format."
            )

        records = raw_predictions.to_dict(orient="records")
        detections: list[Detection] = []
        for record in records:
            detections.append(
                Detection(
                    xmin=float(record["xmin"]),
                    ymin=float(record["ymin"]),
                    xmax=float(record["xmax"]),
                    ymax=float(record["ymax"]),
                    score=float(record.get("score", 0.0)),
                    label=str(record.get("label") or "tree"),
                )
            )

        return detections


deepforest_service = DeepForestService()
