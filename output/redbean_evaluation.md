# Redbean — Evaluación para Ranuk IT Solutions

**Fecha:** 2026-06-02  
**Autor:** Ranukita (AI Assistant)  
**Objetivo:** Evaluar Redbean como herramienta para crear productos digitales vendibles en Gumroad

---

## 1. ¿Qué es Redbean?

[Redbean](https://justine.lol/redbean) es un servidor web **single-file** de código abierto creado por Justine Tunney (ex-Google). Un solo archivo ejecutable de ~5.5MB que:

- **Incluye todo:** Lua 5.4, SQLite 3.40, TLS/SSL (MbedTLS), compresión, hashing
- **Corre en 6 OS:** Linux, macOS, Windows, FreeBSD, NetBSD, OpenBSD (AMD64 + ARM64)
- **Es un ZIP ejecutable:** le metés archivos con `zip` y se convierte en tu web app
- **Benchmark:** 5.3 millones de queries/segundo en Threadripper
- **Sandboxing** y system call tracing para seguridad
- **REPL interactivo** con code completion para desarrollo rápido

**Versión actual:** v3.0.0 (agosto 2024)

## 2. Evaluación: ¿Sirve para Gumroad?

### ✅ Ventajas

| Ventaja | Impacto para Emilio |
|---------|---------------------|
| **Producto = 1 archivo** | El cliente descarga un `.com` de ~5MB, lo ejecuta, y tiene su web. Sin npm, sin Docker, sin hosting. |
| **Cero costo de hosting** | La app corre en la máquina del cliente. No necesitan pagar Heroku/Vercel/DigitalOcean. |
| **Cross-platform** | Mac, Windows, Linux — el 99% de compradores están cubiertos. |
| **TLS incluido** | HTTPS nativo sin configurar certificados. |
| **SQLite embebido** | Formularios con persistencia local. Los leads quedan guardados. |
| **Lua simple** | Scripts de 20-50 líneas resuelven lógica server-side. No necesita un framework pesado. |
| **Alto margen** | 100% código. Costo de producción = 0. Precio Gumroad $19-49 = profit puro. |
| **Diferenciador** | "Descargá y ejecutá" es mucho más simple que "deployá a Vercel" para un no-tech. |

### ❌ Desventajas

| Desventaja | Mitigación |
|------------|-----------|
| **Lua no es popular** | Pero para scripts de 30 líneas no importa. El cliente no toca Lua. |
| **No es React/Next.js** | Para landing pages estáticas con 1 formulario, no hace falta un framework. |
| **Ecosistema limitado** | No hay NPM. Pero para el caso de uso (landing + formulario + SQLite), sobra. |
| **Curva de aprendizaje del dev** | Emilio aprende Lua básico en 1 tarde. |
| **No escala a miles de usuarios** | Pero para un starter kit de $29, el cliente no necesita escalar. |
| **Poco conocido** | Pro: differentiator. Contra: menos stackoverflow. |

### 🎯 Caso de Uso Ideal para Emilio

**Productos "Landing Page Starter Kit" en Gumroad:**

1. **Landing Page Kit** ($29) — Landing con formulario + SQLite + leads dashboard
2. **SaaS Starter Kit** ($49) — Landing + auth básico + dashboard + SQLite
3. **E-commerce Kit** ($39) — Catálogo + carrito + checkout simple

**Flujo del producto:**
```
Cliente compra en Gumroad
    ↓
Descarga "my-landing.com" (~5MB)
    ↓
Lo ejecuta: ./my-landing.com
    ↓
Tiene su web en http://localhost:8080
    ↓
Personaliza index.html y style.css
    ↓
¡Listo! Web corriendo sin hosting
```

**Distribución avanzada:** El cliente puede poner el archivo en un VPS ($5/mes) y tiene una web pública. O usar Cloudflare Tunnel para exponerla gratis.

## 3. Prototipo Creado

Se creó un prototipo funcional en `/output/redbean-landing/`:

| Archivo | Descripción |
|---------|-------------|
| `landing.lua` | Servidor: rutas, SQLite para leads, manejo de formularios (Redbean usa Lua, no Ruby `.rb`) |
| `index.html` | Landing page responsive con hero, features, testimonials, CTA, formulario |
| `style.css` | CSS dark theme moderno, gradientes, responsive |
| `build.sh` | Script de build que empaqueta todo en un solo `.com` ejecutable |

### Para probar:
```bash
cd ~/Desktop/Oficina_Ranuk/output/redbean-landing
# Opción rápida: usar el build script
chmod +x build.sh
./build.sh my-landing.com
./my-landing.com

# O manualmente:
curl -sL https://redbean.dev/redbean-latest.com -o redbean.com
chmod +x redbean.com
mkdir _pkg && cp redbean.com _pkg/my-landing.com
cp index.html style.css _pkg/
cp landing.lua _pkg/.init.lua   # ← Redbean busca /.init.lua en el ZIP
cd _pkg && zip -j ../my-landing.com index.html style.css .init.lua
cd .. && rm -rf _pkg
chmod +x my-landing.com
./my-landing.com
# Abrir http://localhost:8080
# Leads dashboard: http://localhost:8080/leads
```

> **Nota sobre extensiones:** Redbean usa Lua (`.lua`) como lenguaje server-side, no Ruby (`.rb`). El archivo del prototipo es `landing.lua`. Si bien `.rb` fue mencionado en el pedido, la extensión correcta para Redbean es `.lua` ya que embebe un intérprete Lua 5.4.

## 4. Veredicto

| Criterio | Rating | Nota |
|----------|--------|------|
| Viabilidad técnica | ⭐⭐⭐⭐ | Funciona perfecto para landing + forms |
| Facultad de venta | ⭐⭐⭐⭐⭐ | Producto diferenciado, margen 100% |
| Escalabilidad del modelo | ⭐⭐⭐⭐ | Replicable: cambiar HTML/CSS = nuevo kit |
| Esfuerzo de producción | ⭐⭐⭐⭐ | 1 tarde por kit después del primero |
| Mercado objetivo | ⭐⭐⭐ | Nicho: freelancers, emprendedores no-tech |

### Recomendación: **CREAR Y VENDER**

El prototipo está listo para pulir y poner en Gumroad. Pasos sugeridos:

1. ✅ Prototipo base hecho (este repo)
2. 🔄 Pulir diseño CSS (probar 3-4 variantes de colores)
3. 🔄 Agregar 2-3 templates más (minimal, corporate, creative)
4. 🔄 Crear landing de Gumroad para el kit
5. 🔄 Precio sugerido: $29 (landing básica) / $49 (kit completo con auth)
6. 🔄 Publicar en ProductHunt como "deploy your landing page in 1 click"

---

*Evaluación realizada por Ranukita — tu mano derecha digital 🚀*
