# CLAUDE.md — Ranuk IT Solutions
# Principios Karpathy + Superpowers adaptados

## 1. Pensá antes de codear
- Explicitá supuestos. Si hay ambigüedad, preguntá.
- Si hay approach más simple, decilo.
- Si algo no está claro, pará y preguntá.

## 2. Simplicidad primero
- Mínimo código que resuelve el problema.
- Nada especulativo, nada "por si acaso".
- Si 200 líneas pueden ser 50, reescribí.
- No abstracciones para uso único.

## 3. Cambios quirúrgicos
- Tocá solo lo necesario.
- No "mejores" código adyacente.
- Matcheá el estilo existente.
- Cada línea cambiada debe trazar al pedido.

## 4. Ejecución orientada a objetivos
- Definí criterio de éxito antes de implementar.
- "Agregar validación" → "Escribir test que falle, hacerlo pasar"
- "Fixear bug" → "Reproducir en test, fixear, verificar"
- Para tareas multi-step: plan breve con verificación por paso.

## 5. Debugging sistemático (de Superpowers)
- NUNCA fixear sin investigar root cause primero.
- Fase 1: Leer errores, reproducir, check cambios recientes.
- Fase 2: Encontrar ejemplos que funcionan, comparar.
- Fase 3: Hipótesis única, test mínimo.
- Fase 4: Implementar fix, verificar.
- Si 3+ fixes fallan → cuestionar la arquitectura.

## Stack & Conventions
- Python: type hints, docstrings, pytest
- TypeScript: strict mode, ESLint, Prettier
- SQL: Postgres 16, snake_case, soft delete con deleted_at
- Git: conventional commits, no push a main sin PR
- Tests: TDD cuando sea posible, coverage > 80%

## RTK (Token Optimization)
- rtk está instalado globalmente (v0.40.0)
- Todos los comandos shell pasan por rtk automáticamente
- Ahorra 60-90% de tokens en outputs de git, cargo, npm, etc.
