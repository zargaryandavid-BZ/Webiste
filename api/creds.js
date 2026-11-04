const crypto = require('crypto');

// Failed attempts per IP. Best-effort: each serverless instance keeps its own map.
const MAX_ATTEMPTS = 5;
const WINDOW_MS = 15 * 60 * 1000;
const attempts = new Map();

function clientIp(req) {
  const fwd = req.headers['x-forwarded-for'];
  return (Array.isArray(fwd) ? fwd[0] : fwd || '').split(',')[0].trim() || 'unknown';
}

function isLocked(ip) {
  const entry = attempts.get(ip);
  if (!entry) return false;
  if (Date.now() > entry.reset) {
    attempts.delete(ip);
    return false;
  }
  return entry.count >= MAX_ATTEMPTS;
}

function recordFailure(ip) {
  const entry = attempts.get(ip);
  if (!entry || Date.now() > entry.reset) {
    attempts.set(ip, { count: 1, reset: Date.now() + WINDOW_MS });
  } else {
    entry.count += 1;
  }
}

// Compare hashes so the check takes the same time whatever the input.
function passwordMatches(given, expected) {
  const a = crypto.createHash('sha256').update(String(given)).digest();
  const b = crypto.createHash('sha256').update(String(expected)).digest();
  return crypto.timingSafeEqual(a, b);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { CREDS_PASSWORD, MODULE_CREDENTIALS } = process.env;
  if (!CREDS_PASSWORD || !MODULE_CREDENTIALS) {
    console.error('Missing CREDS_PASSWORD or MODULE_CREDENTIALS');
    return res.status(500).json({ error: 'Credentials are not configured.' });
  }

  const ip = clientIp(req);
  if (isLocked(ip)) {
    return res.status(429).json({ error: 'Too many attempts. Try again in 15 minutes.' });
  }

  const { password } = req.body || {};
  if (!password || !passwordMatches(password, CREDS_PASSWORD)) {
    recordFailure(ip);
    await sleep(800);
    return res.status(401).json({ error: 'Wrong password.' });
  }

  attempts.delete(ip);
  try {
    return res.status(200).json({ credentials: JSON.parse(MODULE_CREDENTIALS) });
  } catch {
    console.error('MODULE_CREDENTIALS is not valid JSON');
    return res.status(500).json({ error: 'Credentials are not configured.' });
  }
};
