# Diagnóstico brutal — ADA Outreach (2026-07-06)

> Datos: `~/.ranukita/ada_outreach/crm.json` (816 leads, envíos 2026-06-17 → 2026-07-06),
> `Ranuk-Outreach/envios_email/*.json` (campaña LATAM previa, 165+165),
> DNS de ranuk.dev verificado hoy.

## Números reales

| Métrica | Valor |
|---|---|
| Leads contactados | 806 de 816 (601 con follow-up, touches hasta 3) |
| Respuestas | 4 (0.5%) |
| Respuestas humanas reales | **0** — las 4 son `help@warbyparker.com`, `press@google.com`, `faleconosco@smartfit.com`, `farmamacedonio@gmail.com` (autoresponders) |
| Unsubscribes | 1 |
| Benchmark mínimo cold B2B | reply rate 3% (esperado acá: ~24 respuestas) |

## Veredicto: no es UN problema, son cinco apilados

### 1. Targeting — el peor de todos
- **473/816 (58%) son casillas genéricas** (`info@`, `contacto@`, `ventas@`, `hello@`). Nadie es dueño de ese mail; el que lo abre no decide ni le importa.
- La lista tiene **google.com, warbyparker.com, bnpparibas.es, smartfit.com** — corporaciones con equipos legales y de accesibilidad propios. Eso es scraping sin filtro, no prospección. Un `press@google.com` en la lista es la prueba de que nadie miró los leads antes de enviar.
- Tipos: peluquerías (57), restaurantes (52), hoteles (52), gimnasios (53)... **micronegocios locales sin presupuesto de $899-$2999 para accesibilidad web** y sin percepción de riesgo legal.

### 2. Mercado — 78% de la lista no está sujeta a ADA
- ADA es ley **de Estados Unidos**. La lista: ES 255 + IT 244 + AR 138 = **637/816 leads a los que el pitch legal no les aplica**. Un dentista de Madrid no puede ser demandado bajo ADA, punto.
- (El ángulo correcto para EU existe — el **European Accessibility Act entró en vigor en junio 2025** — pero los templates nunca lo mencionan. Se les vendió miedo a la ley equivocada.)
- 4 países × 3 idiomas a la vez = ningún mensaje afinado para nadie.

### 3. Oferta — claims falsos que queman el dominio
- "We've helped **100+ US businesses**" — falso, 0 clientes. Un prospect que googlea "Ranuk IT accessibility" no encuentra ni un caso.
- "({{company_name}} audit **attached**)" — no hay ningún PDF adjunto. Promesa rota en el subject.
- Subject actual: **"¿lo viste?" / "l'ha vista?"** (301 + 165 envíos). Es el clickbait más quemado del cold email; grita spam y entrena a Gmail para mandar todo lo de ranuk.dev a spam.

### 4. Volumen sobre calidad
- 800+ emails genéricos, **0 auditorías reales adjuntas**, cadencia de 3 toques a buzones muertos. La campaña LATAM previa: 134/165 con subject casi idéntico ("Ex-Booking.com · 10 minutos sobre seguridad X") — patrón perfecto para filtros.
- Un solo mailbox (`emilio@ranuk.dev`) en el **dominio primario del negocio**. Si se quema, se quema ranuk.dev entero (incluye el mail personal de trabajo).

### 5. Deliverability — DNS bien, reputación tocada
- SPF ✅, DKIM ✅, DMARC ✅ pero `p=none` (no protege, solo reporta).
- Memoria del sistema registra **rebotes en tandas ADA** = la reputación ya acusó el golpe.
- Sin dominio secundario de envío, sin warmup escalonado real (806 leads en 19 días).

## Estrategia nueva (lo que sí)

**Principio: 20 emails/semana con auditoría PDF real adjunta > 700 genéricos.**

1. **Solo US** para el pitch ADA (179 leads ya en CRM, filtrar micronegocios y corporaciones). EU queda para una campaña EAA aparte, después.
2. **Auditoría real ANTES de escribir**: correr el AuditBot sobre el sitio, generar PDF de 2-3 páginas con hallazgos concretos, adjuntarlo. El email cita 1 hallazgo específico; el PDF prueba el resto.
3. **Nombre real o no se envía**: buscar decisor (owner/marketing) en el sitio o LinkedIn. Cero `info@`.
4. **Segundo canal: agencias de diseño web** (template 2). Una agencia con 30 clientes es 30 auditorías potenciales white-label; entienden el problema sin que se lo expliques.
5. **Cero claims inventados**: sin "100+ businesses", sin urgencia falsa. Texto plano, corto, con un dato verificable.
6. **Higiene**: comprar dominio de envío secundario (ej. `ranukaudits.com`), warmup 2-3 semanas, máx 20-25/semana por mailbox. DMARC del primario a `p=quarantine` cuando dejen de salir campañas desde ahí.

## Plan A/B — 2 semanas

Celdas chicas pero medibles. Métrica de éxito: **reply rate > 3%** (respuestas humanas, no autoresponders — el lector Gmail OAuth ya distingue rebotes).

**Semana 1 (~45 emails):**
| Celda | Template | Subject | n |
|---|---|---|---|
| A1 | T1 US directo + PDF real | `quick accessibility question about {{domain}}` | 12 |
| A2 | T1 US directo + PDF real | `{{first_name}}, found this on {{domain}}` | 12 |
| B1 | T2 agencias | `accessibility audits for your client sites` | 12 |
| B2 | T2 agencias | `white-label WCAG audits (you keep the margin)` | 9 |

**Semana 2 (~45 emails):** se mata la peor celda de cada par, se agrega T3 (vertical con litigios: dental/e-commerce US) con 2 subjects, mismo tamaño de celda.

**Registro**: columna `template` y `subject_variant` en el CRM; medir replies humanas a los 5 días de cada tanda. Si tras 2 semanas hay 0 respuestas con auditorías reales adjuntas y nombres reales, el problema es la oferta o el precio — recién ahí se pivotea (LinkedIn DMs, o bajar a $499 entry).

## PDF de auditoría automatizado — YA EXISTE (verificado 2026-07-06)

No hay que construir nada: `ADA-AUDITS/scripts/audit-pipeline.py <url> --company "X"` hace URL → scan axe-core (WCAG 2.1 AA) → score 0-100 → PDF con marca en `ADA-AUDITS/entregables/<dominio>/`. Probado contra ranuk.dev: PDF de 124KB con score, top 3, tabla de cumplimiento y fases de remediación. Dependencias instaladas (axe CLI + weasyprint).

1. Flujo por lead: correr el pipeline → tomar el hallazgo #1 del `resumen-scan.json` como `{{finding}}` del template → adjuntar el PDF. Email y adjunto siempre coinciden.
2. Lista de arranque: `~/.ranukita/ada_outreach/leads_us_curados.json` (105 leads US filtrados, 24 con email de persona — esos primero).
3. Límite: 20-25/semana. El PDF es el diferenciador; si se industrializa a 700/semana se vuelve el mismo spam con peso extra.
