# Diseño del Motor — Umbra

> Sub-proyecto 1 de Umbra: **el motor de escaneo**. Es un **core en Python puro**
> (una librería que funciona y se testea sola) envuelto por una **API (FastAPI)**.
> Más adelante, un **frontend en React** consume esa API. El dashboard, las
> cuentas y el billing son _parking lot_ (ver [backlog.md](../backlog.md)).

## Stack

- **Backend / motor:** Python 3.11+ (probado con 3.14).
- **API:** FastAPI (documentación automática en `/docs`).
- **HTTP:** httpx (async, control de concurrencia).
- **Modelos:** Pydantic (validación fuerte).
- **Tests:** pytest.
- **Frontend:** React (fase posterior).

## Principio que atraviesa todo

**Nunca prometer más de lo que se verificó.** Cada decisión de diseño existe
para proteger eso. En concreto: un hallazgo nunca se presenta como
`critical confirmado` si el motor no lo verificó de verdad — y eso se hace
cumplir con código (un validador de Pydantic), no con buena voluntad.

## Estructura de carpetas

```
src/umbra/
  core/            # EL MOTOR — Python puro, no sabe nada de la API ni de React
    allowlist.py       # el guardia
    http_client.py     # cliente observador (httpx)
    findings.py        # modelo Pydantic: Finding, Severity, Confidence  ✅
    report.py          # generador de reporte
    modules/
      header_checker.py  # primer módulo
  api/             # FastAPI — capa fina que envuelve al core
    main.py            # app + endpoints  (/health ✅)
    schemas.py         # request/response (Pydantic)
tests/             # pytest
frontend/          # React (después)
```

El `core/` es el motor; `api/` es el tablero y los pedales; `frontend/` es la
carrocería. Primero que el motor ande, después lo demás.

## Las piezas y su contrato

Cada pieza tiene **una** responsabilidad y se comunica por una interfaz clara.
Así se entienden y testean por separado, y dos personas trabajan en piezas
distintas sin pisarse.

### 1. El guardia (allowlist) — se construye PRIMERO

- **Qué hace:** antes de tocar cualquier host, revisa si está autorizado.
- **Por qué primero:** todo lo demás depende de que exista. Un typo en una URL
  no puede terminar atacando a un tercero.
- **Contrato:** `is_allowed(url) -> bool`, con normalización de host/URL.
- **Regla de oro:** _fail-closed_ — si un objetivo no está explícitamente en la
  lista, se bloquea.
- **Config:** un archivo (`umbra.config.json` o similar) con los objetivos
  autorizados.

### 2. El cliente HTTP observador (httpx)

No es un pedido HTTP cualquiera. Es un cliente con control y previsibilidad —
ahí está la diferencia entre un script de hobby y un framework serio.

- **Nunca sigue redirecciones a ciegas:** valida cada salto contra la allowlist.
- **Respeta el `429` / `Retry-After`:** si el servidor dice "más despacio",
  hace _backoff_.
- **Rate-limit / límite de concurrencia:** no dispara cientos de pedidos de golpe.
- **Registra todo** (request + response): esa es la **evidencia** que alimenta
  al sistema de confianza.

### 3. Los módulos de detección

- Cada módulo busca **UNA** cosa específica y no sabe nada de los demás.
- **Interfaz común:** una clase/función con `id`, `name`, `description` y un
  método `run(ctx)` que devuelve una lista de `Finding`.
- `ctx` les da el cliente HTTP (ya protegido por la allowlist) y el objetivo.
- Al ser independientes: se agregan módulos nuevos sin romper los viejos, y se
  pueden correr en paralelo (ideal para `async`).
- **Primer módulo:** `header_checker` (cabeceras de seguridad faltantes).
  Elegido para ir primero porque la cabecera **está o no está** → confianza
  altísima, casi cero falsos positivos.

### 4. El sistema de confianza (modelo `Finding`, Pydantic) ✅

Ya implementado en `core/findings.py`. Cada hallazgo lleva:

| Campo | Qué es |
|---|---|
| `severity` | Gravedad: `info` / `low` / `medium` / `high` / `critical` |
| `confidence` | Seguridad: `confirmado` (verificado) vs `por-revisar` (patrón) |
| `evidence` | La prueba (qué se vio en la request/response) |
| `remediation` | Cómo arreglarlo |

- **Regla dura (en código):** un `critical` no puede ser `por-revisar`.

### 5. El generador de reporte

- Junta todos los `Finding` y los convierte en algo legible para un humano.
- **Separa** "confirmado" de "por revisar".
- Da un **plan priorizado**: qué arreglar primero.
- **Formato:** Markdown primero; JSON para que la API lo devuelva.

### 6. La API (FastAPI) — la puerta de entrada, se construye ÚLTIMA

- Conecta todo: recibe un host autorizado, corre los módulos, arma el reporte y
  lo devuelve.
- Es la capa más fina, pero va al final porque depende de que todo el motor
  funcione. (Antes este rol lo tenía el CLI; ahora es la API — misma idea.)
- Endpoints previstos: uno para lanzar un escaneo y otro para traer el reporte.
- `/health` ya existe para confirmar que la API está viva.

## Orden de construcción (y por qué)

No se empieza por la API ni por el reporte bonito. Se empieza por la **seguridad
del sistema mismo** (allowlist + cliente HTTP), porque si esa base está mal, nada
de lo que se construya encima sirve.

```
allowlist → http_client (httpx) → findings/confianza ✅ →
  header_checker (de punta a punta) → report → endpoints FastAPI → React
```

## Cómo lo testeamos

- **pytest** en cada pieza; tests antes que el código cuando se pueda (TDD).
- **App vulnerable local:** un servidor mínimo local, con cabeceras faltantes a
  propósito, para testear los módulos de forma segura — sin apuntar a nada
  externo.
- La API se testea con el **TestClient** de FastAPI (en memoria, sin levantar un
  servidor real).
