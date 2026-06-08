# Emails de Outreach — ADA-AUDITS | Junio 2026
## Archivo auxiliar para copy-paste rápido

---

## 1. LEMON CASH (lemon.me)

**To:** soporte@lemon.me
**Subject:** Accessibility gaps on lemon.me — free 1-page audit inside

Hi Lemon Cash team,

I ran a quick WCAG 2.1 accessibility scan on lemon.me and found a few issues that could expose you to legal risk — especially given your 4M+ user base and the growing ADA compliance wave in financial services.

Here's what I spotted:

1. **Duplicated DOM content** — Footer and legal disclaimers render 4x in the page source, confusing screen readers and inflating your accessibility score artificially.
2. **No skip-navigation links** — Keyboard-only users must tab through the entire navigation on every page load before reaching content.
3. **FAQ sections lack ARIA semantics** — Your expanding FAQ items have no `aria-expanded` or accordion roles, making them unusable for assistive tech users.

I put together a **free 1-page accessibility snapshot** for lemon.me with severity ratings and fix recommendations. Want me to send it over?

We're Ranuk IT Solutions — we help fintech companies ship WCAG 2.1 AA-compliant experiences before they become liability targets. Our audits cover contrast, keyboard nav, screen reader compatibility, ARIA, and mobile accessibility.

Happy to run the full scan on your dime.

Best,
Emilio Ranucoli
Ranuk IT Solutions — Accessibility & Web Performance
emilio@ranuk.dev | ranuk.dev/ada-audits

---

## 2. COCOS CAPITAL (cocos.capital)

**To:** hola@cocos.capital
**Subject:** Cocos Accessibility Audit — 3 issues blocking WCAG 2.1 compliance

Hola Cocos team,

Your platform handles real money — so your accessibility game needs to be bulletproof. I analyzed cocos.capital against WCAG 2.1 AA standards and found 3 issues your team should know about:

1. **Dynamic pricing data lacks ARIA live regions** — Stock prices (GOOG, AAPL, CEDEARs) update in real-time but screen readers can't announce changes. Users relying on assistive tech literally can't see live market data.
2. **Dollar purchase widget missing input labels** — The "Comprá dólares" widget uses placeholder text instead of proper `<label>` associations. Screen readers announce "edit text" with no context.
3. **Mega-menu navigation lacks ARIA roles** — Multi-level menus (Inversiones > Productos) don't use `aria-expanded`, `aria-haspopup`, or proper menu roles — keyboard navigation breaks at level 2+.

With +1M active users, these aren't just nice-to-haves — they're compliance gaps that affect real people and create legal exposure under Argentina's emerging digital accessibility regulations.

I'm Emilio from **Ranuk IT Solutions**. We specialize in accessibility audits for financial platforms. I've prepared a **complimentary 1-page WCAG snapshot** for cocos.capital — just say the word and I'll send it.

Talk soon,
Emilio Ranucoli
Ranuk IT Solutions
emilio@ranuk.dev | ranuk.dev/ada-audits

---

## 3. BELO (belo.app)

**To:** hello@belo.app
**Subject:** belo.app — I found 3 accessibility issues in 5 minutes (free audit)

Hi Belo team,

I was checking out belo.app and noticed 3 accessibility issues that could be blocking 15% of your potential users (that's the % of people globally who use assistive technologies).

Here's what I found:

1. **Repeated DOM blocks** — The hero section and benefit cards render 3-4 times in the source for responsive breakpoints. Screen readers crawl through all of them, creating a terrible experience and broken content flow.
2. **Emoji-dependent information** — Emojis like earth, beach and boat carry semantic meaning (countries, travel, payments) but lack `aria-label` or text alternatives. A screen reader just says "earth emoji" — meaningless.
3. **Testimonials lack semantic structure** — Your user reviews (Marcela, Leo, jm, Luciano) are plain text without `<blockquote>`, `<cite>`, or review schema — screen readers can't distinguish a testimonial from body copy.

Belo has 3M+ users across LatAm. Making your site accessible isn't just ethical — it's good business. Accessible fintech products have measurably higher conversion rates.

I'm Emilio from **Ranuk IT Solutions**. I've prepared a **free 1-page WCAG 2.1 audit snapshot** for belo.app with specific fixes. Want me to send it over?

Saludos,
Emilio Ranucoli
Ranuk IT Solutions — Web Accessibility & Performance
emilio@ranuk.dev | ranuk.dev/ada-audits
