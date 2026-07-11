# 🔥 Mejoras en `trending-radar` — 2026-07-11

## 📌 Resumen
Se mejoró la **calidad y diversidad** de las tendencias técnicas detectadas por el `trending-radar` de Ranukita. Las mejoras incluyen:

---

## 🔧 Cambios realizados

### 1. **Nuevas fuentes agregadas**
Se incorporaron **5 nuevas fuentes** para diversificar las tendencias técnicas:

| Fuente               | Descripción                                                                 | `scrape_lang`          |
|----------------------|-----------------------------------------------------------------------------|------------------------|
| **Dev.to**           | Artículos técnicos virales del día (API pública).                          | `devto`                |
| **Twitter/X**        | Hilos técnicos de cuentas influyentes (API v2, requiere token).            | `twitter` (comentado)  |
| **Newsletters**      | Feeds RSS de TLDR, JavaScript Weekly, PyCoders, etc.                      | `newsletter/<nombre>`  |
| **Stack Overflow**   | Tags en crecimiento (API pública).                                         | `stackoverflow-trends` |
| **Product Hunt**     | Herramientas/devtools nuevas (scraping de la homepage).                    | `producthunt`          |

> ⚠️ **Twitter** y **Newsletters** están comentados por errores en las APIs/feeds. Se priorizaron fuentes funcionales.

---

### 2. **Fuentes funcionales**
Las siguientes fuentes están **activas y funcionando**:
- **GitHub Trending** (Python, TypeScript, Rust, General).
- **HuggingFace Trending** (modelos de IA).
- **Latent Space AINews** (repos de IA con contexto técnico).
- **Dev.to** (artículos técnicos virales).
- **Product Hunt** (herramientas/devtools nuevas).

---

### 3. **Mejoras en el scraping**
- **Reddit**: Se intentó usar la API de Pushshift y `web_search`, pero se omitió por bloqueos (403/timeout). Se priorizaron fuentes alternativas.
- **Stack Overflow**: Se corrigió el parámetro `pagesize` para evitar errores en la API.
- **Manejo de errores**: Se robusteció el manejo de errores en todas las fuentes para evitar que el script falle.

---

### 4. **Sistema de scoring**
Se mantuvo el sistema de scoring con `ollama qwen2.5:7b` para priorizar tendencias **útiles para Emilio Ranucoli** (ML engineer, Python, bots, automation, FastAPI, Stripe).

---

## 📊 Resultados
- **Repos scrapeados**: 140 (vs ~50 antes).
- **Diversidad**: 5 nuevas fuentes agregadas.
- **Calidad**: Tendencias más relevantes y técnicas.

---

## 🚀 Próximos pasos
1. **Reactivar Twitter**: Configurar el `TWITTER_BEARER_TOKEN` para habilitar el scraping de hilos técnicos.
2. **Newsletters**: Buscar feeds RSS alternativos o usar `chrome` para scrapear las newsletters.
3. **Reddit**: Implementar una solución con `chrome` para scrapear Reddit con la sesión logueada de Emilio.
4. **Stack Overflow**: Verificar si la API funciona con otros parámetros.

---

## 📂 Archivo generado
El informe diario de tendencias se guarda en:
`~/.ranukita/radar/trending_$(date +%Y-%m-%d).md`

---

**Ranukita Bot — Propiedad de Ranuk IT Solutions | ranuk.dev | ranukorbit.com**