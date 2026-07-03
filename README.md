# PDF Summarizer Bot 🤖

**Automatiza resúmenes de PDFs usando IA** (FastAPI + PyMuPDF + LLM).

## 🚀 Demo rápida
```bash
# Clonar
git clone https://github.com/RanuK12/pdf-summarizer-bot.git
cd pdf-summarizer-bot

# Instalar dependencias
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate en Windows
pip install -r requirements.txt

# Correr servidor (desarrollo)
uvicorn main:app --reload

# Probar endpoint
curl -X POST -F "file=@/ruta/a/tu/archivo.pdf" http://localhost:8000/summarize
```

## 📁 Estructura del proyecto
```
pdf-summarizer-bot/
├── main.py              # API FastAPI
├── requirements.txt     # Dependencias
├── README.md            # Esta guía
├── .github/             # Workflows (opcional)
└── Dockerfile           # Para deploy (pendiente)
```

## 🔧 Próximos pasos (roadmap)
1. **IA**: Integrar LLM (Mistral/DeepSeek) para resumir el texto extraído.
2. **Tests**: Añadir pytest para `/summarize`.
3. **Docker**: Crear Dockerfile para despliegue rápido.
4. **Frontend**: Opcional: interfaz web con HTMX/React.
5. **Monetización**: Versión premium (resúmenes más detallados, API keys).

## 💡 Ideas para monetizar
- **Plantilla premium**: `$15` en Gumroad con instrucciones de deploy + código comentado.
- **SaaS**: Suscripción mensual para uso de la API (ej: `$50/mes` por 1000 resúmenes).
- **Plantilla de Notion**: Guía paso a paso para armar tu propio bot.

## 📄 Ejemplo de uso
```python
# Desde Python
import requests

url = "http://localhost:8000/summarize"
files = {"file": open("ejemplo.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## 🔗 Links útiles
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [Mistral AI API](https://docs.mistral.ai/) (opcional para resumir)