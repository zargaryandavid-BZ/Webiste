const twilio = require('twilio');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const {
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    NOTIFICATION_PHONE,
  } = process.env;

  if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN || !TWILIO_PHONE_NUMBER || !NOTIFICATION_PHONE) {
    console.error('Missing Twilio environment variables');
    return res.status(500).json({ error: 'Server is not configured for SMS notifications.' });
  }

  const { name, email, shop, phone, employees, module } = req.body || {};

  if (!name || !email || !shop || !phone || !employees || !module) {
    return res.status(400).json({ error: 'All fields are required.' });
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

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Twilio error:', err.message);
    return res.status(502).json({ error: 'Failed to send SMS notification.' });
  }
};
