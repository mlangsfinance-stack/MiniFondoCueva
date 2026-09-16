# Registro de hipótesis y tests

**Todo test cuenta**, pase o no. La columna `nº test` es global: con N tests hechos, el p-valor
que hace falta para creer algo es ≈ 0.05 / N. Este fichero es la memoria del laboratorio y el
antídoto contra la minería de datos.

Estados: `idea` · `tendencia` · `prototipo` · `validacion` · `estrategia` · `descartada(tramo)`

Datos NDX: `ndx_norgate_d1` (índice cash 1985–2026) · `ndx_darwinex_d1` (CFD 2008–2026).
IS = Norgate < 2016-01-01 · OOS = 2016+ en ambas. Costes 2 pb/lado, riesgo 1 %.
**Tests acumulados: 16** → p-valor exigido para creer algo nuevo ≈ 0.003.

| nº test | Fecha | Hipótesis | Variante / qué se probó | Datos | Resultado (métrica clave) | Estado |
|---|---|---|---|---|---|---|
| 1 | 2026-09-15 | H001 Holy Grail | evento base, ADX>30, h=5 | sintético placebo (autocorr=0) | exceso ≈ 0, p=0.74 (esperado en ruido) | idea |
| 2 | 2026-09-15 | — kama_tendencia (ejemplo de pipeline) | validación 5 fases, n=10, er_min=0.3 | sintético autocorr=0.15 | PF OOS 1.15 · falla F1, F3, F5 | descartada(validación) — ejemplo, no hipótesis real |
| 3 | 2026-09-15 | H001 Holy Grail (solo largos) | tendencia: ADX(14)>30, +DI>−DI, low≤EMA20<close, h=5 | Norgate NDX IS | n=71, exceso h5 +0.34 %, t=1.92, p=0.209 | tendencia débil (no pasa) |
| 4 | 2026-09-15 | H001 Holy Grail (solo largos) | prototipo IS adx30/ema20/hold5, stop 2 ATR | Norgate NDX IS | n=64, PF 1.40, exp 0.10 R, t=1.09 | prototipo (no pasa) |
| 5 | 2026-09-15 | H001 Holy Grail (solo largos) | validación 5 fases `--rapido`, grid 9, meseta adx_min×ema_n | Norgate IS/OOS · Darwinex OOS | PF OOS 1.05 (13 tr) / Darwinex 0.56 (23 tr) · falla F1, F2, F3, F4, F5 | descartada(validación F1) |
| 6 | 2026-09-15 | H004 80-20 | tendencia lado largo: open≥80 % rango, close≤20 %, rango≥ATR(10), h=1 | Norgate NDX IS (+ sub 2000–2015) | n=570, exceso h1 +0.14 %, t=2.21, p=0.018 (2000+: +0.27 %, p=0.002) | tendencia (pasa) |
| 7 | 2026-09-15 | H004 80-20 | tendencia lado corto: espejo, h=1 | Norgate NDX IS (+ sub 2000–2015) | n=630, exceso h1 +0.12 % con signo contrario (continuación), t=3.10; 2000+: −0.04 %, p=0.61 | descartada(tendencia) lado corto |
| 8 | 2026-09-15 | H004 80-20 (ambas direcciones) | prototipo IS pct0.2/hold1/rango≥1.0 ATR, stop 1.5 ATR | Norgate NDX IS | n=1153, PF 0.74, exp −0.04 R, t=−3.77 (corto PF 0.57, largo 0.95) | prototipo (no pasa) |
| 9 | 2026-09-15 | H004 80-20 (ambas direcciones) | validación 5 fases `--rapido`, grid 9, meseta pct×atr_mult_rango | Norgate IS/OOS · Darwinex OOS | PF OOS 1.15 (276 tr) / Darwinex 1.16 (361 tr) · falla F1, F2, F3, F4, F5 | descartada(validación F1) |
| 10 | 2026-09-15 | H002 breakout_er | tendencia: canal 40 + ER(10)≥0.3, h=5 | Norgate NDX IS | n=687, exceso h5 +0.08 %, t=3.83 (vs cero), p=0.277 | tendencia débil (deriva, no edge) |
| 11 | 2026-09-15 | H002 breakout_er | prototipo IS: 40/20, ER 10/0.3, stop 3 ATR, solo largos | Norgate NDX IS | n=93, PF 2.22, exp 0.55 R, t=2.41 · falla n<100 | prototipo → validación |
| 12 | 2026-09-15 | H002 breakout_er | validación 5 fases `--rapido`, OOS Norgate + Darwinex | Norgate IS/OOS · Darwinex OOS | PF OOS 5.70 / 4.86 · falla solo F1 trades OOS 24 / 23 | descartada(validación F1 — muestra) |
| 13 | 2026-09-15 | H003 mr_2dias | tendencia: largo baja2 & >SMA200, corto sube2 & <SMA200, h=2 | Norgate NDX IS | largo n 1081, exceso +0.10 %, p 0.071 · corto n 458, exceso −0.15 %, t −0.23 | tendencia débil |
| 14 | 2026-09-15 | H003 mr_2dias | prototipo IS: SMA200, hold 2, stop 2 ATR, ambos lados | Norgate NDX IS | n=948, PF 1.05, exp 0.01 R, t=0.67 | prototipo (no pasa) |
| 15 | 2026-09-15 | H003.1 mr_2dias | prototipo IS solo largos (informativo, sin validar) | Norgate NDX IS | n=690, PF 1.12, exp 0.03 R, t=1.26 | descartada(prototipo) |
| 16 | 2026-09-15 | H003 mr_2dias | validación 5 fases `--rapido`, OOS Norgate + Darwinex | Norgate IS/OOS · Darwinex OOS | PF OOS 1.35 / 1.23 · falla F1 Darwinex, F3 meseta 0.86, F5 stress 1.09 / 0.95 | descartada(validación) |
| 17 | 2026-09-15 | — reporte visual Kaufman+Raschke (breakout_er, mr_2dias, kama_tendencia, holy_grail, ochenta_veinte) | backtest con params por defecto, sin optimizar; meseta PF en IS; equity/DD/heatmaps | NDX Norgate, IS<2016, 2 pb | kama_tendencia en NDX por primera vez: PF IS 0.94 · OOS 0.89 · DD −51 %; el resto reproduce los RESUMEN | informe en reportes/kaufman_raschke/ — no cambia veredictos |

Nota 2026-09-15: las validaciones 5, 9, 12 y 16 se re-corrieron tras cambiar la Fase 4 de
permutación a bootstrap (el p5 del retorno era invariante al orden). Veredictos sin cambio;
Holy Grail y 80-20 pasan a fallar también F4 (p5 −4.8 % y −6.4 %).

## Descartadas: qué se aprendió

| Hipótesis | Tramo donde murió | Números | Lección |
|---|---|---|---|
| H001 Holy Grail (largos) | validación F1 (muestra y PF) | n OOS 13/23 · PF OOS 1.05 / 0.56 · PF tercios 0.79/2.53/1.15 | ADX>30 en NDX diario = ~2 eventos/año; vive solo 1999–2012. Sin muestra no hay decisión: ADX 25 o agregar SP500+NDX+DAX como H001.1, tendencia primero |
| H002 breakout_er (largos) | validación F1 (solo muestra) | n OOS 24/23 · PF OOS 5.7/4.9 · meseta plana · stress OK | 3 trades/año no se valida en un solo índice; ir a multi-mercado con la misma regla, nunca acortar el canal para fabricar trades. La tendencia dijo que el exceso a 5–10 d es deriva del NDX |
| H003 mr_2dias (ambos) | prototipo IS | PF 1.05, t 0.67 · exceso 0.10 % vs coste 0.04 % | Reversión 2 días en NDX diario = tamaño del coste; el corto resta; 1985–95 sin edge. OOS mejor que IS es régimen, no confirmación |
| H004 80-20 (ambos) | tendencia (corto) / prototipo (conjunto) | largo p=0.018 ✓ · corto continuación · PF IS 0.74, OOS 1.15 | Edge real pero asimétrico: solo largos. +0.2 % a 1 día no sobrevive a stop intradía + costes. Pre-2000 el open cash de Norgate es artificial (= cierre previo): usar 2000+ o Darwinex. H004.1: solo largos, salida al cierre de Día 2, stop en extremo de Día 1 |
