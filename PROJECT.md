# Pulse Website — Project Documentation

> **Purpose of this document:** Give developers and AI agents full context to read, analyze, modify, and deploy this codebase without guessing. Last updated: June 2026.

---

## 1. Project Overview

**Pulse** is a marketing landing page for a print-shop management SaaS platform. It is a **static single-page website** with one serverless API route for lead capture via SMS.

| Item | Value |
|---|---|
| Product | Pulse — Print House Automation & Management Platform |
| Site type | Static HTML/CSS/JS landing page |
| Primary file | `index.html` (~1,400 lines, all-in-one) |
| Backend | One Vercel serverless function (`api/demo-request.js`) |
| Production URL | https://webiste-lilac.vercel.app |
| Vercel project | `bazaardavit/webiste` |
| GitHub remote | https://github.com/zargaryandavid-BZ/Webiste.git |
| Package name | `pulse-website` |

There is **no build step**, **no framework** (no React/Vue/Next), and **no CSS preprocessor**. Everything lives in one HTML file except the API route and assets.

---

## 2. Directory Structure

```
Webiste/
├── index.html              # Entire frontend: HTML, CSS, JS
├── api/
│   └── demo-request.js     # Vercel serverless — Twilio SMS on form submit
├── images/                 # Active image assets (referenced by index.html)
├── website photos/         # Original source images (duplicate/legacy copies)
├── netlify/
│   └── functions/
│       └── demo-request.js # Legacy Netlify version (NOT used in production)
├── netlify.toml            # Legacy Netlify config (NOT used in production)
├── package.json            # Only dependency: twilio
├── package-lock.json
├── .env.example            # Template for env vars (placeholders only)
├── .env                    # Local secrets — gitignored, never commit
├── .gitignore
├── .vercel/                # Vercel CLI link metadata — gitignored
└── PROJECT.md              # This file
```

### Important path rules

- **Always use `images/`** for `<img src>` paths. Do not reference root-level filenames or `website photos/` (spaces break some deployments).
- **`website photos/`** is a legacy folder with duplicate originals. Prefer `images/` for all new work.
- **Never commit `.env`** — it contains Twilio credentials.

---

## 3. Page Structure (`index.html`)

The page is a single scrolling landing page divided into sections. CSS is embedded in `<style>` in `<head>`. JavaScript is at the bottom in one `<script>` block.

### 3.1 Sections (in DOM order)

| Order | Section ID | Nav label | Content |
|---|---|---|---|
| 1 | `#home` | — | Hero: headline, subtitle, CTA, production photo + mock dashboard cards |
| 2 | `#modules` | Platform *(intended)* | 5 product module cards (CRM, Design, Production, HR, Broker Websites) |
| 3 | `#problem` | The Problem | 6 pain-point cards + **demo request form** (right column) |
| 4 | `#transformation` | — | Before/After comparison ("Chaos Mode" vs "In Control") |
| 5 | — | — | Footer |

### 3.2 Known navigation bugs (do not break accidentally)

Nav and footer links reference IDs that **do not exist** on any `<section>`:

| Link href | Intended target | Actual status |
|---|---|---|
| `#products` | Platform modules | **Broken** — section is `#modules`, not `#products` |
| `#why` | Why Pulse | **Broken** — no section with this ID (CSS exists, HTML section removed or never added) |
| `#process` | How It Works | **Broken** — no section with this ID |
| `#contact` | Demo form | **Broken** — form lives inside `#problem`, no `#contact` ID |

Working links: `#home`, `#problem`, `#modules`, `#transformation`.

**To fix nav:** Add missing `id` attributes to sections or update `<a href>` values in nav (lines ~549–555) and footer (lines ~1323–1327).

### 3.3 Hero section (`#home`)

- **Headline:** "No Mess in the Printing House. Know Your Numbers."
- **Subtitle:** "The user-friendly management platform built for small and mid-size print shops. Easy to adopt, easy to run: From first quote to delivered job."
- **Single CTA:** "Request a Demo" → `#contact` (broken anchor; scrolls nowhere unless fixed)
- **Removed:** "See the Platform" secondary button (intentionally removed)
- **Hero image:** `images/production-floor.jpg`
- **Visual:** Layered mock dashboard cards (static HTML, not live data)

### 3.4 Modules section (`#modules`)

Five cards in `.modules-grid`, each with photo, number, title, description, feature list:

| # | Title | Image file |
|---|---|---|
| 01 | Pulse CRM | `images/crm-operator.png` |
| 02 | Pulse Design Manager | `images/designer-at-work-stockcake.jpg` |
| 03 | Pulse Production | `images/operator-printing-press.jpg` |
| 04 | Pulse HR | `images/Employee-Time-Clocks-for-Your-Time-Tracking-Strategy.jpg` |
| 05 | Broker Websites | `images/broker-storefront.jpg` *(highlighted card)* |

Unused images in `images/` (available for swaps): `production-press.png`, `production-hp-printer.png`, `hp-indigo-printer.webp`, `scodix-ultra-6500.jpg`, etc.

### 3.5 Problem + Form section (`#problem`)

Left: 6 problem cards (`.pf-card`) in a 2×3 grid.  
Right: Demo request form (`.pf-form-box`).

### 3.6 Transformation section (`#transformation`)

Before/After side-by-side layout (`.ba-layout`). Static illustrative content, not interactive.

---

## 4. Demo Request Form

### 4.1 Location

Inside `#problem` section — form id: `demo-form`, handler: `handleSubmit(event)`.

### 4.2 Fields (all required)

| Field name | HTML type | Placeholder / label |
|---|---|---|
| `name` | text | Your name |
| `email` | email | Work email |
| `shop` | text | Print shop name |
| `phone` | tel | Phone number |
| `employees` | select | How many employees? |
| `module` | select | Which module interests you most? |

**Employee options:** 1–5, 6–20, 21–50, 50+  
**Module options:** Pulse CRM, Pulse Design Manager, Pulse Production, Pulse HR, Broker Websites, The full platform

### 4.3 Submit flow

```
User submits form
    → handleSubmit() in index.html (client JS)
    → POST /api/demo-request  (JSON body)
    → api/demo-request.js     (Vercel serverless)
    → Twilio SMS API
    → NOTIFICATION_PHONE receives text with all 6 fields
    → Form hidden, #form-success shown
```

On failure: submit button re-enabled, `#form-error` shown.

### 4.4 API contract

**Endpoint:** `POST /api/demo-request`  
**Content-Type:** `application/json`

**Request body:**
```json
{
  "name": "string",
  "email": "string",
  "shop": "string",
  "phone": "string",
  "employees": "string",
  "module": "string"
}
```

**Success:** `200 { "ok": true }`  
**Errors:** `400` missing fields, `405` wrong method, `500` missing env vars, `502` Twilio failure

**SMS format sent to owner:**
```
New Pulse demo request

Name: ...
Email: ...
Print shop: ...
Phone: ...
Employees: ...
Module: ...
```

---

## 5. Backend — `api/demo-request.js`

Vercel serverless function (Node.js, CommonJS).

- Uses `twilio` npm package
- Reads credentials from environment variables only
- CORS headers allow `*` (same-origin in production; useful for local testing)
- Handles `OPTIONS` preflight

### Required environment variables

| Variable | Description |
|---|---|
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TWILIO_PHONE_NUMBER` | Twilio sending number (E.164, e.g. `+17473185575`) |
| `NOTIFICATION_PHONE` | Owner phone that receives lead SMS (E.164, e.g. `+18189277146`) |

Copy `.env.example` → `.env` for local dev. Set the same four vars in **Vercel → Project → Settings → Environment Variables**.

### Legacy Netlify function

`netlify/functions/demo-request.js` is an older duplicate using Netlify's `exports.handler` format. **Production uses Vercel.** The frontend calls `/api/demo-request`, not `/.netlify/functions/demo-request`. Safe to delete Netlify files if Netlify is not used.

---

## 6. Frontend JavaScript

All JS is inline at the bottom of `index.html`.

### 6.1 Intersection Observer (animations)

- Selects all `.fade-up` elements
- Adds `.visible` class when scrolled into view (threshold 0.1)
- Staggered delay: `index * 60ms`
- CSS transition: opacity + translateY

### 6.2 `handleSubmit(e)`

- Prevents default form submit
- Disables button, shows "Sending…"
- Collects form fields by `name` attribute
- `fetch('/api/demo-request', { method: 'POST', ... })`
- Note: inline comment still mentions "Netlify function" — outdated; actual target is Vercel `/api/demo-request`

---

## 7. Design System (CSS variables)

Defined in `:root` at top of `<style>`:

| Variable | Value | Usage |
|---|---|---|
| `--bg` | `#06060e` | Main background |
| `--bg2` | `#0c0c18` | Alternate section background |
| `--bg3` | `#11111f` | Cards |
| `--border` | `rgba(255,255,255,0.07)` | Borders |
| `--blue` | `#4f6ef7` | Primary accent |
| `--blue-light` | `#7b93ff` | Secondary accent |
| `--cyan` | `#22d3ee` | Highlight accent |
| `--text` | `#f0f2ff` | Body text |
| `--muted` | `#8b90a8` | Secondary text |

**Font:** Inter (Google Fonts)  
**Favicon:** Inline SVG data URI, background color `#3237FF`  
**Brand icon:** Pulse waveform SVG (used in nav + footer)

### Responsive breakpoints

- `900px` — hero, modules, before/after layouts stack
- `600px` — CTA, process steps, footer
- `460px` — modules single column

---

## 8. Deployment

### 8.1 Vercel (production)

```bash
npm install
npx vercel deploy --prod
```

- Static files served from repo root (`index.html`, `images/`)
- `api/*.js` auto-deployed as serverless functions
- Env vars must be set in Vercel dashboard before SMS works
- After changing env vars, redeploy for functions to pick them up

### 8.2 Local development

```bash
npm install
cp .env.example .env   # fill in real Twilio values
npx vercel dev           # serves site + API locally
```

Test API directly:
```bash
curl -X POST http://localhost:3000/api/demo-request \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"t@e.com","shop":"Shop","phone":"555","employees":"1–5 employees","module":"Pulse CRM"}'
```

### 8.3 GitHub

Remote: `origin` → `https://github.com/zargaryandavid-BZ/Webiste.git`  
Branch: `main`

**Known issue:** `git push` may fail with `403 Permission denied` if local Git credentials don't match the `zargaryandavid-BZ` org account. Vercel CLI deploy works independently of GitHub push.

---

## 9. Dependencies

```json
{
  "dependencies": {
    "twilio": "^5.7.1"
  }
}
```

No devDependencies. No bundler. Twilio is only used by the serverless function.

---

## 10. Security Notes for AI Agents

1. **Never commit** `.env`, `.env.production`, `.env.vercel` — contain live Twilio secrets.
2. **Never put real credentials** in `.env.example` — placeholders only.
3. **Do not expose** `TWILIO_AUTH_TOKEN` in client-side code; it must stay server-side only.
4. Form has no rate limiting or CAPTCHA — consider adding if spam becomes an issue.
5. CORS is `*` on the API — acceptable for this use case but worth tightening if API is reused elsewhere.

---

## 11. Common Modification Tasks

| Task | Where to edit |
|---|---|
| Change hero text | `#home` section, `.hero-sub` paragraph |
| Change module copy/images | `#modules` section, `.mc` cards |
| Add/remove form field | Form in `#problem`, `handleSubmit()`, `api/demo-request.js`, SMS template |
| Change SMS recipient | `NOTIFICATION_PHONE` env var |
| Fix broken nav links | Nav + footer `<a href>` or add missing section IDs |
| Change brand colors | `:root` CSS variables |
| Change favicon color | `<link rel="icon">` SVG data URI, `fill='%23XXXXXX'` |
| Swap hero image | `images/` file + `<img src>` in `.hero-photo-layer` |
| Add new page | Not supported — single-page only; would need new HTML file or refactor |

---

## 12. Git History (summary)

| Commit | Description |
|---|---|
| Initial | Marketing website with images in `website photos/` |
| fa94858 | Vercel API for Twilio SMS, form wiring, favicon, hero updates |
| 9b7f731 | Fixed image paths — moved active assets to `images/` |

---

## 13. Quick Reference for AI Agents

**Before editing, know:**

1. This is a **monolithic static site** — most changes go in `index.html` only.
2. **Only one API route** — form SMS is the only dynamic behavior.
3. **Images must use `images/` paths** — not root, not `website photos/`.
4. **Nav anchors are partially broken** — see §3.2.
5. **Deploy target is Vercel**, not Netlify or GitHub Pages.
6. **Test SMS** requires valid Twilio env vars; API returns 500 without them.
7. **Do not commit secrets** or `.DS_Store`.
8. **No tests exist** — manual browser + curl testing only.

**Safe to delete (if cleaning up):** `netlify/`, `netlify.toml`, duplicate files in `website photos/` (after confirming `images/` has everything needed).

**Do not delete:** `api/demo-request.js`, `images/`, `index.html`, `package.json`.
