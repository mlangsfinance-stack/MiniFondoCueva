# E001 — holy_grail (Holy Grail de Raschke, solo largos, NDX diario)

- **Hipótesis origen:** H001 (`hipotesis/H001_holy_grail.md`)
- **Familia de edge:** continuación
- **Estado:** `x_descartadas/` — muerta en **Fase 1 (IS/OOS)**; además falla F2, F3 y F5. Ya llegaba
  marcada como "tendencia débil" (n=71, p=0.21) y sin pasar la puerta de prototipo (n=64, t=1.09).
- **Señal:** `quantlab.senales_raschke.holy_grail` · parámetros fijados: `{adx_min: 30, ema_n: 20, hold: 5}`
  · config `{stop_atr: 2.0, max_barras: 5}`
- **RESUMEN de validación:** `reportes/ndx_holy_grail/RESUMEN.md` (2026-09-15, **DESCARTADA**)

## 1. Especificación operable
| Campo | Valor |
|---|---|
| Universo y sesión | NDX cash (Norgate) para IS/OOS; CFD NDX Darwinex como OOS real (2016+) |
| Barra | diaria |
| Entrada | apertura de la barra siguiente a la señal, orden a mercado. Señal: ADX(14) > 30, +DI > −DI, low ≤ EMA20 y close > EMA20 (solo largos) |
| Stop inicial | k = 2.0 × ATR(14) |
| Salidas | por tiempo (5 barras) / por señal (ventana `hold` agotada) / por stop |
| Gaps | fill en apertura si abre más allá del stop |
| Datos | Norgate NDX 1985–2026 (antes de ~2000 el open es el cierre previo); Darwinex 2008–2026 |

## 2. Motivo del descarte (acta)
Tendencia IS: n=71 < 100, exceso h=5 +0.34 % pero t=1.92 y p=0.21 → no pasa.
Prototipo IS: n=64, PF 1.40, exp 0.10 R, t=1.09, 60 % años positivos → no pasa (n, t).
Validación (una sola pasada, `--rapido`):

| fase | check | valor | umbral |
|---|---|---|---|
| 1 | pf_oos (Norgate 2016+) | 1.049 | ≥ 1.30 |
| 1 | trades_oos | 13 | ≥ 30 |
| 1 | pf_sin_mejor_oos | 0.748 | > 1.00 |
| 1 | pf_oos_darwinex | 0.561 | ≥ 1.30 |
| 1 | trades_oos_darwinex | 23 | ≥ 30 |
| 1 | pf_sin_mejor_oos_darwinex | 0.439 | > 1.00 |
| 2 | wf_eficiencia | 0.369 | ≥ 0.50 |
| 3 | meseta_min_vecino | 1.181 | ≥ 1.20 |
| 5 | stress_costes_x2_pf_oos | 1.004 | ≥ 1.10 |
| 5 | stress_sin_2_mejores_anios_pf | 1.066 | ≥ 1.10 |
| 5 | stress_peor_tercio_pf | 0.788 | ≥ 1.10 |

PF por tercios de la muestra: 0.79 / 2.53 / 1.15 — el edge vive solo en el tercio central
(1999–2012). En OOS hay 13 trades en 10 años (Norgate) y 23 en Darwinex con PF 0.56.

## 3. Lección
Con ADX(14) > 30 el NDX diario genera ~2 eventos/año: no hay muestra para decidir nada y el OOS
es anecdótico. El retroceso a la EMA20 con tendencia fuerte tiene el signo correcto (exceso
positivo en todos los horizontes ≥ 2) pero no la potencia estadística. Si se retoma: H001.1 con
ADX 25 (más eventos) y/o varios índices agregados (SP500 + NDX + DAX), en tendencia primero.

## Historial de estado
| Fecha | De | A | Motivo |
|---|---|---|---|
| 2026-09-15 | idea | tendencia | ficha H001 completada sobre NDX IS |
| 2026-09-15 | tendencia | prototipo | tendencia débil (n=71, p=0.21); se pasa por ser test inicial de pipeline |
| 2026-09-15 | prototipo | validación | no pasa puerta (n=64, t=1.09); se valida igualmente para ver el pipeline entero |
| 2026-09-15 | validación | x_descartadas | DESCARTADA en Fase 1: PF OOS 1.05 Norgate / 0.56 Darwinex, 13 y 23 trades |
