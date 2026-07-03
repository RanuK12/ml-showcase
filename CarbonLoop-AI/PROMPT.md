# CarbonLoop AI — Prompt de build (MVP)

Origen: idea "unicornio" generada por Ranukita el 2026-07-02 (`~/.ranukita/ideas/unicorn_idea_20260702_224246.pdf`).
Este archivo es el PROMPT que un agente de código ejecuta para construir el MVP. Buildeá el MVP, no el unicornio entero.

## Qué es
CarbonLoop AI: plataforma que ayuda a PYMEs a **medir, reportar y reducir su huella de carbono** sin
consultoras caras. El unicornio a 5 años es la capa de infraestructura verde (marketplace de créditos,
integraciones con reguladores/bancos). El MVP entrega solo el núcleo verificable de valor.

## Alcance del MVP (lo ÚNICO a construir ahora)
Una API + un cálculo real, deployable, que:
1. Recibe consumos de la PYME (electricidad kWh, gas m³, combustible litros, km de flota) por
   formulario o CSV.
2. Calcula la huella de carbono (tCO2e) con **factores de emisión públicos** (GHG Protocol / DEFRA /
   grid emission factor por país). Nada de ML todavía: fórmula transparente y auditable.
3. Devuelve un reporte: total tCO2e, desglose por fuente (scope 1/2), y 3 recomendaciones de reducción
   priorizadas por impacto/costo.
4. Genera un PDF del reporte (reusar `scripts/ranukita_report.py` del bridge si sirve).

NO incluir en el MVP: marketplace de créditos, scraping de ERP/IoT, pagos, cuentas de usuario, Kafka.
Eso queda documentado como roadmap, no se construye.

## Stack (mínimo, Ponytail)
- Python 3.12, **FastAPI + Uvicorn**.
- Factores de emisión en un `data/emission_factors.json` versionado (con fuente y año de cada factor).
- Cálculo en `carbonloop/calc.py` (funciones puras + type hints + docstrings).
- Endpoints: `POST /footprint` (JSON o CSV) → reporte JSON; `POST /footprint/pdf` → PDF.
- Tests con pytest: casos de cálculo con valores conocidos (coverage del cálculo > 80%).
- README con: cómo correr local, ejemplo de request/response, y la lista de factores con su fuente.

## Criterio de éxito (verificable)
- `uvicorn` levanta; `POST /footprint` con un ejemplo real devuelve tCO2e coherente con los factores.
- `pytest` verde con al menos 3 casos de cálculo verificados a mano.
- Commit en branch `ranukita/<task_id>` con tag `[ranukita:<task_id>]`.
- Honestidad: los factores de emisión deben citar fuente real; si no se consigue un factor confiable
  para algo, se documenta el supuesto, no se inventa un número.

## Roadmap (documentar en README, NO construir ahora)
Conectores ERP/facturación → estimación por ML (±5%) → marketplace de créditos → integración reguladores.
