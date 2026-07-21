# Snoots Brand Guidelines

Living reference for the Snoots website (joinsnoots.com / snootsvet.com). Mirrors the tokens in `src/styles.css` and the component patterns used across the codebase. If you change a token here, change it there too.

---

## 1. Brand voice

- **Plain-spoken, warm, a bit cheeky.** We're a vet clinic, not a hospital chain. Talk like a smart friend who happens to be a vet.
- **No jargon, no fear-selling.** Never frame care around what could go wrong if you don't buy. Frame it around what your pet gets.
- **Confident about the model.** Unlimited primary care, flat monthly fee, no copays, no surprise bills. Say it plainly and repeatedly.
- **British/American split.** UK site (snootsvet.com) uses UK spelling and £. US site (joinsnoots.com) uses US spelling and $. Never mix on one page.
- **Avoid:** "fur babies", "pawsome", emoji-heavy copy, exclamation points stacked more than one at a time.

---

## 2. Logo

- Primary asset: `src/assets/snoots-logo.png`
- On dark backgrounds, invert with `filter: invert(1)` (see `Footer.tsx`).
- Minimum height: 32px. Default footer height: 48px.
- Never recolor, stretch, add a drop shadow, or place on a busy photo without a solid backing.

---

## 3. Color palette

All colors are defined as CSS variables in `src/styles.css` under `:root`. Use the variables — never hardcode hex in components.

### Core brand

| Token         | Hex       | Variable        | Use                                              |
| ------------- | --------- | --------------- | ------------------------------------------------ |
| Black         | `#000000` | `--black`       | Primary text, primary buttons, nav               |
| White         | `#FFFFFF` | `--white`       | Default page background                          |
| Yellow        | `#FBCA01` | `--yellow`      | **Hero accent.** Button hover, underlines, highlights |
| Blue          | `#066AC8` | `--blue`        | Ticker bar, links-in-context, secondary accent   |
| Green         | `#04B95C` | `--green`       | Success / "included" ticks                       |
| Orange        | `#FC9002` | `--orange`      | Coming-soon asterisk, tertiary accent            |
| Baby Blue     | `#ABDAF4` | `--baby-blue`   | Soft section backgrounds                         |
| Baby Pink     | `#FFC8DB` | `--baby-pink`   | Soft section backgrounds                         |
| Emergency Red | `#FF3B30` | (inline)        | Out-of-hours emergency callouts only             |

### Usage rules

- **Yellow is the signature.** Use it sparingly and decisively — one big yellow moment per section beats yellow everywhere.
- **Black + white is the base.** Brand colors are accents, not the structure.
- **Never** use Tailwind utility colors like `text-purple-500`, `bg-indigo-600`, etc. Stick to the tokens above.
- **Never** stack baby blue and baby pink in the same fold.

---

## 4. Typography

Two families, loaded locally. Never @import remote font CSS — load via `<link>` in `__root.tsx` if a new face is added.

### Display — `Barlow Condensed`

- Weight: `800` (extra bold), always.
- Style: `text-transform: uppercase`, `letter-spacing: 0.01em`.
- Used for: all H1–H6, `.font-display`, buttons (`.btn-snoots`), nav, ticker.
- CSS variable: `--font-display`.

### Body — `Aktiv Grotesk`

- Weights shipped: 400, 500, 700 (regular + italic for each).
- Used for: paragraphs, lists, form fields, captions.
- Fallback stack: `"Aktiv Grotesk", "Helvetica Neue", Arial, sans-serif`.
- CSS variable: `--font-sans`.

### Scale (mobile-aware — see `styles.css` media queries)

| Role             | Desktop                  | Mobile cap                   |
| ---------------- | ------------------------ | ---------------------------- |
| Hero H1          | 88–120px                 | `clamp(48px, 14vw, 88px)`    |
| Page H1          | 56–72px                  | `clamp(40px, 11vw, 56px)`    |
| Section H2       | 32–40px                  | scales down                  |
| Sub-headline     | 22–28px                  | `clamp(18px, 5vw, 26px)`     |
| Body             | 16–18px                  | 16px                         |
| Footer / legal   | 13–14px, `0.08em` track  | same                         |

---

## 5. Buttons

Defined as `.btn-snoots` + a variant in `styles.css`. Always pill-shaped (`border-radius: 999px`), uppercase Barlow Condensed 800.

| Variant          | Resting                       | Hover                                |
| ---------------- | ----------------------------- | ------------------------------------ |
| `.btn-primary`   | Black bg, white text          | Yellow bg, black text                |
| `.btn-secondary` | White bg, black border + text | Yellow bg, black border + text       |
| `.btn-amber`     | Yellow bg, black text         | Yellow bg, black text (no change)    |

- On mobile (≤480px) buttons shrink to 13px / 18px padding automatically.
- CTAs stack full-width on mobile.
- One primary CTA per screen-fold. Never two black buttons next to each other.

---

## 6. Layout & spacing

- **Max content width:** `1400px` (footer, nav, most page shells).
- **Default section padding:** `80px 24px` desktop, `48px 24px` mobile.
- **Grid gap default:** `24px` (3 cards), `40px` (4-col footer).
- **Border radius:** `0.625rem` base (`--radius`). Buttons override to fully pill.
- **Mobile breakpoints:** `≤480px` (small phone tweaks), `≤768px` (mobile), `768px–1100px` (tablet hero fixes).

---

## 7. Components

| Component               | File                                     | Notes                                               |
| ----------------------- | ---------------------------------------- | --------------------------------------------------- |
| Ticker bar              | `src/components/TickerBar.tsx`           | Blue bg, white display type, 30s scroll loop        |
| Top nav                 | `src/components/Nav.tsx`                 | Fixed, white, black text. Mobile: flush to top      |
| Footer                  | `src/components/Footer.tsx`              | Black bg, 4-col grid, yellow "AS FEATURED IN" strip |
| Site shell              | `src/components/SiteShell.tsx`           | Nav + Footer wrapper. Currently US-only mode        |
| Blog prose              | `.snoots-prose` in `styles.css`          | H2 gets a 56×6 yellow underline bar                 |
| Underline word          | `src/components/UnderlineWord.tsx`       | Hand-drawn blue underline accent for hero copy      |
| Comparison tables       | `ComparisonTable.tsx`, `Tiered…tsx`      | Yellow header row, green ticks                      |

---

## 8. Imagery

- **Real photography only.** Stock photos of real dogs, cats, and people in lifestyle contexts.
- **Never** AI-generated, illustrated, or 3D-rendered pet imagery. This is a hard rule.
- Prefer warm natural light, shallow depth of field. Avoid clinical/sterile vet-photo clichés (gloved hands, stethoscopes on white).
- Hero photos sit inside rounded-corner cards on desktop, full-width crops on mobile.

---

## 9. Iconography

- Library: `lucide-react` (already installed via shadcn).
- Stroke width: default (`2`).
- Color: inherits `currentColor` — never hardcode.
- For "coming soon" use the orange asterisk component (`src/components/us/ComingSoon.tsx`), not an icon.

---

## 10. Motion

- Library: `framer-motion` where animation is non-trivial; CSS for simple cases.
- Ticker scroll: 30s linear infinite.
- Button transitions: `200ms ease` on bg / color / border only.
- Default to subtle. One hero animation per page; no scattered micro-interactions.

---

## 11. Accessibility & SEO

- Single `<h1>` per route. Subsequent sections use `<h2>` / `<h3>`.
- All images need meaningful `alt` text. Decorative images: `alt=""`.
- External links: `target="_blank"` **and** `rel="noopener noreferrer"`.
- Per-route `head()` with unique `title` (<60 chars) and `meta description` (<160 chars). Never reuse the home page's metadata.
- Canonical URL on every page.
- Color contrast: black-on-yellow and white-on-black are the safe pairings. Avoid white-on-yellow or black-on-blue body text.

---

## 12. Regional config

The codebase is currently in **US-only mode** (`US_ONLY_MODE = true` in `SiteShell`, `Nav`, `TickerBar`). UK code paths are preserved verbatim — to restore the UK site, flip the flags listed in `src/router.tsx`'s header comment. Do not delete UK strings, routes, or assets.

| Locale | Domain           | Currency | Ticker copy                                                                |
| ------ | ---------------- | -------- | -------------------------------------------------------------------------- |
| US     | joinsnoots.com   | USD ($)  | `ALWAYS UNLIMITED · NO COPAYS · NO SURPRISE BILLS · REAL VETS · AFFORDABLE CARE` |
| UK     | snootsvet.com    | GBP (£)  | `NO EXCESSES. · NO SURPRISES. · ALWAYS UNLIMITED.`                          |

---

## 13. What we don't do

- No purple/indigo gradients on white.
- No generic "modern SaaS" hero (centered headline + two CTAs + dashboard screenshot).
- No Inter, Poppins, Roboto, or any other default Google sans.
- No emoji in headlines or CTAs.
- No fear-based copy ("Don't let this happen to your pet…").
- No three-letter acronyms the customer doesn't already know.
- No AI pet imagery. Ever.

---

_Last updated: June 2026. Source of truth for tokens: `src/styles.css`._
