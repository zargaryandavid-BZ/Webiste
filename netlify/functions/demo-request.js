const twilio = require('twilio');

exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
      },
    };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  };

  const {
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    NOTIFICATION_PHONE,
  } = process.env;

  if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_PHONE_NUMBER || !NOTIFICATION_PHONE) {
    console.error('Missing Twilio environment variables');
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Server is not configured for SMS notifications.' }),
    };
  }

  let data;
  try {
    data = JSON.parse(event.body);
  } catch {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'Invalid request body.' }),
    };
  }

  const { name, email, shop, phone, employees, module } = data;

  if (!name || !email || !shop || !phone || !employees || !module) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'All fields are required.' }),
    };
  }

  const message = [
    'New Pulse demo request',
    '',
    `Name: ${name}`,
    `Email: ${email}`,
    `Print shop: ${shop}`,
    `Phone: ${phone}`,
    `Employees: ${employees}`,
    `Module: ${module}`,
  ].join('\n');

  try {
    const client = twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);
    await client.messages.create({
      body: message,
      from: TWILIO_PHONE_NUMBER,
      to: NOTIFICATION_PHONE,
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ ok: true }),
    };
  } catch (err) {
    console.error('Twilio error:', err.message);
    return {
      statusCode: 502,
      headers,
      body: JSON.stringify({ error: 'Failed to send SMS notification.' }),
    };
  }
};
