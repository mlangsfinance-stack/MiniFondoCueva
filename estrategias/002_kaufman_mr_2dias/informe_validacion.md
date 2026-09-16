# E003 — mr_2dias: reversión de 2 cierres con filtro SMA200 (NDX, ambos lados)

- **Hipótesis origen:** H003 (`hipotesis/H003_mr_2dias.md`)
- **Familia de edge:** reversión de corto plazo + filtro de régimen (tendencia de fondo)
- **Estado:** `x_descartadas/` — muerta en **prototipo IS** (PF 1.05, exp 0.01 R, t 0.67) y confirmada
  en validación (Fase 1 Darwinex, Fase 3 meseta, Fase 5 stress). Tendencia débil (largo p 0.07; corto |t| 0.2).
- **Señal:** `quantlab.senales_kaufman.mr_2dias` · parámetros fijados: `{sma_n: 200, hold: 2}` ·
  config `stop_atr=2.0`
- **RESUMEN de validación:** `reportes/ndx_mr_2dias/RESUMEN.md` (2026-09-15, DESCARTADA)

## Motivo del descarte (acta)
| Fase | Check | Valor | Umbral |
|---|---|---|---|
| prototipo IS | PF / expectancia / t | 1.05 / 0.014 R / 0.67 | > 1.2 / > 0.1 R / > 2 |
| 1 IS/OOS | pf_oos_darwinex | 1.233 | ≥ 1.3 |
| 3 meseta (IS) | meseta_min_vecino | 0.860 | ≥ 1.2 |
| 5 stress | stress_sin_2_mejores_anios_pf | 1.086 | ≥ 1.1 |
| 5 stress | stress_peor_tercio_pf | 0.947 | ≥ 1.1 |

Pasaron: PF OOS Norgate 1.354 (282 trades) · MaxDD OOS −8.9 % · WF 0.65, 3/5 ventanas · MC ok ·
costes ×2 PF 1.28. PF por tercios [0.95, 1.16, 1.33]: el edge crece con el tiempo, pero en IS es plano.

Lectura: exceso de +0.10 % a 2 días contra 0.04 % de coste; el lado corto resta (258 trades, −7.9 k
en IS); 1985-1995 sin edge. El OOS 2016+ mejor que el IS es cambio de régimen, no confirmación. No se
refina aquí (sería H003.2 con tendencia nueva).

## 1. Especificación operable (tal como se validó)
| Campo | Valor |
|---|---|
| Universo y sesión | NDX cash (Norgate) · CFD NDX Darwinex, diario |
| Barra | diaria |
| Entrada | apertura siguiente a: 2 cierres consecutivos a la baja y close > SMA200 (largo) / 2 al alza y close < SMA200 (corto) |
| Stop inicial | 2 × ATR(14), intrabarra, gap en contra rellena en apertura |
| Salidas | por tiempo: la señal persiste 2 barras (un evento nuevo la renueva) / stop |
| Datos | Norgate cash 1985-2026 (IS < 2016) · Darwinex CFD 2008-2026 (OOS 2016+) |
| Costes | 2 pb por lado sobre nocional · riesgo 1 % del equity por trade |

## 2–6. Sizing, cartera, incubación, live, retirada
No aplica: no llegó a incubación.

## Historial de estado
| Fecha | De | A | Motivo |
|---|---|---|---|
| 2026-09-15 | idea | tendencia | H003 escrita; IS: largo n 1081, exceso h2 +0.10 %, p 0.07; corto n 458, t −0.2 → débil |
| 2026-09-15 | tendencia | prototipo | test inicial de pipeline; IS: PF 1.05, n 948, t 0.67 → no pasa |
| 2026-09-15 | prototipo | validación | se corre igualmente para ver el pipeline entero |
| 2026-09-15 | validación | x_descartadas | F1 Darwinex 1.23, F3 meseta 0.86, F5 stress 1.09 / 0.95 |
