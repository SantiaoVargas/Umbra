# Spec 001: Guardia (allowlist fail-closed)

**Historia:** 001 Como dueño de un sistema quiero que Umbra solo escanee objetivos que autoricé explícitamente, para que un typo o un host ajeno nunca reciban tráfico
**Dominio:** guardia · **Responsable:** Santiago · **Revisor/a:** Iker · **Fecha:** 2026-11-02 · **Estado:** borrador
**Depende de:** 000 · **Ficha de dominio:** `docs/architecture/dominios/guardia.md`

Marcas de evidencia: **observado** (ruta/línea), **<persona>** (fecha), **hipótesis**.

## Alcance
- Entra:
  - Archivo de configuración `umbra.config.json` con la lista de objetivos autorizados.
  - Carga y validación de la config, con errores claros; una config inválida impide arrancar.
  - Función `is_allowed(url) -> bool`, fail-closed, único punto de decisión.
  - Normalización del host (mayúsculas, punto final) y comparación segura por partes, nunca por texto.
  - Tests unitarios, incluidos los casos hostiles de la sección Flujo.
- **No entra:**
  - Hacer requests HTTP (historia 002). La 001 no toca la red.
  - Revalidar cada salto de redirección: eso lo hace el cliente HTTP (002) llamando a `is_allowed` en cada salto. Aquí solo se garantiza que `is_allowed` sirve para eso.
  - Comodines (`*.miempresa.com`), rangos de IP, CIDR, resolución DNS.
  - Interfaz o endpoint para editar la lista.

## Decisiones tomadas
| Decisión | Resultado | Fuente |
|---|---|---|
| Formato de la lista | Archivo `umbra.config.json` | Santiago (2026-11-02) |
| Subdominios | Solo si la entrada tiene `incluir_subdominios: true` (por defecto `false`) | Santiago (2026-11-02) |
| Identidad del objetivo | host + puerto. Sin puerto en la entrada = solo 80 y 443 | Santiago (2026-11-02) |

## Flujo
1. El arranque lee `umbra.config.json` y construye un `Allowlist`. Si algo está mal, falla con un mensaje claro y Umbra no arranca.
2. Cualquier código que quiera pedir una URL llama `allowlist.is_allowed(url)`.
3. `is_allowed` hace, en orden, y devuelve `False` en el primer fallo:
   1. La URL se puede parsear y el esquema es `http` o `https`.
   2. Se extrae el **host real** (con un parser, no con búsquedas de texto) y se normaliza a minúsculas sin punto final.
   3. Se calcula el puerto efectivo: el explícito, o 80/443 según el esquema.
   4. Se recorre la lista. Una entrada autoriza si el host es **igual**, o (con `incluir_subdominios: true`) si el host termina en `"." + entrada.host`.
   5. Además el puerto efectivo debe estar permitido por la entrada (ver Contrato).
4. Si ninguna entrada autoriza → `False`. Nunca lanza excepción por una URL rara: una URL ilegible es `False`.

Casos hostiles que **deben** bloquearse (con la lista `[{"host": "example.com", "incluir_subdominios": true}]`):

| URL | Resultado | Por qué |
|---|---|---|
| `https://tienda.example.com` | permite | subdominio pedido explícitamente |
| `https://example.com:8080` | bloquea | puerto no autorizado |
| `https://evil-example.com` | bloquea | contiene el texto pero no es subdominio |
| `https://example.com.evil.test` | bloquea | el host real es `evil.test` |
| `https://example.com@evil.test/` | bloquea | lo anterior a `@` es usuario, el host real es `evil.test` |
| `https://EXAMPLE.com.` | permite | mayúsculas y punto final se normalizan |
| `ftp://example.com` | bloquea | esquema no permitido |
| `no es una url` | bloquea | ilegible → fail-closed |

## Contrato
Archivo: `umbra.config.json`

```json
{
  "objetivos": [
    { "host": "example.com" },
    { "host": "api.example.com", "puerto": 8000 },
    { "host": "tienda.example.com", "incluir_subdominios": true }
  ]
}
```

- `host` (obligatorio): solo el nombre, sin esquema, sin ruta, sin puerto, sin `*`.
- `puerto` (opcional, 1–65535): si está, **solo** ese puerto queda autorizado. Si falta, 80 y 443.
- `incluir_subdominios` (opcional, por defecto `false`).

Módulo nuevo: `src/umbra/core/allowlist.py` (hipótesis de nombres, se ajustan con los tests):
- `Objetivo` (modelo Pydantic): valida los campos de arriba al cargar.
- `Allowlist`: se construye desde una lista de `Objetivo`; expone `is_allowed(url: str) -> bool`.
- `cargar_config(ruta) -> Allowlist`: lee el JSON y lanza un error propio con mensaje claro si falla.

Errores de config que impiden arrancar: archivo inexistente, JSON inválido, falta `objetivos`, lista vacía, `host` con esquema/ruta/puerto/`*`, puerto fuera de rango.

## Honestidad: severidad y confianza
No aplica: la historia no produce hallazgos (`Finding`).

## Seguridad del producto
- P1 Allowlist: **aplica, es la implementación.** `is_allowed` es el único punto de decisión. La 002 debe llamarlo antes de cada request y en cada redirección; ningún módulo recibe un cliente crudo.
- P3 Tests: aplica. Se usan solo nombres reservados para documentación (`example.com`, `.test`), y la 001 no hace requests, así que ningún test toca la red.
- P4 Peticiones: no aplica (no hay peticiones).
- P5 Secretos: la config solo contiene hosts. Si el archivo real de un usuario se coloca en el repo, va a `.gitignore`; se versiona únicamente un ejemplo (`umbra.config.example.json`).

## Decisiones abiertas
- ¿La config real (`umbra.config.json`) va al `.gitignore` y se versiona un `umbra.config.example.json`? Propuesta: sí. **Iker, ¿de acuerdo?**
- IPs literales (`http://203.0.113.5`): propuesta de esta spec: se tratan como un host cualquiera, solo coincidencia exacta y nunca `incluir_subdominios`. Falta confirmar con Iker.
- Ruta de la config: propuesta: `umbra.config.json` en el directorio de trabajo, ruta distinta por parámetro. Variable de entorno queda para después.

## Criterios de aceptación (booleanos)
- [ ] CA1: un host fuera de la lista nunca pasa (`test_host_fuera_de_lista_se_bloquea`).
- [ ] CA2: todos los casos hostiles de la tabla dan el resultado indicado (tests parametrizados).
- [ ] CA3: una config inválida lanza un error con mensaje claro, para cada error listado en Contrato.
- [ ] CA4: sin `incluir_subdominios`, un subdominio se bloquea; con `true`, pasa.
- [ ] CA5: sin `puerto`, solo pasan 80 y 443; con `puerto`, solo ese.
- [ ] CA6: `is_allowed` nunca lanza excepción ante entradas raras (vacío, `None`-like, basura).
- [ ] CA7: `pytest` y `ruff check .` pasan.

## Riesgos y reversión
- Riesgo: un bug de comparación autoriza hosts ajenos. Mitigación: comparar por partes con un parser y tests hostiles obligatorios.
- Riesgo: la 002 olvide validar redirecciones. Mitigación: queda como criterio de la spec 002.
- Reversión: revert del PR; no hay datos persistidos ni efectos en la red.
