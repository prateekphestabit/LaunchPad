export default async function ProductsPage({ params }) {
  const Id = await params;
  return (
    <main>
      <h1>{Id.productId}</h1>
    </main>
  );
}