# PROTOCOLO — el método TIS en 8 pasos

Una estrategia es una línea de producción. Entra una premisa, sale una estrategia validada.
Los pasos **naranjas** (03-06) los hace la IA. Los **verdes** (01, 02, 07, 08) son criterio:
los cierra la persona o no los cierra nadie.

| # | Paso | Quién | Agente | Entrega |
|---|---|---|---|---|
| 01 | Hipótesis | la persona | — | `hipotesis.md` (core logic: qué comportamiento explotas y por qué existe) |
| 02 | AED | IA + criterio de la persona | `investigador` | `informe_aed.md` → **puerta_hipotesis** |
| 03 | Reglas | IA | `protocolo` | `reglas.md` (entrada, salida, filtros, riesgo; blanco o negro) |
| 04 | Backtest IS/OOS | IA | `motor` | `informe_motor.md` + `reportes/` |
| 05 | Optimización | IA | `motor` | meseta, no pico |
| 06 | Robustez | IA | `motor` | stress, Montecarlo, costes reales |
| 07 | Sizing · RM | IA propone, decide la persona | `motor` + `validador` | `checklist_deploy.md` → **puerta_deploy** |
| 08 | Deploy | la persona | — | incubación en demo, servidor, monitoreo |

## Criterios de validación

> **Los umbrales que mandan son los de [MIS_REGLAS.md](MIS_REGLAS.md)**, que es el fichero de la
> persona. Lo de abajo son los valores por defecto del método TIS, que es con lo que sale el repo.
> Si los dos no coinciden, gana `MIS_REGLAS.md`. **Ningún agente los baja.**

Estos números los usa `validador` para aprobar o rechazar. Si una estrategia no llega, se archiva,
o la persona cambia el criterio en su fichero y lo anota con fecha y motivo.

### Datos
- Split fijo **IS 70 % / OOS 30 %** por fecha. La fecha de corte se fija en `reglas.md` antes de correr nada.
- **OOS se mira una sola vez.** Si el motor vuelve tras un rechazo, no re-optimiza sobre OOS.
- Costes realistas siempre: spread + comisión + slippage por activo, definidos en `reglas.md`.

> Origen de estos números: los fijó por defecto la sesión que creó el repo (2026-09-15), como
> umbrales estadísticos de mínimo de muestra y robustez habituales; no vienen de Kaufman ni de
> Raschke ni los dictó nadie de TIS. Son tuyos para cambiarlos. Cada cambio se anota en `estrategias/REGISTRO.md`.

### Paso 04 — Backtest IS/OOS
- Profit factor OOS **≥ 1.3**
- Trades OOS **≥ 30**
- Max drawdown OOS **< 20 %**
- PF OOS sin el mejor trade **> 1.0**
- **Concentración: PF OOS sin las 5 mejores operaciones > 1.0.** Es el test que más revela y el que
  menos se hace. Si la estrategia se vuelve plana al quitarlas, lo que hay son cinco eventos
  afortunados. Lo calcula `quantlab.metrics.pf_sin_top`.

### Paso 05 — Optimización
- Cada parámetro tiene rango y paso declarados en `reglas.md` (máx. 3 parámetros optimizables).
- El óptimo elegido vive en una **meseta ≥ 3×3** de la rejilla; ningún vecino cae **> 30 %** en PF.
- Walk-forward (mín. 4 ventanas): eficiencia WF **≥ 0.5** y **≥ 60 %** de ventanas OOS positivas.

### Paso 06 — Robustez
- Montecarlo (5 000 barajados de trades): p5 de retorno **> 0**, p95 de MaxDD **< 25 %**, ruina **< 5 %**.
- Stress: costes ×2 → PF OOS **≥ 1.1**. Sin los 2 mejores años → PF **> 1.0**.

### Paso 07 — Sizing · RM
- Riesgo por trade propuesto y drawdown esperado (p95 MC) con ese riesgo.
- Correlación con lo que ya opera en `docs/PORTAFOLIO.md` (si existe).

## Formato de veredicto
Cada agente cierra su turno con una última línea exacta:
`VEREDICTO: EDGE | NO_EDGE | OK | APROBADA | RECHAZADA`.
El harness lee esa línea y mueve la estrategia de fase. Sin esa línea, la estrategia se queda parada.
