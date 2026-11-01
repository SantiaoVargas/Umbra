# Flujo de trabajo con IA para cada desarrollo

**Versión:** 2026-11-01. Manual operativo. La constitución dice qué es obligatorio; este documento dice cómo se hace, paso a paso, entre dos personas y sus IAs.

## 0. Cómo se activa la base sin hacer nada

- Claude Code carga `CLAUDE.md` al abrir el repo; Codex y Cursor leen `AGENTS.md`. Ambos mandan leer la constitución y este flujo.
- La skill del proyecto `/umbra-slice` (`.claude/skills/umbra-slice/`) ejecuta el ciclo. Está en git: los dos la tienen al clonar.
- La memoria privada de cada IA es complemento, no sustituto: **la verdad vive en el repo**.

## 1. Roles

| Quién | Hace | No hace |
|---|---|---|
| Persona responsable (NAVIGATOR) | Elige la historia, aprueba spec y tasks, revisa `git diff`, hace commit/push/PR | Escribir el grueso del código |
| IA de esa persona (DRIVER) | Lee la base, propone spec, escribe tests y código, corre `pytest`/`ruff`, actualiza docs | Push, PR, merge, trabajar en `main`, agregar dependencias sin aprobación |
| Otra persona (REVISORA) | Aprueba la spec y revisa el PR (con ayuda de su IA si quiere) | Tocar la rama ajena sin avisar |

## 2. Trabajar de a dos sin pisarse

1. **Reclamar una historia.** Mira `backlog.md`: una historia sin **Responsable** y con sus dependencias en `hecho` está libre. Avísale al otro (chat) y pon tu nombre en **Responsable** y estado `en spec` en tu rama (ver paso 3).
2. **Una historia = un responsable = una rama = una spec.** El número de la spec es el de la historia (`specs/004_header_checker/`).
3. **PR temprano (draft).** Apenas hay spec + tasks, se abre un PR en borrador: así el otro ve qué estás haciendo y aprueba la spec **antes** de que se escriba código.
4. **Archivos calientes** (`backlog.md`, `decisiones.md`, `metricas-adopcion.md`): editar con cambios pequeños y solo agregar filas; resolver conflictos conservando las dos versiones. IDs nuevos (`NNN`, `M-NNN`, `I-NNN`): tomar el siguiente libre al hacer rebase si hubo colisión.
5. **Módulos independientes** (`core/modules/*`) permiten trabajar en paralelo sin conflictos. Piezas que dependen de otra (ej. el cliente HTTP necesita el guardia) se hacen en orden, no en paralelo.
6. **Contexto compartido.** Antes de cerrar la sesión, lo que la IA "aprendió" se escribe en spec/ficha/decisiones. Si no está en git, el otro dev no lo sabe.
7. **`main` siempre verde.** `git pull --rebase origin main` antes de abrir el PR; `pytest` y `ruff` pasan.

## 3. Ciclo de un desarrollo (seis pasos)

### Paso 1. Historia en `backlog.md`
"Como [rol] quiero [acción] para [beneficio]" con ID `NNN`, dominio, prioridad A/B/C, dependencias. Cualquiera de los dos (o su IA) puede proponerla; una idea (`I-NNN`) se promueve a historia cuando los dos lo acuerdan.
Prompt tipo: `Agrega al backlog la historia: como dev quiero X para Y. Dominio cliente-http.`

### Paso 2. Contexto: ficha de dominio
La IA lee `docs/architecture/dominios/<dominio>.md` y `docs/DISENO-MOTOR.md`. Si no hay ficha, la crea desde `_plantilla.md` **solo con lo necesario para esta historia**. Pregunta a la persona únicamente lo que cambie una decisión.

### Paso 3. Spec en `specs/<NNN>_<feature>/spec.md`
Desde `specs/_plantilla/spec.md`: alcance, **qué no entra**, flujo, contrato, **honestidad (severidad/confianza)**, **seguridad del producto (P1–P6)**, criterios de aceptación booleanos, riesgos y reversión. Modo plan. Nada de código antes de la aprobación de la persona responsable **y** la revisora (aprobación en el PR draft).
Prompt tipo: `Redacta la spec 001 para la historia 001 usando la ficha guardia.md. Modo plan.`

### Paso 4. Tasks en `specs/<NNN>_<feature>/tasks.md`
Bloques de 15–30 min, cada uno con su test y su ruta. Aprobados por la persona responsable. Lo que no cabe en la sesión queda anotado en `tasks.md` como pendiente (y en backlog si es historia nueva).

### Paso 5. Ejecución TDD en rama
1. Rama desde `main` actualizado: `feature/<NNN>-<tema>`.
2. Por cada task: test rojo → código mínimo → refactor → `pytest` y `ruff check` en verde. La IA muestra la salida real.
3. Sin commits salvo que la persona lo pida; propone mensaje convencional.
4. Antes del PR: `git diff` completo revisado por la persona responsable; criterios de aceptación marcados V/F con evidencia (salida de test o comando).
5. Módulos de detección: probar contra la **app vulnerable local**, nunca contra hosts reales (P3).

### Paso 6. Cierre y aprendizaje
Obligatorio antes de dar por terminado (mismo PR):
- Ficha de dominio actualizada (contratos, decisiones, límites).
- `docs/architecture/decisiones.md`: cada decisión nueva con fecha y quién.
- `docs/architecture/contratos/` y `datos/` si cambió un contrato o esquema (ej. formato de la config de allowlist, JSON del reporte).
- `backlog.md`: historia a `en revisión`/`hecho`; deuda detectada como **mejora** `M-NNN`.
- `docs/repo_rules.md` si se descubrió una regla o límite técnico nuevo.
- Fila en `docs/metricas-adopcion.md`.

## 4. Slice ligero vs completo

- **Ligero** (fix o mejora C de 1–2 archivos): spec de 5 líneas en la descripción del PR, sin `tasks.md`, test obligatorio, cierre normal.
- **Completo** (historia nueva, mejora A/B, toca el contrato de `Finding`, la allowlist o la API): los seis pasos con spec y tasks aprobadas.
- **Regla:** todo lo que toque P1 (allowlist/cliente HTTP), P2 (modelo de confianza) o P4 (peticiones activas) es siempre slice completo.

## 5. Reglas de oro durante la sesión

- **Una sesión, un slice.** Si surge otra cosa, va al backlog.
- **Modo plan primero** si el cambio toca más de un archivo o un contrato.
- **Leer, no asumir.** Ruta/línea o comando como evidencia; si no se verificó, decirlo.
- **Preguntar solo lo que cambia una decisión.**
- **Nada nuevo sin test.**
- **Dependencias nuevas** requieren aprobación de los dos.
- **Secretos y objetivos reales:** nunca en prompts, docs ni git.

## 6. Qué hacer según el tipo de tarea

| Tarea | Cómo | Entrada | Salida |
|---|---|---|---|
| Entender o documentar una pieza | `/umbra-slice` (paso 2) | pregunta | ficha de dominio |
| Historia nueva o cambio | `/umbra-slice` | historia del backlog | spec, tasks, código con tests, docs |
| Deuda técnica | `/umbra-slice` con `M-NNN` | ítem del backlog | slice ligero o completo |
| Idea nueva | editar `backlog.md` (Ideas) | idea | `I-NNN` con contexto |
| Revisar el PR del otro | `/code-review` + lectura humana | PR | comentarios y aprobación |

## 7. Medición

Al cerrar cada slice la IA agrega una fila a `docs/metricas-adopcion.md`. Revisión a los 3 meses con las preguntas de ese archivo.
