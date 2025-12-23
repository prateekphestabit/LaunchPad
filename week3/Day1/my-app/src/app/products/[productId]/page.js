export async function generateMetadata({ params }, parent) {
  const id = await params
  const productId = id.productId;

  return {
    title: `Product ${productId}`,
    description: `Details for product ${productId}`,
  }
}

export default async function ProductsPage({ params }) {
  const Id = await params;
  return (
    <main>
      <h1>{Id.productId}</h1>
    </main>
  );
}