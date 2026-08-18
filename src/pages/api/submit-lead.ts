import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.formData();
    const rawName = data.get('name') as string || 'Guest';
    const rawEmail = data.get('email') as string || 'Not provided';
    const rawWechat = data.get('wechat') as string || 'Not provided';
    const rawPhone = data.get('phone') as string || 'Not provided';
    const city = data.get('city') as string || 'Unknown';
    const service = data.get('service') as string || 'Cleaning';

    // The Lead Capture Firewall Rules (Phase 4):
    // 2. Prevent Email duplication merging in Chatwoot
    const uniqueName = `${rawName} #${Date.now().toString(36)}`;

    // 3. Do not send phone_number to contact directly. Pack email and phone into content.
    const messageContent = `
New Lead for ${service} in ${city}!
- Name: ${rawName}
- WeChat ID: ${rawWechat}
- Phone: ${rawPhone}
- Email: ${rawEmail}

Service requested: ${service}
City: ${city}
    `;

    // 1. Use full domain for Chatwoot (placeholder domain per instructions)
    const CHATWOOT_DOMAIN = 'https://chat.example.com';
    const INBOX_ID = 'your_inbox_id'; // Placeholder
    const ACCOUNT_ID = '1'; // Placeholder
    
    // In a real scenario we'd do a fetch to Chatwoot API here:
    /*
    const contactRes = await fetch(`${CHATWOOT_DOMAIN}/api/v1/accounts/${ACCOUNT_ID}/contacts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api_access_token': 'YOUR_TOKEN' },
      body: JSON.stringify({
        inbox_id: INBOX_ID,
        name: uniqueName
        // strictly no email or phone here to prevent 422 / merge issues
      })
    });
    const contactData = await contactRes.json();
    
    const convRes = await fetch(`${CHATWOOT_DOMAIN}/api/v1/accounts/${ACCOUNT_ID}/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api_access_token': 'YOUR_TOKEN' },
      body: JSON.stringify({
        source_id: contactData.payload.contact.source_id,
        inbox_id: INBOX_ID
      })
    });
    const convData = await convRes.json();

    await fetch(`${CHATWOOT_DOMAIN}/api/v1/accounts/${ACCOUNT_ID}/conversations/${convData.id}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'api_access_token': 'YOUR_TOKEN' },
      body: JSON.stringify({
        content: messageContent,
        message_type: 'incoming'
      })
    });
    */
    
    console.log("Lead captured successfully following Phase 4 firewall rules:");
    console.log("Unique Name:", uniqueName);
    console.log("Message Content:", messageContent);

    // Astro redirect
    return Response.redirect(new URL('/quote?success=true', request.url), 302);
  } catch (error) {
    console.error('Lead submission error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
};
