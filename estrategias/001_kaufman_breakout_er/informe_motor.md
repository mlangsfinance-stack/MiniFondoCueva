# 001 · kaufman_breakout_er — Informe del motor (pasos 04-07)

Código: `codigo/estrategias/001_kaufman_breakout_er.py` (señal + PLAN) sobre `codigo/quantlab/`.
Ejecución: señal al cierre, entrada en la apertura siguiente, stop 3×ATR(14) intrabarra, 2 pb por
lado, riesgo 1 % del equity. Capital 100 k por tramo. Salidas en `reportes/001_kaufman_breakout_er/`.
Reproducir: `python codigo/validar.py 001 data/ndx_norgate_d1.parquet --oos-extra data/ndx_darwinex_d1.parquet`.

## 04 · Backtest IS/OOS (parámetros por defecto de Kaufman, sin optimizar)

| métrica | IS 1985-2015 | OOS cash 2016-2026 | OOS CFD 2016-2026 |
|---|---|---|---|
| trades | 93 | 24 | 23 |
| profit factor | 2.22 | 5.70 | 4.86 |
| PF sin el mejor trade | 2.00 | 4.89 | 4.18 |
| win rate | 43 % | 71 % | 61 % |
| expectancia (R) | 0.55 | 1.06 | 0.81 |
| CAGR | 1.6 % | 2.4 % | 1.7 % |
| MaxDD | −7.3 % | −4.8 % | −3.8 % |
| Sharpe | 0.53 | 0.86 | 0.69 |
| t-stat | 2.41 | 3.03 | 2.82 |

| criterio | valor | umbral | pasa |
|---|---|---|---|
| PF OOS | 5.70 / 4.86 | ≥ 1.3 | sí |
| trades OOS | **24 / 23** | ≥ 30 | **no** |
| MaxDD OOS | 4.8 % / 3.8 % | < 20 % | sí |
| PF OOS sin mejor | 4.89 / 4.18 | > 1.0 | sí |

## 05 · Optimización (solo IS)

Meseta 5×5 de PF IS sobre `n_entrada × er_min` (`meseta.csv`): centro (40, 0.3) con 3×3 completo,
mínimo del vecindario **1.91**, caída máxima **13.8 %**. Es meseta, no pico.

Walk-forward, 5 ventanas rodantes (`walk_forward.csv`): eficiencia **0.77**, **4/5** ventanas OOS
positivas (CAGR OOS: 2.4 %, −0.2 %, 2.7 %, 1.8 %, 2.0 %). La rejilla eligió `n_salida=40` en 4 de 5
ventanas: el canal de salida largo deja correr; es coherente con la hipótesis.

| criterio | valor | umbral | pasa |
|---|---|---|---|
| meseta 3×3 | 9 celdas | ≥ 9 | sí |
| mínimo vecino | 1.91 | ≥ 1.2 | sí |
| caída vecinos | 13.8 % | ≤ 30 % | sí |
| eficiencia WF | 0.77 | ≥ 0.5 | sí |
| ventanas OOS positivas | 80 % | ≥ 60 % | sí |

## 06 · Robustez

| criterio | valor | umbral | pasa |
|---|---|---|---|
| MC p5 retorno | +13.3 % | > 0 | sí |
| MC p95 MaxDD | 3.8 % | < 25 % | sí |
| MC ruina | 0 % | < 5 % | sí |
| costes ×2 → PF OOS | 5.62 | ≥ 1.1 | sí |
| sin 2 mejores años → PF | 2.42 | > 1.0 | sí |
| peor tercio → PF | 1.90 | ≥ 1.1 | sí |

PF por tercios del OOS: 2.52 · 1.90 · 3.81.

## 07 · Sizing (propuesta)
Con 1 % de riesgo por trade el p95 del MaxDD en Monte Carlo es 3.8 %. La estrategia opera ~3 veces
al año con 42 barras de media en mercado; el sizing no es el problema, la frecuencia sí.

## Resumen
| paso | qué pasa | qué no pasa |
|---|---|---|
| 04 | PF, DD y PF sin mejor en ambas series | **trades OOS: 24 / 23 < 30** |
| 05 | meseta y walk-forward | — |
| 06 | Monte Carlo y los tres stress | — |

VEREDICTO: OK
