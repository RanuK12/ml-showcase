# Auditorías WCAG

## Auditoría Clarín.com
- **Fecha**: 27 de junio de 2026
- **Auditor**: Ranukita Bot
- **Objetivo**: Homepage principal de https://www.clarin.com/
- **PDF**: WCAG_Clarín_2026-06-27.pdf (generado con ranukita_report.py)
- **Spec**: spec-wcag-clarin.json

### Hallazgos destacados
- 14 issues críticos (nivel A)
- 8 issues moderados (nivel AA)
- Fallos de contraste en el CTA principal (1:1 vs 4.5:1 mínimo)
- 27 inputs sin etiquetas
- 11 botones sin nombre accesible
- Jerarquía de headings desbalanceada (5 h1, 362 h2, saltos h1→h3)
- Falta landmark <main> o role="main"

### Recomendaciones
- Añadir alt a imágenes
- Mejorar contraste
- Añadir aria-label a botones con SVGs
- Añadir <main> o role="main"
- Reorganizar headings
- Asociar inputs con labels
- Asegurar navegación con teclado
- Validar con axe DevTools / WAVE

### Próximos pasos
Contactar al equipo de Clarín con este informe adjunto y ofrecer auditoría completa o consultoría de accesibilidad.
