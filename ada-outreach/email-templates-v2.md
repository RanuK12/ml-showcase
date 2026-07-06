# ADA Outreach — Templates v2 (2026-07-06)

> Reemplazan a `email-template.md` / `followup-template.md` (v1, retirados del uso).
> Reglas duras: texto plano (sin HTML decorado), **nombre real del destinatario o no se envía**,
> **PDF de auditoría real adjunto** (T1 y T3), cero claims no verificables, máx 120 palabras el cuerpo.
> Variables: solo las que el pipeline puede llenar con datos REALES del scan.

---

## T1 — US directo, auditoría real adjunta

**Para:** negocios US medianos (con web activa que venda/agende online). NO micronegocios, NO Fortune 500.
**Subjects (A/B):**
- A: `quick accessibility question about {{domain}}`
- B: `{{first_name}}, found this on {{domain}}`

```
Hi {{first_name}},

I ran an accessibility scan on {{domain}} before writing this — the full
report is attached (2 pages, no signup, it's yours either way).

The one thing I'd fix first: {{finding}}. It affects real users
(screen readers can't get past it) and it's the kind of issue that shows
up in ADA web lawsuits — there were 4,000+ of them last year.

I'm Emilio, a software engineer (ex-Booking.com). I fix these for a flat
fee, most sites in under 2 weeks.

Worth a 15-minute call? If not, the report still tells your web person
exactly what to fix.

Emilio Ranucoli
Ranuk IT — emilio@ranuk.dev
```

**Follow-up único (día +6), solo si abrió el email o el PDF:**
```
Subject: Re: {{original_subject}}

Hi {{first_name}} — did the report make it to the right person?

If accessibility isn't a priority right now, no problem. One free fix
from the report you can do today: {{quick_win}}.

Emilio
```

---

## T2 — Agencias de diseño web (reseller / white-label)

**Para:** agencias y estudios web US con portfolio de clientes visible. Acá el decisor entiende el tema.
**Subjects (A/B):**
- A: `accessibility audits for your client sites`
- B: `white-label WCAG audits (you keep the margin)`

```
Hi {{first_name}},

I looked at a few sites in {{agency_name}}'s portfolio — nice work.
I also noticed most of them would fail a WCAG 2.1 AA check, which is
normal (96% of the web does) but increasingly a liability for their
owners: ADA web lawsuits keep climbing and small businesses are the
usual target.

I do the technical side — automated + manual audit, remediation
roadmap, WCAG references — as a white-label service. You present it
under your brand, price it however you want, I stay invisible.

One audit of any site in your portfolio, free, so you can judge the
quality. Which one should I run it on?

Emilio Ranucoli
Software engineer, ex-Booking.com — emilio@ranuk.dev
```

**Follow-up único (día +6):**
```
Subject: Re: {{original_subject}}

Hi {{first_name}} — offer stands: one free audit on any client site,
white-label, you see exactly what your clients would get.

If it's not a fit for {{agency_name}}, tell me and I won't follow up again.

Emilio
```

---

## T3 — Vertical bajo litigio activo (dental / e-commerce US)

**Para:** verticales US con demandas ADA documentadas y recientes. El dato de litigio debe ser REAL y citable
(fuente: registros públicos de demandas ADA Title III / reportes UsableNet-Seyfarth del año en curso).
**Subjects (A/B):**
- A: `ADA lawsuits hitting {{industry}} sites — where {{domain}} stands`
- B: `{{first_name}}, {{industry}} is getting sued over websites`

```
Hi {{first_name}},

{{lawsuit_fact}} — e.g. "Over 300 e-commerce sites were hit with ADA
web lawsuits in Q1 this year; most settled for $20-50k."

I'm not a lawyer and this isn't a scare pitch: I ran an actual WCAG
scan on {{domain}} (attached) so you can see where you stand instead
of guessing. Current state: {{issue_count}} issues, {{critical_count}}
of them the kind that show up in these cases.

I'm a software engineer and I fix exactly this — flat fee, about two
weeks, retest included.

Want me to walk you through the report? 15 minutes, no obligation.

Emilio Ranucoli
Ranuk IT — emilio@ranuk.dev
```

**Follow-up único (día +6):**
```
Subject: Re: {{original_subject}}

Hi {{first_name}} — quick close on this. The report I sent is current
for about 90 days; after that a rescan makes sense either way.

If you want the fixes done, I have room for one more {{industry}}
project this month. If not, the roadmap in the PDF is enough for any
competent developer to work through.

Emilio
```

---

## Reglas de envío (aplican a los 3)

1. **Cadencia:** 1 follow-up máximo, día +6. Después, muere. (v1 hacía 3 toques a buzones muertos.)
2. **Volumen:** 20-25/semana total. El cuello de botella es generar la auditoría real, y así debe ser.
3. **Nunca:** `info@`/`ventas@`, empresas >200 empleados, leads fuera de US para pitch ADA, claims sin fuente.
4. **Variables `{{finding}}` / `{{quick_win}}` / `{{lawsuit_fact}}`:** salen del scan real o de una fuente citable. Si el pipeline no las puede llenar, el email no sale.
5. **Firma corta**: sin lista de certificaciones ni "Fortune 500". Un cargo real y un mail.
6. **Unsubscribe:** respetar "remove" en el día, marcar `unsubscribed` en CRM (ya soportado).
