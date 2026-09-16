# 001 · kaufman_breakout_er — Reglas (paso 03)

Especificación blanco o negro. Un programador la implementa sin hacer una pregunta.

## Activo, timeframe, sesión
NDX (Nasdaq 100), velas diarias. Serie principal: índice cash. Serie de contraste: CFD NDX del
broker. Zona horaria: la de cada serie (cierre de sesión US); no se mezclan barras entre series.

## Datos y corte
`data/ndx_norgate_d1.parquet` (cash, 1985-2026) y `data/ndx_darwinex_d1.parquet` (CFD, 2008-2026).
Corte IS/OOS: **2016-01-01**. IS = cash < 2016. OOS = ≥ 2016 en cash **y** en CFD.

## Entrada
Al cierre de la barra t, si `close[t] > max(high[t-40 .. t-1])` **y** `ER(10)[t] ≥ 0.3`
→ largo en la **apertura de t+1**. `ER(n) = |close[t] − close[t−n]| / Σ|close[i] − close[i−1]|` sobre las
n barras. Solo largos. Una posición como máximo; si ya hay posición, la señal no hace nada.

## Salida
1. **Canal:** al cierre de t, si `close[t] < min(low[t-20 .. t-1])` → cierre en la apertura de t+1.
2. **Stop catastrófico:** `precio_entrada − 3 × ATR(14)` calculado al cierre previo a la entrada,
   evaluado intrabarra con el low. Si la barra abre por debajo del stop, se rellena en la apertura
   (gap en contra, nunca a favor).
3. Si coinciden en la misma barra, manda el stop (se ejecuta antes, intrabarra).

## Filtros
Solo el ER ≥ 0.3 de la entrada. Lo apoya la tabla de rango del AED (p(supera alto) 0.88 vs 0.71).
Ningún filtro más: el AED no vio otro.

## Riesgo por trade
1 % del equity actual hasta el stop: `unidades = 0.01 × equity / (3 × ATR14)`. Fixed fractional.

## Costes
2 pb (0.02 %) por lado sobre el nocional: ≈ spread/2 + slippage sobre NDX ~8 000. Sin comisión (CFD).
Toda métrica se reporta neta de costes.

## Parámetros
| Parámetro | Defecto | Rango | Paso | Optimizable |
|---|---|---|---|---|
| `n_entrada` | 40 | 20-60 | 10 | sí |
| `er_min` | 0.3 | 0.1-0.5 | 0.1 | sí |
| `n_salida` | 20 | 10-40 | (10, 20, 40) | sí, solo en walk-forward |
| `er_n` | 10 | — | — | no: valor de Kaufman |
| `stop_atr` | 3.0 | — | — | no: es catastrófico, no de gestión |

Los defectos son los de Kaufman; no salen de buscar. Meseta 5×5 sobre `n_entrada × er_min`.

## Criterios de validación
Los de `docs/PROTOCOLO.md`, sin relajar:
- 04: PF OOS ≥ 1.3 · trades OOS ≥ 30 · MaxDD OOS < 20 % · PF OOS sin mejor trade > 1.0 — **en las dos series**.
- 05: meseta 3×3 con ningún vecino < 1.2 ni caída > 30 % · walk-forward ≥ 4 ventanas, eficiencia ≥ 0.5, ≥ 60 % OOS positivas.
- 06: MC 5 000: p5 retorno > 0, p95 MaxDD < 25 %, ruina < 5 % · costes ×2 PF ≥ 1.1 · sin 2 mejores años PF > 1.0.

## Lo que NO se hace
Cortos. Acortar `n_entrada` para fabricar trades. Tocar el OOS más de una vez. Apalancar por encima
del 1 % de riesgo. Cambiar los defectos de Kaufman después de ver el OOS.

VEREDICTO: OK
