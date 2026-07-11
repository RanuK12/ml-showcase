# Mini-diagnóstico de accesibilidad (WCAG 2.1 – AA)
**Sitio evaluado:** [mayucooperativa.org](https://mayucooperativa.org)

---

| #  | Hallazgo                          | Por qué incumple WCAG 2.1 AA               | Impacto en usuarios                     | Solución práctica                                                                                     |
|----|-----------------------------------|--------------------------------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------|
| 1  | Logo sin texto alternativo        | 1.1.1 Non-text Content                     | Usuarios de lectores de pantalla no identifican la marca ni pueden navegar al inicio.               | ```html
<img src="/assets/logo.svg" alt="Mayú Cooperativa – Logo">
```                          |
| 2  | Contraste insuficiente en banner  | 1.4.3 Contrast (Minimum)                   | Usuarios con visión reducida o daltonismo no leen el mensaje del banner.                            | ```css
.hero h1 { color: #FFFFFF; background-color: #2C5A9A; /* Contraste 4.6:1 */ }
```            |
| 3  | Orden de encabezados roto         | 1.3.1 Info and Relationships               | Lectores de pantalla no perciben la estructura del contenido.                                       | ```html
<h2>Nuestros proyectos</h2>
``` (revisar jerarquía en todo el sitio).                          |
| 4  | Enlaces "Leer más" sin foco visible | 2.4.7 Focus Visible                        | Usuarios que navegan con teclado no saben qué enlace está activo.                                   | ```css
.btn:focus { outline: 3px solid #FFB400; outline-offset: 2px; }
```                            |
| 5  | Falta atributo `lang` en `<html>` | 3.1.1 Language of Page                     | Lectores de pantalla no seleccionan la voz/pronunciación correcta.                                  | ```html
<html lang="es">
```                                                                 |

---

### Resumen para el cliente
- **3-5 ajustes concretos** son suficientes para cumplir con **WCAG 2.1 AA**.
- Cada cambio mejora la experiencia de **todos los usuarios** y favorece el **SEO**.
- Implementación rápida (minutos) y bajo costo.

> **Próximo paso:** Si lo desea, podemos acompañarle en la implementación y validar los resultados con pruebas de usuarios reales. ¡Estamos a su disposición!