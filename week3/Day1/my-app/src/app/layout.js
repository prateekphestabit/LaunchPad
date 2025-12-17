export const metadata = {
  title: "My App",
  description: "this default file was created manually",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
} 