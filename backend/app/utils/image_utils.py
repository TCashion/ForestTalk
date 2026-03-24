from pathlib import Path
from uuid import uuid4

import matplotlib.pyplot as plt
import pandas as pd
from deepforest.visualize import plot_results
from PIL import Image
from shapely.geometry import box

from app.schemas.prediction import Detection


def save_annotated_image(
    source_image_path: Path, detections: list[Detection], output_dir: Path
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    basename = f"result_{uuid4().hex}"
    output_path = output_dir / f"{basename}.png"

    results = pd.DataFrame(
        [
            {
                "xmin": detection.xmin,
                "ymin": detection.ymin,
                "xmax": detection.xmax,
                "ymax": detection.ymax,
                "score": detection.score,
                "label": detection.label,
                "image_path": str(source_image_path),
            }
            for detection in detections
        ]
    )

    if results.empty:
        with Image.open(source_image_path) as source_image:
            source_image.convert("RGB").save(output_path, format="PNG")
        return output_path

    results["geometry"] = results.apply(
        lambda row: box(row.xmin, row.ymin, row.xmax, row.ymax),
        axis=1,
    )

    figure = plot_results(
        results=results,
        image=str(source_image_path),
        savedir=str(output_dir),
        basename=basename,
        show=False,
    )
    plt.close(figure)

    return output_path
