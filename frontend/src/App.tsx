function App() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,_rgba(108,163,154,0.18),_transparent_40%),linear-gradient(180deg,_rgba(255,255,255,0.03),_transparent_55%)] px-6 py-16">
      <div className="surface w-full max-w-2xl px-8 py-12 sm:px-10">
        <div className="space-y-4 text-center">
          <p className="text-accent text-sm font-medium uppercase tracking-[0.25em]">
            Forest Intelligence
          </p>
          <h1 className="text-4xl font-semibold tracking-tight text-slate-50 sm:text-5xl">
            ForestTalk
          </h1>
          <p className="text-muted text-lg leading-8">
            Analyze aerial imagery to detect and count trees.
          </p>
        </div>
      </div>
    </main>
  );
}

export default App;
