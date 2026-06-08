# Bounty Tracker

## Resumen
| Bounty | Monto | Repo | Branch | PR | Estado | Fecha |
|--------|-------|------|--------|-----|--------|-------|
| Job validation: inverted budget ranges (#2853) | $780 USD | SecureBananaLabs/bug-bounty | ranukita/fdfde6 | [#4436](https://github.com/SecureBananaLabs/bug-bounty/pull/4436) | PR abierto, listo para review | 2026-06-04 |

---

## Detalle: #2853 — Job validation: inverted budget ranges

- **Bounty**: $780 USD (Algora / SecureBananaLabs)
- **Issue**: https://github.com/SecureBananaLabs/bug-bounty/issues/2853
- **Parent**: #743 (Low Hanging Fruit Automation)
- **Repo**: https://github.com/SecureBananaLabs/bug-bounty
- **Branch**: `ranukita/fdfde6`
- **PR**: https://github.com/SecureBananaLabs/bug-bounty/pull/4436
- **Fecha**: 2026-06-04
- **Estado**: PR abierto, listo para review

### Qué se hizo
- Extracted base Zod schema (`jobBaseSchema`) from `createJobSchema`
- Added `.refine()` to `createJobSchema` ensuring `budgetMax >= budgetMin`
- Added conditional `.refine()` to `updateJobSchema` (only validates when both fields present)
- Created 10 comprehensive tests in `jobValidator.test.js`

### Archivos modificados
- `apps/api/src/validators/job.js` — validación de ranges
- `apps/api/src/tests/jobValidator.test.js` — 10 tests nuevos

### Test results
```
✔ 11 tests, 0 failures
✔ createJobSchema: accepts valid job
✔ createJobSchema: accepts equal budgets
✔ createJobSchema: rejects inverted range
✔ createJobSchema: rejects budgetMax=0
✔ createJobSchema: rejects missing fields
✔ updateJobSchema: accepts partial (title only)
✔ updateJobSchema: accepts valid budget range
✔ updateJobSchema: rejects inverted range
✔ updateJobSchema: allows only budgetMin
✔ updateJobSchema: allows only budgetMax
✔ health check
```
