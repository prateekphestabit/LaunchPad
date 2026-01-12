'use client'

let data = '';
const updateData = (newData) => {data = newData};
const uploadData = () => {
  console.log(data);
  
  // Call your own API route (runs in browser, hits localhost:3000)
  fetch('/api/data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: data }),
  })
  .then(response => response.json())
  .then(result => {
    console.log('Data saved to DB:', result);
  })
  .catch(error => {
    console.error('Error saving data:', error);
  });
}

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <div className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-6">
        <div className="w-full space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
              Welcome
            </h1>
            <p className="mt-3 text-slate-300">
              Enter your information to continue
            </p>
          </div>

          <div className="rounded-2xl bg-white/10 p-8 shadow-2xl backdrop-blur-lg">
            <form className="space-y-6">
              <div>
                <label htmlFor="email" className="sr-only">
                  Email address
                </label>
                <input
                  onChange={e => updateData(e.target.value)}
                  id="email"
                  name="email"
                  type="email"
                  placeholder="Enter your email"
                  className="w-full rounded-lg border border-white/20 bg-white/5 px-4 py-3 text-white placeholder-slate-400 backdrop-blur-sm transition focus:border-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-400/50"
                />
              </div>

              <button
                type="submit"
                onClick={uploadData}
                className="w-full rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 px-4 py-3 font-semibold text-white shadow-lg transition hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 focus:ring-offset-slate-900"
              >
                Submit
                
              </button>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
}