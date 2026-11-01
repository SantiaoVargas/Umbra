"""Aplicación FastAPI de Umbra.

Por ahora solo expone `/health` para confirmar que la API está viva. Los
endpoints de escaneo (recibir un host, devolver el reporte) llegan en la Fase 5,
cuando el motor ya funcione de punta a punta.
"""

from fastapi import FastAPI

from umbra import __version__

app = FastAPI(
    title="Umbra",
    description="Escáner de seguridad para apps web y APIs.",
    version=__version__,
)


@app.get("/health")
def health() -> dict[str, str]:
    """Chequeo de vida: confirma que la API está arriba y responde."""
    return {"status": "ok", "version": __version__}
