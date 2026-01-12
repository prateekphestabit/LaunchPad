/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://server:5000/:path*",
      },
    ];
  },
  reactCompiler: true,
};

export default nextConfig;
