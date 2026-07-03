"""
PDF Summarizer Bot - FastAPI server
Automatización de resúmenes de PDFs usando IA.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import Optional
import fitz  # PyMuPDF
import tempfile

app = FastAPI(title="PDF Summarizer Bot", version="0.1.0")

@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...), lang: Optional[str] = "es"):
    """
    Endpoint para resumir un PDF.
    - Recibe: archivo PDF (upload)
    - Devuelve: resumen en texto (JSON)
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF.")

    try:
        # Guardar temporalmente el PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(await file.read())
            tmp_path = tmp_pdf.name

        # Extraer texto del PDF
        doc = fitz.open(tmp_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # TODO: Aquí iría la llamada a la IA para resumir (ej: mistralai/client.chat(...))
        # Por ahora, devolver el texto extraído como "resumen" (placeholder)
        summary = f"[Resumen generado] Longitud: {len(text)} caracteres. Texto extraído:\n\n{text[:500]}..."

        return JSONResponse(
            content={
                "status": "success",
                "filename": file.filename,
                "summary": summary,
                "language": lang
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "pdf-summarizer-bot"}