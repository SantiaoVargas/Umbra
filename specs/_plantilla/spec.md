# Spec NNN: <nombre de la feature>

**Historia:** <ID backlog> Como ... quiero ... para ...
**Dominio:** <dominio> · **Responsable:** <persona> · **Revisor/a:** <persona> · **Fecha:** AAAA-MM-DD · **Estado:** borrador / aprobada / implementada
**Depende de:** <historias> · **Ficha de dominio:** `docs/architecture/dominios/<dominio>.md`

Marcas de evidencia: **observado** (ruta/línea), **<persona>** (fecha), **hipótesis**.

## Alcance
- Entra: ...
- **No entra:** ...

## Flujo
<pasos numerados o diagrama mermaid: actor, disparador, decisiones, efectos>

## Contrato
<firmas públicas, modelos Pydantic, JSON de entrada/salida, formato de config. Enlazar/crear en `docs/architecture/contratos/` si es estable>

## Honestidad: severidad y confianza (obligatorio si produce hallazgos)
| Hallazgo | Severity | Cuándo es `confirmado` (qué se verificó) | Cuándo es `por-revisar` (solo patrón) |
|---|---|---|---|
| ... | ... | ... | ... |

¿Puede dar falso positivo? ¿Cómo se evita? Recordar P2: `critical` ⇒ `confirmado`.

## Seguridad del producto (marcar cada punto: aplica / no aplica / cómo se cumple)
- P1 Allowlist: ¿todo request pasa por el cliente observador?
- P3 Tests: ¿solo contra app local / mocks, nunca terceros?
- P4 Peticiones: ¿solo lectura (`GET`/`HEAD`/`OPTIONS`)? Si hay payloads → justificar y pedir aprobación de los dos.
- P5 Secretos/evidencia: ¿qué se guarda y qué se redacta?

## Decisiones abiertas
<preguntas que cambian el diseño; se resuelven con la otra persona antes de aprobar>

## Criterios de aceptación (booleanos)
- [ ] CA1: ... (Verdadero/Falso, con el test o comando que lo demuestra)
- [ ] CA2: ...

## Riesgos y reversión
<qué puede salir mal, cómo se deshace (revert del PR, flag, etc.)>
