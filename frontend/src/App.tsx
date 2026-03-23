import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";

import { getBackendAssetUrl, uploadImage } from "./lib/api";
import type { PredictionResponse } from "./types/prediction";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setSelectedFile(file);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedFile) {
      setError("Please choose a PNG or JPEG image first.");
      return;
    }

    setIsSubmitting(true);
    setError(null);
    setResult(null);

    try {
      const response = await uploadImage(selectedFile);
      setResult(response);
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Something went wrong while uploading the image.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-6 py-16">
      <div className="surface w-full max-w-3xl px-8 py-12 sm:px-10">
        <div className="space-y-10">
          <div className="space-y-4 text-center">
            <p className="text-accent text-sm font-medium uppercase tracking-[0.25em]">
              Forest Intelligence
            </p>
            <h1 className="text-4xl font-semibold tracking-tight text-slate-50 sm:text-5xl">
              ForestTalk
            </h1>
            <p className="text-muted text-lg leading-8">
              Upload an aerial image and send it to the backend for tree counting.
            </p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="surface-soft space-y-4 p-6">
              <label
                className="block text-sm font-medium text-slate-100"
                htmlFor="image-upload"
              >
                Select an image
              </label>
              <input
                id="image-upload"
                name="image-upload"
                type="file"
                accept="image/png,image/jpeg"
                onChange={handleFileChange}
                className="block w-full rounded-xl border border-strong bg-panel px-4 py-3 text-sm text-slate-100 file:mr-4 file:rounded-full file:border-0 file:bg-slate-100 file:px-4 file:py-2 file:text-sm file:font-medium file:text-slate-900"
              />
              <p className="text-muted text-sm">
                {selectedFile
                  ? `Selected file: ${selectedFile.name}`
                  : "PNG and JPEG images are supported."}
              </p>
            </div>

            <button
              className="btn-brand w-full sm:w-auto"
              disabled={isSubmitting}
              type="submit"
            >
              {isSubmitting ? "Uploading..." : "Count Trees"}
            </button>
          </form>

          {error ? (
            <div className="rounded-2xl border border-red-400/40 bg-red-500/10 px-5 py-4 text-sm text-red-100">
              {error}
            </div>
          ) : null}

          {result ? (
            <section className="surface-soft space-y-4 p-6">
              <div className="space-y-1">
                <h2 className="text-xl font-semibold text-slate-50">Prediction</h2>
                <p className="text-muted text-sm">
                  Real DeepForest tree crown detections from `POST /predict`
                </p>
              </div>

              <dl className="grid gap-4 text-sm text-slate-100 sm:grid-cols-2">
                <div>
                  <dt className="text-muted">Tree count</dt>
                  <dd>{result.tree_count}</dd>
                </div>
                <div>
                  <dt className="text-muted">Detections</dt>
                  <dd>{result.detections.length}</dd>
                </div>
              </dl>

              <div className="space-y-3">
                <p className="text-muted text-sm">Annotated image</p>
                <img
                  src={getBackendAssetUrl(result.annotated_image_url)}
                  alt="Annotated tree crown detections"
                  className="w-full rounded-2xl border border-strong object-cover"
                />
              </div>
            </section>
          ) : null}
        </div>
      </div>
    </main>
  );
}

export default App;
