export type Detection = {
  xmin: number;
  ymin: number;
  xmax: number;
  ymax: number;
  score: number;
  label: string;
};

export type PredictionResponse = {
  tree_count: number;
  detections: Detection[];
  annotated_image_url: string;
};
