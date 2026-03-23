function App() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-100 px-6 py-16 text-slate-900">
      <div className="w-full max-w-2xl rounded-3xl border border-gray-200 bg-white px-8 py-12 shadow-sm sm:px-10">
        <div className="space-y-4 text-center">
          <p className="text-sm font-medium uppercase tracking-[0.25em] text-emerald-700">
            Forest Intelligence
          </p>
          <h1 className="text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
            ForestTalk
          </h1>
          <p className="text-lg leading-8 text-slate-600">
            Analyze aerial imagery to detect and count trees.
          </p>
        </div>
      </div>
    </main>
  );
}

export default App;
