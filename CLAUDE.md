# Umbra — instrucciones para la IA

Este archivo está en git: lo cargan Claude Code (y, vía `AGENTS.md`, Codex/Cursor) en la sesión de **cualquiera de los dos devs**. Preferencias personales van en `CLAUDE.local.md` (ignorado por git).

1. Lee primero `docs/constitution.md`. Es innegociable (incluye las **reglas del producto**: allowlist fail-closed, confianza honesta, tests sin objetivos reales).
2. Para un desarrollo nuevo sigue `docs/flujo-de-trabajo-ia.md` paso a paso. Invoca `/umbra-slice` para el ciclo. Reglas técnicas del repo: `docs/repo_rules.md`.
3. Qué hacer ahora: `backlog.md` (historias `NNN`, mejoras `M-NNN`, ideas `I-NNN`). Una sesión, un slice. Antes de tomar una historia mira la columna **Responsable**: si la tiene el otro dev, no la toques.
4. Conocimiento acumulado: `docs/architecture/` (`diseno` en `docs/DISENO-MOTOR.md`, fichas en `dominios/`, `decisiones.md`). Si un dominio tiene ficha, léela antes de tocarlo; si no, créala con `_plantilla.md`.
5. Marca cada afirmación como **observada** (ruta/línea), **explicada por <persona>** (fecha) o **hipótesis**.
6. Reglas duras: la IA escribe código, tests y docs en una rama; **push, PR y merge los hace la persona** (commit solo si lo pide). Nunca trabajar en `main`. Sin dependencias nuevas sin aprobación. Nunca secretos ni datos de objetivos reales en git. Los tests jamás apuntan a hosts de terceros.
7. **La verdad vive en el repo, no en el chat ni en la memoria privada de la IA.** Toda decisión o aclaración que cambie algo se escribe en spec, ficha o `decisiones.md` antes de cerrar la sesión; el otro dev (y su IA) solo ve lo que está en git.
8. Al cerrar cualquier tarea: ficha de dominio, `docs/architecture/decisiones.md` si hubo decisión, `backlog.md` (estado y mejoras nuevas con etiqueta **mejora**) y una fila en `docs/metricas-adopcion.md`.
