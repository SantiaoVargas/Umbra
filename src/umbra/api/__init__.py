"""La capa API de Umbra: FastAPI que envuelve el motor (core).

Esta capa NO hace lógica de seguridad; solo recibe pedidos, llama al core y
devuelve resultados. Todo el trabajo real vive en `umbra.core`.
"""
