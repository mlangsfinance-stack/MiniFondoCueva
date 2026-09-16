# 005 · nasdaq_sma_cross — Hipótesis

> Paso 01. Estrategia de prueba del repo: cruce de medias móviles simples, largo solo.

## Activo(s) y timeframe
NDX (Nasdaq 100 CFD, Darwinex), velas diarias (D1). Datos en `data/NDX_D1.csv`.

## Comportamiento que explotas
El Nasdaq tiene tendencias plurianuales: cuando la media rápida cruza por encima de la lenta,
los retornos posteriores son, de media, mejores que los incondicionales; cuando cruza por debajo, peores.

## Por qué existe (la razón estructural)
Momentum de índice: flujos pasivos y de tendencia que se retroalimentan, más la deriva alcista
estructural del índice tech. Quien pierde: el que vende en corrección y recompra tarde.

## Cómo se vería si es verdad
- Retorno medio diario con SMA rápida > SMA lenta claramente superior al retorno con SMA rápida < SMA lenta,
  y superior a la base incondicional, en la mayoría de años.
- El efecto se sostiene en un rango amplio de longitudes (p. ej. rápida 20-100, lenta 100-300), no en un par concreto.
- Lo mataría: que el "edge" sea solo la deriva alcista (largo siempre lo iguala) o que dependa de 1-2 años.

## Datos
`data/NDX_D1.csv` (2008-08 a 2026-07). Fecha de corte IS/OOS: **2021-01-01** (IS 2008-2020, OOS 2021-2026).

## Límites
- Largo solo. Sin apalancamiento. Una posición como máximo.
- Máximo 2 parámetros optimizables (longitudes de las medias).
- Costes: spread 1.5 puntos + slippage 1 punto por lado. Sin comisión (CFD).
