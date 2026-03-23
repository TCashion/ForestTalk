from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw

from app.schemas.prediction import Detection


def save_annotated_image(
    source_image_path: Path, detections: list[Detection], output_dir: Path
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(source_image_path) as source_image:
        annotated_image = source_image.convert("RGB")

    draw = ImageDraw.Draw(annotated_image)
    for detection in detections:
        box = (
            detection.xmin,
            detection.ymin,
            detection.xmax,
            detection.ymax,
        )
        draw.rectangle(box, outline="#38b48b", width=3)
        label_text = f"{detection.label} {detection.score:.2f}"
        text_origin = (detection.xmin + 4, max(4, detection.ymin - 18))
        draw.text(text_origin, label_text, fill="#f8fafc")

    output_path = output_dir / f"result_{uuid4().hex}.png"
    annotated_image.save(output_path, format="PNG")
    return output_path
