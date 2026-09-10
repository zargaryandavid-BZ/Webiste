# Pulse Website — Image Map & File Reference

All image files live in the root of the project folder alongside `index.html`.
A backup copy of every image is also in `/website photos/`.

---

## Images Currently Used in index.html

| File | Where Used | Section | Notes |
|------|-----------|---------|-------|
| `production-floor.jpg` | Hero section — left column background | `#home` `.hero-photo-layer` | Full-bleed photo behind the glass dashboard widget |
| `crm-operator.png` | Module card #01 | `#modules` `.mc-photo` | Female headset operator — Pulse CRM card |
| `hp-indigo-printer.webp` | Module card #02 | `#modules` `.mc-photo` | HP Indigo digital press — Pulse Design Manager card |
| `operator-printing-press.jpg` | Module card #03 | `#modules` `.mc-photo` | Man operating large-format printer — Pulse Production card |
| `crm-operator-2.jpeg` | Module card #04 | `#modules` `.mc-photo` | Male operator — Pulse HR card (placeholder, replace with shift/HR photo) |
| `broker-storefront.jpg` | Module card #05 | `#modules` `.mc-photo` | PrintPapa-style storefront screenshot — Broker Websites card |

---

## Images in Folder — NOT Yet Used in HTML (available to assign)

| File | Description | Best Use |
|------|-------------|----------|
| `crm-operator-2.jpeg` | Male call center operator with headset | Alternative for CRM card |
| `hp-indigo-printer.webp` | HP Indigo digital press | Alternative for Production card |
| `production-press.png` | Yellow-background printing machine | Alternative for Production card |
| `production-hp-printer.png` | HP digital printer close-up | Alternative for Production card |
| `broker-website.webp` | Print website screenshot | Alternative for Broker Websites card |
| `broker-website-storefront.jpg` | Another storefront screenshot | Alternative for Broker Websites card |
| `scodix-ultra-6500.jpg` | Scodix Ultra 6500 SHD machine (white bg) | Could be used in a tech/equipment section |

---

## Module Cards Still Using Unsplash URLs (need local replacements)

| Module | Current src | Suggested local replacement |
|--------|------------|----------------------------|
| Pulse Design Manager (#02) | `https://images.unsplash.com/photo-1561070791-2526d30994b5` | Need a graphic designer / artwork photo |
| Pulse HR (#04) | `https://images.unsplash.com/photo-1612831455359-970e23a1e4e9` | Need a clock-in / shift management photo |

> ⚠️ Unsplash URLs can break. Replace with local files when available.

---

## Hero Section Layout (index.html `#home`)

```
┌──────────────────────────────────────────────────────────┐
│  LEFT COLUMN (.hero-visual)          RIGHT COLUMN        │
│  ┌────────────────────────────────┐  (.hero-content)     │
│  │  production-floor.jpg          │                      │
│  │  (full bleed, brightness 100%) │  "No Mess in the     │
│  │  ┌──────────────────┐          │   Printing House."   │
│  │  │ Glass dashboard  │          │                      │
│  │  │ (top-left, 220px │          │  [Request a Demo]    │
│  │  │  backdrop-blur)  │          │  [See the Platform]  │
│  │  └──────────────────┘          │                      │
│  └────────────────────────────────┘                      │
└──────────────────────────────────────────────────────────┘
```

---

## Module Cards Layout (index.html `#modules`)

5-column CSS grid. Each card has:
- Top photo (200px height, `object-fit: cover`, `brightness(0.85)`)
- Blue icon badge (`background: var(--blue)`) bottom-left of photo
- Card number, title, description, feature list

```
[ 01 Pulse CRM ]  [ 02 Design Mgr ]  [ 03 Production ]  [ 04 Pulse HR ]  [ 05 Broker Sites ]
crm-operator.png   Unsplash URL       operator-printing   Unsplash URL     broker-storefront.jpg
                   ⚠️ needs local     -press.jpg          ⚠️ needs local
```

---

## Color Palette (CSS variables)

```css
--bg:         #06060e   /* page background */
--bg2:        #0c0c18   /* section alternate */
--bg3:        #11111f   /* cards */
--blue:       #4f6ef7   /* primary / icons */
--blue-light: #7b93ff
--cyan:       #22d3ee   /* accent */
--text:       #f0f2ff
--muted:      #8b90a8
```
