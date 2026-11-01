# Umbra 🛡️

Umbra es una herramienta de **escaneo de seguridad para aplicaciones web y APIs**.
Automatiza la parte mecánica y repetitiva de buscar oportunidades de mejora de
seguridad, para que una persona revise solo lo que de verdad importa.

> **No reemplaza el criterio humano — lo multiplica.**

## Principio rector

**Nunca prometer más de lo que se verificó.** Cada hallazgo no dice solo qué tan
grave es (severidad), sino también **qué tan seguro está Umbra de que es real**
(confianza). Un reporte honesto que diga "2 confirmados y 8 para revisar" vale
más que uno que grite "10 críticos" y mienta. Esa honestidad es el producto.

## Para quién

- Quien construye apps (incluida la gente que "vibecodea") y quiere conocer a
  fondo las oportunidades de mejora de lo que publicó.
- Quien ya tiene experiencia y quiere un escaneo serio, sin falsos positivos que
  le hagan perder tiempo.

## ⚠️ Uso autorizado únicamente

Umbra solo debe apuntar a sistemas **de los que seas dueño o para los que tengas
autorización explícita y por escrito**. Por eso lo primero que hace, antes de
tocar cualquier host, es validar una **allowlist**: si un objetivo no está
explícitamente autorizado, Umbra no le pega. Escanear sistemas de terceros sin
permiso es ilegal.

## Estado

En diseño / arranque. La definición completa está en:

- [docs/DISENO-MOTOR.md](docs/DISENO-MOTOR.md) — arquitectura del motor.
- [BACKLOG.md](BACKLOG.md) — tareas por fases.

## Stack

Node.js + TypeScript.
