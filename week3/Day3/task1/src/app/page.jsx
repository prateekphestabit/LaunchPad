import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 text-center">
        <p className="mb-4 text-sm font-medium tracking-widest text-slate-300">
          LAUNCHPAD
        </p>

        <h1 className="text-balance text-4xl font-semibold leading-tight sm:text-6xl">
          Clean landing page. One button. Straight to the dashboard.
        </h1>

        <p className="mt-5 max-w-2xl text-pretty text-base text-slate-300 sm:text-lg">
          Built with Next.js (App Router) + Tailwind CSS + JSX. Click the button
          below to open your dashboard.
        </p>

        <div className="mt-10">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-xl bg-indigo-500 px-6 py-3 text-base font-semibold text-white shadow-sm transition hover:bg-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:ring-offset-2 focus:ring-offset-slate-950"
          >
            Open Dashboard
          </Link>
        </div>

        <div className="mt-4">
          <Link
            href="/about"
            className="inline-flex items-center justify-center rounded-lg bg-black px-4 py-2 text-sm font-medium text-white"
          >
            About
          </Link>
        </div>
      </div>
    </main>
  );
}