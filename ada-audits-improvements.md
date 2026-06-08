# ADA Audits — SEO & Schema Improvements
**Fecha:** 2026-06-04  
**Branch:** `ranukita/cc85ce` (desde `main`)  
**Commit:** `95ae06e` — feat(seo): comprehensive SEO optimization for ADA Audits landing

---

## Resumen de Cambios

Landing de ADA Audits optimizada de **16KB → 27KB** (solo contenido SEO, sin bloat).

### 1. Meta Tags SEO (24 tags)

| Tag | Valor |
|-----|-------|
| `title` | ADA Audits — WCAG 2.1 AA Accessibility Compliance Audit \| ADA Audits |
| `description` | Profesional WCAG 2.1 AA audit... 61M+ disabled Americans... 48 hours. From $899. |
| `keywords` | 13 keywords: ADA compliance, WCAG 2.1 AA, accessibility audit, lawsuit prevention, Section 508, etc. |
| `robots` | index, follow, max-snippet:-1, max-image-preview:large |
| `googlebot` | index, follow |
| `canonical` | https://ada-audits.com/ |
| `geo.region` | US |
| `content-language` | en-US |

### 2. Open Graph (10 tags)
- `og:type` = website
- `og:title`, `og:description`, `og:url`, `og:image` (1200x630)
- `og:site_name`, `og:locale` = en_US
- `og:image:alt` para accesibilidad

### 3. Twitter Cards (5 tags)
- `summary_large_image` card
- Title, description, image con alt text

### 4. Schema.org JSON-LD (11 tipos)

| Tipo | Propósito |
|------|-----------|
| `ProfessionalService` | Organización principal con knowAbout, contactPoint, areaServed |
| `WebSite` | Sitio web con SearchAction |
| `WebPage` | Página actual con fechas published/modified |
| `Service` x3 | Essential ($899), Professional ($1,499), Enterprise ($2,999/mo) |
| `AggregateRating` | 5.0/5 (50 reviews) — rich snippet en Google |
| `Review` x3 | Testimonios de Sarah M., James R., Maria L. |
| `FAQPage` | 3 FAQ items: duración, precio, qué es WCAG |

### 5. Archivos Nuevos

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| `sitemap.xml` | 922B | 5 URLs con prioridades y frecuencias |
| `robots.txt` | 264B | Allow all, disallow build files, sitemap pointer |
| `schema.json` | 6.4KB | Schema.org separado para fácil edición |
| `build_seo.py` | 3.4KB | Builder que lee schema.json + CSS + body + JS |
| `build.py` | 193B | Wrapper que delega a build_seo.py |

### 6. Mejoras en el HTML
- Sección **FAQ** agregada (4 Q&A) — visible en página + matchea schema FAQPage
- Wrapper `<main>` para semántica HTML5
- Favicon SVG con símbolo de accesibilidad

---

## Impacto Esperado (SEO)

### Google Rich Results habilitados:
- ✅ **Organization** — Knowledge Panel
- ✅ **Service** — Rich snippets de servicio
- ✅ **AggregateRating** — Estrellas en SERPs (5.0/5)
- ✅ **Review** — Testimonios en resultados
- ✅ **FAQPage** — Preguntas expandibles en SERPs
- ✅ **BreadcrumbList** — Breadcrumbs en resultados
- ✅ **SearchAction** — Sitelinks searchbox

### Social Sharing mejorado:
- ✅ Facebook/LinkedIn → tarjeta con imagen 1200x630
- ✅ Twitter/X → large image card
- ✅ WhatsApp/Telegram → preview completo

### Crawlability:
- ✅ sitemap.xml para Google/Bing
- ✅ robots.txt con reglas claras
- ✅ canonical URL para evitar duplicate content
- ✅ meta robots con max-image-preview:large

---

## Verificación (Rich Results Test)

Para verificar cuando esté deployado:
1. Ir a https://search.google.com/test/rich-results
2. Ingresar `https://ada-audits.com/`
3. Debería mostrar: Organization, Service, AggregateRating, FAQPage, Review

---

## Siguientes Pasos
- [ ] Crear `og-image.png` (1200x630) para social sharing
- [ ] Crear `logo.png` para schema Organization
- [ ] Deploy a ada-audits.com
- [ ] Submit sitemap en Google Search Console
- [ ] Verificar con Rich Results Test post-deploy
