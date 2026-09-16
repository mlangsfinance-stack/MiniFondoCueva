# H001 — Holy Grail: retroceso a la EMA20 en tendencia fuerte (solo largos)

- **Fecha:** 2026-09-15
- **Fuente:** literatura — Raschke & Connors, *Street Smarts* (1995), cap. "The Holy Grail"
  (ADX(14) > 30 y subiendo, retroceso a la EMA20, entrada al superar el alto de la barra del
  retroceso, stop bajo el mínimo del retroceso, objetivo el máximo previo).
- **Familia de edge:** continuación
- **Estado:** descartada (validación, Fase 1; tendencia y prototipo ya débiles) — ver `estrategias/003_raschke_holy_grail/`
- **Tests acumulados sobre esta hipótesis:** 3 (1 placebo sintético que no cuenta como evidencia,
  1 tendencia IS NDX, 1 validación 5 fases NDX)

## 1. Observación
En índices y futuros líquidos, cuando la tendencia es fuerte (ADX alto) y el precio retrocede
hasta la media de 20, con frecuencia reanuda la tendencia en las siguientes sesiones.
Raschke lo documenta en diario e intradía (60 min). Aquí se prueba **solo el lado largo** sobre el
NDX diario: el índice tiene deriva positiva y el lado corto del Holy Grail en renta variable
es una hipótesis distinta (se probaría aparte).

## 2. Mecanismo
Conductual + estructural: en tendencia fuerte hay participantes que se quedaron fuera y
compran el primer retroceso ("buy the dip"), más gestores tendenciales que añaden en pullbacks.
La EMA20 es un punto focal ampliamente vigilado, lo que concentra esas órdenes.

## 3. Universo y timeframe
Índices (SP500, NDX, DAX) y futuros líquidos en diario. NO se espera en pares de divisas
en rango ni en acciones individuales de baja liquidez. Este test: NDX cash (Norgate) diario.

## 4. Evento
```
adx, +di, -di = ADX(14)   (suavizado de Wilder, quantlab.indicators.adx)
ema20 = EMA(close, 20)
evento_largo = (adx > 30) & (+di > -di) & (low <= ema20) & (close > ema20)
```
Simplificación respecto a Street Smarts: no se exige "ADX subiendo" ni entrada por ruptura del
alto de la barra del retroceso (en diario el motor entra en la apertura siguiente). El objetivo
"máximo previo" se sustituye por salida por tiempo (`hold` = 5 barras) + stop 2·ATR(14).

## 5. Predicción falsable
Tras el evento largo, el retorno a 3 y 5 barras supera el incondicional; la probabilidad de
superar el alto de la barra del evento en 3 barras es mayor que la base.
Horizonte principal: h = 5. Magnitud esperada: ≥ +0.3 % de exceso (NDX diario).

## 6. Métrica que decide
Exceso de retorno a h=5 (t-stat) y `p_supera_alto` a h=3; p-valor de permutación a h=5.

## 7. Criterio de muerte (escrito ANTES de correr nada)
Datos: Norgate NDX, IS = fecha < 2016-01-01. Se descarta en tendencia si n < 100, o exceso ≤ 0
a h=5, o exceso > 0 en menos de 2 horizontes, o |t| < 2, o p-valor de permutación > 0.05.
Variantes admitidas si hiciera falta: ADX 25/30/35 (son 3 tests, no 1). En este test inicial
solo se corre la variante natural (ADX 30).
Prototipo (IS, params naturales adx_min=30, ema_n=20, hold=5, stop 2 ATR): muere si PF ≤ 1.2,
n < 100, expectancia ≤ 0.1 R o t ≤ 2.

## 8. Coste esperado
Índice CFD/futuro: ~0.04 % ida y vuelta (2 pb por lado). Exceso esperado 0.3 %. Ratio 7.5×. OK.

---

## Resultado del test de tendencia
Fecha 2026-09-15 · datos `data/ndx_norgate_d1.parquet`, IS = 1985-01-31 → 2015-12-31 (7.795 barras).
Evento largo: **n = 71** (0.9 % de las barras).

| h | n | media | mediana | pct_pos | media_base | pct_pos_base | exceso | t_stat |
|---|---|---|---|---|---|---|---|---|
| 1 | 71 | 0.0002 | 0.0022 | 0.563 | 0.0006 | 0.542 | -0.0005 | 0.07 |
| 2 | 71 | 0.0029 | 0.0056 | 0.592 | 0.0012 | 0.543 | +0.0017 | 1.40 |
| 3 | 71 | 0.0043 | 0.0051 | 0.592 | 0.0018 | 0.558 | +0.0025 | 1.30 |
| 5 | 71 | 0.0064 | 0.0048 | 0.606 | 0.0030 | 0.566 | +0.0034 | 1.92 |
| 10 | 71 | 0.0105 | 0.0096 | 0.578 | 0.0058 | 0.577 | +0.0047 | 2.13 |

`prob_rango` h=3: p_supera_alto 0.789 vs base 0.713 · p_rompe_bajo 0.437 vs base 0.619.
`test_permutacion` h=5, n_sim=1000: media 0.0064 vs azar 0.0032 → **p = 0.209**.

Puerta: n ≥ 100 **NO** (71) · exceso > 0 en ≥ 2 horizontes SÍ (h=2..10) · |t| ≥ 2 en h=5 **NO** (1.92)
· p ≤ 0.05 **NO** (0.21). La dirección del efecto es la predicha (+0.34 % a h=5, ≥ 0.3 % esperado)
y el rango se comporta como dice Raschke (más roturas del alto, menos del bajo), pero la muestra
es pequeña: ADX(14) > 30 en el NDX diario ocurre poco y el toque de la EMA20 dentro de ese
régimen, menos. No pasa la puerta de tendencia.

## Decisión
**Tendencia débil, no pasa la puerta.** Por ser test inicial de pipeline se lleva igualmente a
prototipo y validación (marcado como "tendencia débil"); el veredicto final lo tiene en cuenta.
Lo aprendido: el filtro ADX > 30 deja al NDX con ~2 eventos/año; para tener n suficiente habría
que probar ADX 25 (variante H001.1, test nuevo) o agregar varios índices como decía la ficha
original (SP500 + NDX + DAX).

## Prototipo y validación (2026-09-15)
Prototipo IS (adx_min 30, ema_n 20, hold 5, stop 2 ATR, 2 pb/lado): n=64, PF 1.40, exp 0.103 R,
t=1.09, 60 % años positivos → no pasa la puerta (n < 100, t < 2).
Validación `codigo/scripts/04_validar_ndx.py holy_grail --rapido` → **DESCARTADA**. PF OOS 1.05 (Norgate,
13 trades) y 0.56 (Darwinex, 23 trades); fallan F1, F2 (eficiencia WF 0.37), F3 (vecino 1.18) y F5
(peor tercio 0.79). Acta completa en `reportes/003_raschke_holy_grail/RESUMEN.md`.
