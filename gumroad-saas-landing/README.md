# SaaS Starter Kit — Landing Page

A professional, high-converting landing page for selling the **SaaS Starter Kit** on Gumroad. Built with the Ranuk brand identity (dark theme, cyan/gold accents).

## Preview

Open `index.html` in your browser to preview:
```bash
open index.html
```

## Deploy to Gumroad

1. Zip the entire folder (index.html + styles.css + assets/)
2. Upload to Gumroad as a digital product
3. Set price to **$29**
4. Use the page URL as your product landing page
5. Alternatively, host on Netlify/Vercel for a custom URL

## Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
  --bg: #1a1a2e;        /* Main background */
  --bg-light: #16213e;  /* Section alternating bg */
  --bg-card: #0f3460;   /* Card background */
  --cyan: #00d4ff;      /* Primary accent */
  --gold: #ffd700;      /* Secondary accent */
}
```

### Content
- **Hero**: Edit `hero.html`
- **Features**: Edit `features.html`
- **Pricing**: Edit `pricing.html`
- **Testimonials**: Edit `testimonials.html`
- **FAQ**: Edit `faq.html`

### Logo
Replace `assets/ranukita-logo.png` with your own logo.

## Tech Stack

- Single HTML file + CSS (no build step)
- Google Fonts (Inter)
- Vanilla JavaScript (FAQ accordion, navbar scroll)
- Fully mobile responsive
- Optimized for conversion

## Sections

1. **Navbar** — Fixed with backdrop blur, mobile hamburger menu
2. **Hero** — Problem/solution headline, social proof stats
3. **Problem** — 3 pain point cards
4. **Features** — 6 product feature cards
5. **Pricing** — Single $29 card with checklist
6. **Testimonials** — 3 customer reviews with ratings
7. **FAQ** — 5 accordion items
8. **CTA** — Final conversion section
9. **Footer** — Branding and links

## Files

```
gumroad-saas-landing/
├── index.html          # Main landing page (assembled)
├── styles.css          # All styles (Ranuk brand)
├── assets/
│   └── ranukita-logo.png
├── assemble.py         # Build script
├── head.html           # HTML head
├── nav.html            # Navbar
├── hero.html           # Hero section
├── problem.html        # Problem section
├── features.html       # Features section
├── pricing.html        # Pricing section
├── testimonials.html   # Testimonials section
├── faq.html            # FAQ section
├── cta.html            # CTA + Footer
├── scripts.html        # JavaScript
└── README.md           # This file
```

## Built by

**Ranuk IT Solutions** — [ranuk.dev](https://ranuk.dev)
