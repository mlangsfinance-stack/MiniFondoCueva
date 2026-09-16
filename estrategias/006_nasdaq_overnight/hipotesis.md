# 006 · nasdaq_overnight — Hipótesis

> Paso 01. Estrategia de prueba del repo: comprar al cierre, vender en la apertura siguiente (overnight).

## Activo(s) y timeframe
NDX (Nasdaq 100 CFD, Darwinex), velas diarias (D1). Datos en `data/NDX_D1.csv`.
El `open` y `close` de cada vela diaria son la apertura y el cierre de sesión del CFD (hora servidor).

## Comportamiento que explotas
La rentabilidad del Nasdaq se concentra en el tramo **overnight** (cierre → apertura siguiente);
el tramo intradía (apertura → cierre) aporta poco o nada. Comprar al cierre y vender en la
apertura captura la deriva sin exponerse a la sesión.

## Por qué existe (la razón estructural)
Efecto overnight documentado en índices US: noticias y resultados se publican fuera de horario,
los market makers cobran prima por el riesgo de gap, y los flujos institucionales operan en subasta
de apertura. Quien pierde: quien vende en el cierre para "dormir tranquilo".

## Cómo se vería si es verdad
- Retorno medio de `open[t+1]/close[t] - 1` positivo y significativamente mayor que `close[t]/open[t] - 1`,
  consistente en la mayoría de años.
- Suma acumulada overnight ≫ suma acumulada intradía.
- Lo mataría: que el retorno overnight medio sea menor que el spread+slippage de dos lados, o que
  desaparezca al quitar los 2 mejores años.

## Datos
`data/NDX_D1.csv` (2008-08 a 2026-07). Fecha de corte IS/OOS: **2021-01-01** (IS 2008-2020, OOS 2021-2026).

## Límites
- Largo solo. Sin apalancamiento. Una posición, todos los días (o con un único filtro simple si el AED lo justifica).
- Máximo 1 parámetro optimizable.
- Costes: spread 1.5 puntos + slippage 1 punto por lado. Sin comisión (CFD). **Los costes son el punto crítico
  de esta estrategia: si no los supera con margen, no hay edge.**
