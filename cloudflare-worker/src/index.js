export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const data = await request.json();
    const { from, body, fromMe } = data;

    if (fromMe) return new Response('OK', { status: 200 });

    const userId = from.split('@')[0];
    
    const response = await fetch(`${env.PYTHON_BACKEND_URL}/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.API_SECRET}`
      },
      body: JSON.stringify({ user_id: userId, message: body })
    });

    const result = await response.json();
    
    await fetch(`${env.WAHA_URL}/api/sendText`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.WAHA_API_KEY}`
      },
      body: JSON.stringify({
        chatId: from,
        text: result.response,
        session: 'default'
      })
    });

    return new Response('OK', { status: 200 });
  }
};
