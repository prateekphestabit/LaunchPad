export async function POST(request) {
  try {
    const body = await request.json();
    
    // This fetch runs on the server side (inside Docker container)
    // So it CAN use the Docker network hostname 'server'
    const response = await fetch('http://server:8000/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error('Failed to save data');
    }

    return Response.json({ success: true, message: 'Data saved to DB' });
  } catch (error) {
    console.error('Error saving data:', error);
    return Response.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}