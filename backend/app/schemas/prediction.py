from pydantic import BaseModel


class Detection(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    score: float
    label: str


class PredictionResponse(BaseModel):
    tree_count: int
    detections: list[Detection]
    annotated_image_url: str
