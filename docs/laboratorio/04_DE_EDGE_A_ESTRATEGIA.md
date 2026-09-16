# 04 — De edge validado a estrategia operable (tramos 75–100)

Un edge validado todavía no se puede operar. Falta decidir cuánto, con qué, junto a qué, cómo
se ejecuta y cuándo se apaga. Eso es la **estrategia**; se escribe en `docs/laboratorio/PLANTILLA_ESTRATEGIA_laboratorio.md`.

## 1. Especificación completa (75–85)

Todo lo que un tercero necesitaría para operarla igual que tú, sin preguntarte nada:

- **Universo y sesión**: activos concretos, horario, zona horaria de la plataforma real.
- **Señal**: nombre de la función + parámetros fijados en validación. No se cambian en live.
- **Órdenes**: tipo (mercado en apertura / stop / límite), qué pasa con gaps, qué pasa si no hay fill.
- **Stop y salidas**: stop inicial (k·ATR), salida por señal, salida por tiempo. Nada discrecional.
- **Sizing** (ver §2).
- **Límites**: máximo de posiciones simultáneas, exposición máxima por activo y total, pérdida diaria/semanal que para la estrategia.
- **Datos**: fuente, cómo se limpian, qué se hace si faltan barras.
- **Plan de retirada** (ver §5) escrito antes de empezar.

## 2. Sizing

Principio: el tamaño lo decide el riesgo hasta el stop, no la convicción.

- **Fixed fractional**: unidades = equity × riesgo_pct / distancia_al_stop. Con `riesgo_pct` entre
  0.5 % y 1 % por trade para una estrategia; menos si hay varias correlacionadas.
- **Objetivo de volatilidad** (alternativa para señales sin stop): nocional tal que la
  volatilidad anualizada de la posición ≈ objetivo (p. ej. 10 %).
- **Restricción por drawdown**: el MaxDD p95 del Monte Carlo escalado por el sizing tiene que
  quedar por debajo del DD que estás dispuesta a aguantar de verdad. Si el p95 es 25 % y tu
  límite real es 15 %, el sizing baja a 0.6× — no se "aguanta más".
- Kelly y f óptima: se calculan para saber dónde está el techo, y se opera a **¼–½** de eso. Nunca al óptimo.

## 3. Cartera (Simons: agregar edges)

Una estrategia nueva se acepta en cartera si:
- Correlación de retornos mensuales con cada estrategia existente < 0.5 (ideal < 0.3).
- Aporta: el MAR (CAGR/MaxDD) de la cartera con ella es ≥ al de la cartera sin ella.
- No comparte el mismo modo de fallo (dos estrategias de breakout en índices caen juntas en rango).
- Asignación inicial: igual riesgo (cada estrategia aporta la misma volatilidad al conjunto); se
  revisa trimestralmente, no cada mes malo.

## 4. Incubación (85–95)

Paper o forward con ejecución real en la plataforma donde va a vivir. Se sale cuando:
- ≥ 3 meses **o** ≥ 30 trades, lo que llegue después.
- El equity real cae dentro del cono Monte Carlo p5–p95 del RESUMEN.md.
- Paridad: los trades de la plataforma coinciden con los del motor (mismo nº de trades ±1,
  PnL ±5 %); si no, el motor no modela bien la ejecución y se arregla **el motor**.
- Costes reales medidos ≤ costes modelados. Si son mayores, se re-corre la Fase 5 con los reales.

## 5. Live y retirada (95–100)

Mensual, en la ficha de la estrategia:
- PF rodante (últimos 30 trades) y equity contra el cono MC.
- Salud: 🟢 dentro del cono · 🟡 por debajo de p25 dos meses seguidos → tamaño ½ · 🔴 por debajo de p5
  **o** DD > p95 MC → **parada**, no "espera a ver".
- La regla de retirada se decidió antes de empezar; no se renegocia con la posición abierta.
- Retirada no es descarte: la ficha va a `x_descartadas/` con motivo `retirada live` y los números.
  Si el edge vuelve (régimen), se re-valida desde Fase 1 con los datos nuevos.

## 6. Playbook diario (Raschke)

Cuando hay estrategias en live, el proceso diario es fijo y corto:
1. **Pre-mercado**: datos actualizados, señales generadas, órdenes revisadas, eventos del día (noticias, vencimientos) anotados.
2. **Sesión**: se ejecuta lo que dice la señal. Ninguna decisión discrecional sobre una posición sistemática.
3. **Post-mercado**: reconciliar fills contra el motor; anotar cualquier desviación; una línea en el diario sobre lo que hizo el mercado.
4. **Semanal**: revisar el diario buscando **hipótesis nuevas** — es la fuente principal del tramo 0–10.
