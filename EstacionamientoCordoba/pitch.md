# Pitch SaaS Estacionamiento Córdoba

## Resumen Ejecutivo
Desarrollamos una plataforma SaaS para la gestión integral de estacionamientos en la provincia de Córdoba, ofreciendo reservas en tiempo real, pagos digitales, y analítica operativa. El modelo de negocio se basa en suscripciones mensuales para operadores y comisiones por transacción.

## Arquitectura y Hardware
- **Frontend**: React + TypeScript, SPA responsive.
- **Backend**: FastAPI (Python) con PostgreSQL y Redis.
- **Infraestructura**: Deploy en DigitalOcean Kubernetes (K8s) usando nodos con 2 vCPU, 4 GB RAM (tamaño S). 
- **Hardware en sitio**: Raspberry Pi 4 con cámara y sensor RFID para entrada/salida, conectado vía MQTT al backend.
- **Escalabilidad**: Autoscaling de pods, uso de CDN Cloudflare.

## Stack Tecnológico
| Capa | Tecnologías |
|------|-------------|
| UI/UX | React, TailwindCSS |
| API | FastAPI, Pydantic |
| DB | PostgreSQL 15, Prisma ORM |
| Cache | Redis 7 |
| Mensajería | MQTT (Mosquitto) |
| CI/CD | GitHub Actions, Docker, Helm |
| Monitoring | Prometheus + Grafana |

## Fases de Implementación en Córdoba
| Fase | Duración | Actividades |
|------|----------|-------------|
| **F1** (MVP) | 1 mes | - Configuración de hardware en 2 estacionamientos piloto.<br>- Desarrollo de módulo de reservas y pagos.<br>- Dashboard básico de ocupación. |
| **F2** | 2 meses | - Integración con sistemas de pago locales (MercadoPago, TodoPago).<br>- Notificaciones push y SMS.<br>- Reporting avanzado. |
| **F3** | 3 meses | - Expansión a 10 estacionamientos.
- API pública para partners.
- Modelo de precios dinámico. |

## Monetización (ARS)
- **Suscripción básica**: $1.500/mes por estacionamiento (incluye 1 000 reservas). 
- **Suscripción premium**: $2.800/mes (reservas ilimitadas, reporting avanzado).
- **Comisión por transacción**: 3 % del valor del ticket.
- **Retainer de mantenimiento**: $800/mes opcional.

## Estrategia de Marketing
- **Inbound**: Blog SEO sobre gestión de estacionamientos y movilidad urbana.
- **Outbound**: Cold outreach a municipalidades y empresas de gestión de parkings (personalización basada en datos de ocupación).
- **Partners**: Integración con apps de movilidad (e.g., DiDi, Cabify) para ofrecer estacionamiento a conductores.
- **Campañas SEM**: Keywords: "gestión de estacionamiento Córdoba", "reserva de parqueo online".

## Competencia / SEMM
| Competidor | Diferenciador | Precio (ARS) |
|------------|---------------|--------------|
| Park+ (local) | Solo reservas, sin analítica | $2.000/mes |
| EasyPark | App móvil, alta cuota mensual | $3.500/mes |
| Nuestro SaaS | Plataforma completa + hardware de bajo costo + soporte local |

## Riesgos y Mitigaciones
- **Adopción lenta**: Mitigar con pruebas piloto gratuitas de 30 días.
- **Regulación de pagos**: Utilizar pasarelas locales certificadas.
- **Fallas de hardware**: Redundancia con doble Raspberry Pi y alertas automáticas.
- **Competencia establecida**: Enfocar en nicho de pequeños operadores y ofrecer precios flexibles.

## Roadmap
- **3 meses**: MVP en 2 parkings, 10 clientes piloto, ingresos estimados $30.000 ARS.
- **6 meses**: Expansión a 10 parkings, suscripciones premium, ingresos $120.000 ARS.
- **12 meses**: Red nacional, integración con apps de movilidad, MRR > $300.000 ARS.

---
*Ranukita Bot — Propiedad de Ranuk IT Solutions | ranuk.dev | ranukorbit.com*