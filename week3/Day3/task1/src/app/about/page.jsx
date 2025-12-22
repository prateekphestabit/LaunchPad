import Link from "next/link";
import Sidebar from "../../../components/ui/Sidebar";

export default function AboutPage() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar currPage="About Us"/>

      <main style={{ flex: 1 }} className="px-6 py-12 md:px-12">
        <section className="mx-auto w-full max-w-4xl">
          <p className="text-sm font-medium text-gray-500">LaunchPad</p>

          <h1 className="mt-3 text-4xl font-semibold tracking-tight md:text-5xl">
            About
          </h1>

          <p className="mt-4 text-base leading-7 text-gray-600 md:text-lg">
            This project is a Next.js dashboard-style UI built as part of Week 3,
            Day 3. The goal is to practice component-driven design, reusable UI
            patterns, and app routing.
          </p>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            <div className="rounded-xl border border-gray-200 bg-white p-5">
              <h2 className="text-lg font-semibold">What you’ll find here</h2>
              <ul className="mt-3 list-disc space-y-2 pl-5 text-gray-600">
                <li>Reusable UI components (cards, navbar, sidebar, options)</li>
                <li>Multi-page routing using the App Router</li>
                <li>Dashboard layout patterns and responsive sections</li>
                <li>Static assets (icons, fonts, illustrations)</li>
              </ul>
            </div>

            <div className="rounded-xl border border-gray-200 bg-white p-5">
              <h2 className="text-lg font-semibold">Why this page</h2>
              <p className="mt-3 text-gray-600 leading-7">
                The About page gives a quick overview of the project and provides
                easy navigation back to the main pages.
              </p>

              <div className="mt-5 flex flex-wrap gap-3">
                <Link
                  href="/"
                  className="inline-flex items-center justify-center rounded-lg bg-black px-4 py-2 text-sm font-medium text-white"
                >
                  Go to Home
                </Link>
                <Link
                  href="/dashboard"
                  className="inline-flex items-center justify-center rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-900"
                >
                  View Dashboard
                </Link>
              </div>
            </div>
          </div>

          <div className="mt-10 rounded-xl border border-gray-200 bg-gray-50 p-5">
            <h3 className="text-base font-semibold">Tech</h3>
            <p className="mt-2 text-gray-600">
              Next.js (App Router) • React • CSS/Tailwind-style utility classes
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}