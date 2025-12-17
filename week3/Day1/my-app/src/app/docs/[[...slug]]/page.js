export default async function DocsPage({ params }) {
  const slugObject = await params;
  const slug = slugObject.slug;
  console.log(slug);
  let slugLen = slug !== undefined ? slug.length : 0;
  console.log(slugLen);
  
  if(slugLen === 0){
    return (
        <main>
            <h1>your are currently viewing docs page</h1>
        </main>
    );
  }
  else if(slugLen === 1){
    return (
        <main>
            <h1>your are currently viewing feature {slug[0]} of docs page</h1>
        </main>
    );
  }
  else return (
    <main>
      <h1>your are currently viewing concept {slug[1]} of feature {slug[0]} of docs page</h1>
    </main>
  );
}