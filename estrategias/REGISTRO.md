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
| 007 | `oro_nasdaq` | — | sin datos | hipótesis vacía | investigación (sin premisa) | El investigador para si no hay hipótesis (regla 1). Bloqueada por el agente de eficiencia; pendiente de que se escriba el paso 01. |

## Cómo rehacer estos números

Las cuatro con acta (001-004) tienen su señal en `codigo/estrategias/<ID>_<nombre>.py` y se
revalidan con un comando, sobre tus propios datos diarios (`fecha, open, high, low, close`):

```
python codigo/validar.py 002 data/TU_NDX_D1.csv --corte 2016-01-01
```

Sin datos, `--sintetico` corre el placebo: sobre ruido las cuatro **tienen que** fallar. Los datos
del NDX usados aquí (Norgate y Darwinex) no se redistribuyen por licencia, así que los números
exactos de la tabla solo salen con esas mismas series; el método y los veredictos sí se reproducen
con cualquier serie equivalente. Las 005-007 murieron en el AED y no llegaron a tener señal.

> **Nota sobre las actas de 2026-09-15.** Los `RESUMEN.md` que hay en `reportes/` se generaron antes
> de que el motor incorporase el test de concentración (PF sin las 5 mejores operaciones), así que esa
> fila no aparece en ellos. No cambia ningún veredicto: las cuatro ya estaban descartadas por otros
> criterios, y un criterio más estricto no rescata a ninguna. Al revalidar con tus datos sí lo verás.

## Sobre el criterio que rechaza la 001

`trades OOS ≥ 30` **no lo dictó ninguna escuela**: lo puso por defecto la sesión que escribió
`docs/PROTOCOLO.md` (y el laboratorio en `validation.Criterios`), como regla estadística de mínimo
de muestra. Con 24 trades, un solo trade mueve el PF de 5.7 a 4.9 y el intervalo del win rate es
±20 puntos: el número no se puede distinguir de la deriva del índice en la década. Kaufman y
Raschke no dan ese número; es un umbral de honestidad, no de escuela.

Es un paso verde: **lo decides tú**. Si cambias el umbral a 50 o a 20, se cambia en
`docs/MIS_REGLAS.md` y se anota allí con fecha y motivo; con 20 la 001 pasaría entera. Lo que no se hace es acortar
el canal para fabricar trades.
