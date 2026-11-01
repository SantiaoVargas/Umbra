# Diseño del Motor — Umbra

> Sub-proyecto 1 de Umbra: **el motor de escaneo**. Es una librería + CLI que
> funciona sola, se testea sola, y es el corazón sobre el que después se
> construye todo lo demás (dashboard, cuentas, billing — eso es _parking lot_,
> ver [BACKLOG.md](../BACKLOG.md)).

## Principio que atraviesa todo

**Nunca prometer más de lo que se verificó.** Cada decisión de diseño de abajo
existe para proteger eso. En concreto: un hallazgo nunca se presenta como
`critical confirmado` si el motor no lo verificó de verdad.

## Las piezas y su contrato

Cada pieza tiene **una** responsabilidad y se comunica con las demás por una
interfaz clara. Así se pueden entender y testear por separado, y dos personas
pueden trabajar en piezas distintas sin pisarse.

### 1. El guardia (allowlist) — se construye PRIMERO

- **Qué hace:** antes de tocar cualquier host, revisa si está autorizado.
- **Por qué primero:** todo lo demás depende de que exista. Un typo en una URL
  no puede terminar atacando a un tercero.
- **Contrato:** `isAllowed(url): boolean`, con normalización de host/URL.
- **Regla de oro:** _fail-closed_ — si un objetivo no está explícitamente en la
  lista, se bloquea. Nunca al revés.
- **Config:** un archivo (`umbra.config.json`) que lista los objetivos
  autorizados (host, si incluye subdominios, rutas permitidas).

### 2. El cliente HTTP observador

No es un `fetch()` cualquiera. Es un `fetch()` con control y previsibilidad —
ahí está la diferencia entre un script de hobby y un framework serio.

- **Nunca sigue redirecciones a ciegas:** valida cada salto contra la allowlist
  antes de seguirlo.
- **Respeta el `429` / `Retry-After`:** si el servidor dice "más despacio",
  hace _backoff_.
- **Rate-limit / límite de concurrencia:** no dispara cientos de requests de
  golpe.
- **Registra todo** (request + response): esa es la **evidencia** que después
  alimenta el sistema de confianza.
- **Contrato:** `request(opts): Promise<RespuestaConMetadata>`.

### 3. Los módulos de detección

- Cada módulo busca **UNA** cosa específica y no sabe nada de los demás.
- **Interfaz común:** `{ id, name, description, run(ctx): Finding[] }`.
- `ctx` les da el cliente HTTP (ya protegido por la allowlist) y los datos del
  objetivo.
- Al ser independientes: se agregan módulos nuevos sin romper los viejos, y se
  pueden correr en paralelo sin pisarse.
- **Primer módulo:** `security-headers` (cabeceras de seguridad faltantes).
  Elegido para ir primero porque la cabecera **está o no está** → confianza
  altísima, casi cero falsos positivos. Valida todo el flujo sin pelear con
  lógica compleja.

### 4. El sistema de confianza (parte del modelo de hallazgo)

Cada hallazgo (`Finding`) lleva:

| Campo | Qué es |
|---|---|
| `severity` | Qué tan grave es el impacto: `info` / `low` / `medium` / `high` / `critical` |
| `confidence` | Qué tan seguro está el motor: `confirmado` (lo verificó) vs `por-revisar` (solo encontró un patrón sospechoso) |
| `evidence` | La prueba (request/response) de por qué lo marcó |
| `remediation` | Cómo arreglarlo |

- **Regla:** no se emite un `critical` como `confirmado` sin una verificación
  real. Un patrón sospechoso va como `por-revisar`.

### 5. El generador de reporte

- Junta todos los `Finding` y los convierte en algo que un humano de negocio
  puede leer — no un JSON crudo.
- **Separa claramente** "esto SÍ es un problema confirmado" de "esto hay que
  mirarlo".
- Da un **plan priorizado**: qué arreglar primero.
- **Formato:** Markdown primero (legible y versionable en Git). JSON / HTML más
  adelante si hace falta.

### 6. El CLI (la puerta de entrada) — se construye ÚLTIMO

- Conecta todo: lee la config, corre los módulos en orden, llama al reporte.
- Es la pieza más simple, pero va al final porque depende de que todo lo
  anterior exista.
- Ejemplo de uso: `umbra scan --config umbra.config.json`.

## Orden de construcción (y por qué)

No se empieza por el CLI ni por el reporte bonito. Se empieza por la **seguridad
del sistema mismo** (allowlist + cliente HTTP), porque si esa base está mal, nada
de lo que se construya encima sirve.

```
allowlist → cliente HTTP → modelo de hallazgo/confianza →
  módulo security-headers (de punta a punta) → reporte → CLI
```

## Cómo lo testeamos

- **TDD:** cada pieza con tests antes que el código de implementación.
- **App vulnerable local:** un servidor mínimo local, con cabeceras de seguridad
  faltantes a propósito, para testear los módulos de forma segura — sin apuntar
  a nada externo.
