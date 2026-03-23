function App() {
  return (
    <main className="min-h-screen bg-stone-50 px-6 py-16 text-slate-900">
      <div className="mx-auto flex max-w-3xl flex-col gap-6 rounded-2xl border border-stone-200 bg-white p-8 shadow-sm">
        <span className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-700">
          Tree Detection MVP
        </span>
        <div className="space-y-3">
          <h1 className="text-4xl font-semibold tracking-tight text-slate-950">
            ForestTalk
          </h1>
          <p className="max-w-2xl text-base leading-7 text-slate-600">
            A simple web app for detecting and counting trees in aerial imagery
            with DeepForest.
          </p>
        </div>
      </div>
    </main>
  );
}

export default App;
