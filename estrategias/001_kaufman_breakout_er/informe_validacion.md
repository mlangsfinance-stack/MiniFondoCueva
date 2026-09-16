# 001 · kaufman_breakout_er — Informe de validación

Auditado contra `reglas.md` y `docs/PROTOCOLO.md`. Números recalculados con
`codigo/validar.py 001` sobre las mismas series (cash IS/OOS + CFD OOS); coinciden con
`informe_motor.md` (misma semilla, mismo motor). Hallazgos por gravedad.

## Tabla de criterios

| paso | criterio | motor | validador | umbral | pasa |
|---|---|---|---|---|---|
| 04 | PF OOS cash / CFD | 5.70 / 4.86 | 5.70 / 4.86 | ≥ 1.3 | sí |
| 04 | **trades OOS cash / CFD** | 24 / 23 | 24 / 23 | ≥ 30 | **no** |
| 04 | MaxDD OOS | 4.8 % / 3.8 % | igual | < 20 % | sí |
| 04 | PF OOS sin mejor | 4.89 / 4.18 | igual | > 1.0 | sí |
| 05 | meseta 3×3 · mín vecino · caída | 9 · 1.91 · 13.8 % | igual | 9 · ≥1.2 · ≤30 % | sí |
| 05 | WF eficiencia · ventanas + | 0.77 · 80 % | igual | ≥ 0.5 · ≥ 60 % | sí |
| 06 | MC p5 · p95 DD · ruina | 13.3 % · 3.8 % · 0 % | igual | >0 · <25 % · <5 % | sí |
| 06 | costes ×2 · sin 2 mejores años · peor tercio | 5.62 · 2.42 · 1.90 | igual | ≥1.1 · >1.0 · ≥1.1 | sí |

## Hallazgos

1. **Muestra OOS insuficiente (bloqueante).** 24 trades en diez años son 2.4 al año. Un PF de 5.7
   con 24 trades no es evidencia de edge: es la década más alcista del NDX con salidas de canal
   que dejaron correr 2016-2021. Un solo criterio fallido = RECHAZADA. No hay "casi".
2. **El AED ya avisó.** Permutación p = 0.28: el exceso a 5 días sobre la base es deriva del índice.
   La regla completa tiene buena forma (payoff 2.9, meseta plana, sobrevive a costes ×2), pero la
   forma no sustituye a la muestra.
3. Look-ahead: revisado `maximo_previo`/`minimo_previo` (shift(1)) y ejecución a la apertura
   siguiente en `quantlab.backtest`. Sin hallazgo.
4. OOS tocado una vez: la bitácora registra una sola validación. Sin hallazgo.
5. Costes: 2 pb por lado según `reglas.md`, aplicados en todas las métricas. Sin hallazgo.

## Qué haría falta
No acortar `n_entrada` para fabricar trades (prohibido en `reglas.md`). La vía legítima es
**multi-mercado**: correr la misma regla, sin tocarla, sobre SP500, DJI, RUT y DAX para sumar
trades OOS y ver si la forma se mantiene. Eso es una hipótesis nueva (001.1), con su AED.

Pasa todo menos la muestra. No pasa el criterio de 30 trades OOS en ninguna de las dos series.
Haría falta una validación multi-mercado antes de volver a hablar de esta regla.

VEREDICTO: RECHAZADA
