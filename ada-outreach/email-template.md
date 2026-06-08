# Ranuk IT — ADA Outreach Email Template

> **Service:** Automated WCAG 2.1 Accessibility Audit + Remediation
> **Sender:** Emilio Ranucoli — emilio@ranuk.dev
> **Landing:** https://ranuk.dev
> **Last updated:** 2026-06-03

---

## Subject Line Options

Pick one based on tone and audience. A/B test across batches.

1. **Direct / Urgency:**
   `{{company_name}}, your site has {{issue_count}} accessibility issues — free audit inside`

2. **Value-first / Curiosity:**
   `Quick audit of {{company_name}} — found a few things worth fixing`

3. **Social Proof / Trust:**
   `How 100+ businesses avoided ADA lawsuits ({{company_name}} audit attached)`

---

## Initial Outreach Email

```
Subject: {{subject_line_variant}}

Hi {{contact_first_name}},

I ran an automated WCAG 2.1 accessibility audit on {{company_name}}'s public website and found {{issue_count}} issues — including {{critical_count}} critical ones that could trigger an ADA compliance risk.

Quick summary of what the scan caught:

{{pain_point}}

Most of these are fixable in under a week. We've helped 100+ US businesses go from non-compliant to fully accessible (WCAG 2.1 AA) — for a flat $1,200, no surprises.

Here's what you'd get with a free audit:

• Automated scan of your entire public site (every page, every element)
• Top 10 accessibility issues ranked by severity
• Compliance risk score (0–100)
• Prioritized remediation roadmap with WCAG criterion references
• Delivered to your inbox within 48 hours

No commitment, no credit card — just a clear picture of where {{company_name}} stands.

If you'd like the full report, just reply with your preferred email and I'll send it over. Or if you'd rather talk it through, book a 15-minute call here: {{calendly_link}}

Talk soon,
Emilio Ranucoli
Ranuk IT Solutions
emilio@ranuk.dev | https://ranuk.dev
```

---

## Personalization Guide

| Placeholder | Description | Example |
|---|---|---|
| `{{company_name}}` | Prospect's company name | "Sundds Dental" |
| `{{contact_first_name}}` | Decision-maker's first name | "Sarah" |
| `{{issue_count}}` | Total issues found in scan | "23" |
| `{{critical_count}}` | Critical/high-severity issues | "4" |
| `{{pain_point}}` | Most relevant finding (1-2 sentences) | "Missing form labels on your appointment booking page — screen readers can't navigate it at all." |
| `{{subject_line_variant}}` | One of the 3 subject lines above | See above |
| `{{calendly_link}}` | Calendly or scheduling link | "https://calendly.com/ranukit/15min" |

### Pain Point Examples (by industry)

**Dental / Medical:**
- "Missing alt text on all patient testimonial images — 42% of your visual content is invisible to assistive technology."
- "Forms without labels on your appointment booking page — screen readers can't navigate it."
- "Color contrast failures across your services section — 15 elements below WCAG AA threshold."

**E-Commerce:**
- "Product images without alt attributes — your entire catalog is inaccessible to visually impaired users."
- "Keyboard navigation traps in your checkout flow — users can't complete a purchase without a mouse."
- "Missing ARIA labels on all filter and sort controls."

**SaaS / Tech:**
- "Modal dialogs without focus trapping — keyboard users get lost in your UI."
- "Your login form has no error identification via ARIA — screen reader users can't see validation messages."
- "Dashboard charts have no text alternatives — data is completely inaccessible."

---

## Quick Stats Block (paste into email when relevant)

```
📊 ADA Litigation Stats:
• 4,000+ web accessibility lawsuits filed in 2024 (up 30% YoY)
• Average settlement: $50,000–$150,000
• 96% of home pages have WCAG 2 failures (WebAIM 2024)
• Small businesses are the #1 target — 77% of lawsuits
```
