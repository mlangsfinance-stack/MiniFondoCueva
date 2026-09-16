# REGISTRO — todas las pruebas del MINI FONDO

Todo test cuenta, también los que fallan. Primeras pruebas: 2026-09-15, en tres sesiones en vivo
(laboratorio de trading sistemático · repo de agentes · agente de eficiencia). El detalle de cada
test del laboratorio (17 corridas) está en `REGISTRO_laboratorio.md`.

| ID | Estrategia | Escuela | Datos | Resultado clave | Muere en | Por qué |
|---|---|---|---|---|---|---|
| 001 | `kaufman_breakout_er` — canal 40/20 + ER ≥ 0.3, solo largos | Kaufman | NDX D1 cash IS<2016 · OOS cash + CFD | PF OOS **5.70 / 4.86** · 24 / 23 trades · DD −4.8 % | validación, criterio de muestra | Pasa TODO menos `trades OOS ≥ 30`. 2.4 trades/año no permiten distinguir edge de la década alcista. El AED ya avisó (permutación p = 0.28). Vía: multi-mercado. |
| 002 | `kaufman_mr_2dias` — reversión 2 días a favor de SMA200, ambos lados | Kaufman | NDX D1 cash + CFD | PF OOS 1.35 / 1.23 · 282 trades | validación F1 (CFD), F3 meseta, F5 stress | Frontera en cash, no pasa en CFD; la meseta es un pico (vecino 0.86); costes ×2 lo matan (1.09). |
| 003 | `raschke_holy_grail` — ADX>30, +DI>−DI, retroceso a EMA20, solo largos | Raschke | NDX D1 cash + CFD | PF OOS 1.05 / 0.56 · 13 / 23 trades | validación F1-F5 | ADX>30 en NDX diario son ~2 eventos/año; vive solo 1999-2012. Sin muestra y sin PF. |
| 004 | `raschke_ochenta_veinte` — 80-20 (Street Smarts), ambos lados | Raschke | NDX D1 cash + CFD | PF OOS 1.15 / 1.16 · 276 / 361 trades | validación F1-F5 | El lado largo tenía tendencia (p = 0.018) pero el lado corto es continuación, no reversión; junto, PF 0.74 en IS. |
| 005 | `nasdaq_sma_cross` — cruce de medias, largo solo | prueba del repo | NDX D1 CFD 2008-2026, corte 2021 | AED: retorno con cruce alcista **peor** que la base | investigación (AED) | Ruido con sesgo negativo: el cruce no mejora el "largo siempre". No pasa a reglas. |
| 006 | `nasdaq_overnight` — comprar close, vender open | prueba del repo | NDX D1 CFD 2008-2026 | overnight D1 del CFD: −6 pts/noche neto, 13 años | investigación (AED) | Con velas D1 del CFD el "overnight" es el descanso de rollover del bróker, no el overnight de mercado. Hace falta dato intradía. |
| 007 | `oro_nasdaq` | — | sin datos | hipótesis vacía | investigación (sin premisa) | El investigador para si no hay hipótesis (regla 1). Bloqueada por el agente de eficiencia; pendiente de que Mariel escriba el paso 01. |

## Sobre el criterio que rechaza la 001

`trades OOS ≥ 30` **no lo fijó Mariel**: lo puso por defecto la sesión que escribió
`docs/PROTOCOLO.md` (y el laboratorio en `validation.Criterios`), como regla estadística de mínimo
de muestra. Con 24 trades, un solo trade mueve el PF de 5.7 a 4.9 y el intervalo del win rate es
±20 puntos: el número no se puede distinguir de la deriva del índice en la década. Kaufman y
Raschke no dan ese número; es un umbral de honestidad, no de escuela.

Es un paso verde: **Mariel decide** si el umbral es 30, 50 o 20. Si lo cambia, se cambia en
`docs/PROTOCOLO.md` y se anota aquí; con 20 la 001 pasaría entera. Lo que no se hace es acortar
el canal para fabricar trades.
