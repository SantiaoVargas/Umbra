from pydantic import BaseModel, field_validator


class Objetivo(BaseModel):
    host: str    

    @field_validator("host")
    @classmethod
    def _validar_host(cls, v):
        if "://" in v:
            raise ValueError("(El host no debe incluir https://)")
        if "/" in v:
            raise ValueError("(El host no debe incluir rutas, ej: /login)")
        if ":" in v:
            raise ValueError("(El host no debe incluir puerto, ej: :8000)")
        return v
