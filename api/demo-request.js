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
  const isDeck = module === 'Deck Download';

  if (isDeck) {
    if (!name || !email || !phone) {
      return res.status(400).json({ error: 'Name, email, and phone are required.' });
    }
  } else if (!name || !email || !shop || !phone || !employees || !module) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  const message = isDeck
    ? [
        'New Pulse deck download',
        '',
        `Name: ${name}`,
        `Email: ${email}`,
        `Phone: ${phone}`,
      ].join('\n')
    : [
        'New Pulse demo request',
        '',
        `Name: ${name}`,
        `Email: ${email}`,
        `Print shop: ${shop}`,
        `Phone: ${phone}`,
        `Employees: ${employees}`,
        `Module: ${module}`,
      ].join('\n');

  // NOTIFICATION_PHONE can hold several numbers separated by commas; all are texted at once.
  const recipients = NOTIFICATION_PHONE.split(',').map((n) => n.trim()).filter(Boolean);

  const client = twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);
  const results = await Promise.allSettled(
    recipients.map((to) => client.messages.create({ body: message, from: TWILIO_PHONE_NUMBER, to }))
  );

  results.forEach((r, i) => {
    if (r.status === 'rejected') console.error(`Twilio error for ${recipients[i]}:`, r.reason && r.reason.message);
  });

  // Succeed as long as at least one person got the text.
  if (results.some((r) => r.status === 'fulfilled')) {
    return res.status(200).json({ ok: true });
  }
  return res.status(502).json({ error: 'Failed to send SMS notification.' });
};
