# H004 — 80-20: reversión tras un día que abre en un extremo y cierra en el otro

- **Fecha:** 2026-09-15
- **Fuente:** literatura — Raschke & Connors, *Street Smarts* (1995), cap. "80-20's"
  (patrón de Taylor/Crabel: un día que abre en el 20 % superior de su rango y cierra en el 20 %
  inferior tiende a revertir al día siguiente; Street Smarts añade que el rango del Día 1 debe
  ser mayor que la media, que la entrada es tras un nuevo extremo en el Día 2 y que es un trade
  de un día).
- **Familia de edge:** reversión (corto plazo)
- **Estado:** descartada (prototipo IS, confirmado en validación Fase 1) — ver `estrategias/x_descartadas/E004_ochenta_veinte.md`
- **Tests acumulados sobre esta hipótesis:** 3 (tendencia IS NDX largo, tendencia IS NDX corto,
  validación 5 fases NDX)

## 1. Observación
Un día que abre en un extremo y cierra en el opuesto es un "día de tendencia" intradía agotado.
Raschke y Connors documentan en futuros de índices, bonos y divisas que al día siguiente el precio
tiende a volver hacia el extremo de apertura, sobre todo cuando el rango del Día 1 es grande.

## 2. Mecanismo
Conductual: sobre-reacción intradía. El movimiento de apertura a cierre en un solo día arrastra
stops y órdenes de pánico; al día siguiente, sin flujo nuevo, el precio retrocede parte del exceso.
Estructural menor: gestores que cierran posiciones al cierre y las reabren en apertura.

## 3. Universo y timeframe
Futuros de índices, bonos y divisas en diario (Street Smarts). Aquí: NDX cash (Norgate) diario.
NO se espera en horizontes > 2 días ni en activos con tendencia intradía persistente.
**Aviso de datos:** antes de ~2000 el `open` del NDX cash es el cierre previo (no hay apertura
real); el evento en ese tramo es un artefacto (open = cierre previo) y se anota como tal.

## 4. Evento
```
rango = high - low
pos_open  = (open  - low) / rango          # 0 = abre en el mínimo, 1 = abre en el máximo
pos_close = (close - low) / rango
grande = rango >= atr_mult_rango * ATR(10).shift(1)   # rango mayor que la media (sin look-ahead)
evento_largo = (pos_open >= 1 - pct) & (pos_close <= pct) & grande   # abre arriba, cierra abajo
evento_corto = (pos_open <= pct) & (pos_close >= 1 - pct) & grande   # abre abajo, cierra arriba
```
pct = 0.2. Barras con rango 0 no generan evento.
Simplificación respecto a Street Smarts: señal al cierre de Día 1, entrada en la apertura de
Día 2 (no se espera al nuevo extremo ni se coloca el stop en ese extremo); salida al cierre de
Día 2 (`hold` = 1) o por stop 1.5·ATR(14).

## 5. Predicción falsable
Tras el evento largo, el retorno a 1 barra es mayor que el incondicional; tras el evento corto,
menor. Horizonte principal: h = 1. Magnitud esperada: ≥ +0.2 % de exceso a favor de la reversión
(NDX diario, vol diaria ~1.5 %).

## 6. Métrica que decide
Exceso de retorno a h=1 (t-stat, signo según dirección) y p-valor de permutación a h=1.
Para el corto se evalúa con retorno cambiado de signo (o p-valor unilateral inferior).

## 7. Criterio de muerte (escrito ANTES de correr nada)
Datos: Norgate NDX, IS = fecha < 2016-01-01. Cada dirección se mide por separado. Una dirección
muere si n < 100, o exceso a favor de la reversión ≤ 0 a h=1, o exceso a favor en menos de 2
horizontes consecutivos (h=1,2), o |t| < 2, o p-valor de permutación > 0.05.
Si mueren ambas, la hipótesis muere en tendencia (se puede llevar igualmente al prototipo como
"tendencia débil" en este test inicial, pero el veredicto lo tendrá en cuenta).
Prototipo (IS, params naturales pct=0.2, hold=1, atr_mult_rango=1.0, stop 1.5 ATR): muere si
PF ≤ 1.2, n < 100, expectancia ≤ 0.1 R o t ≤ 2.

## 8. Coste esperado
Índice CFD: ~0.04 % ida y vuelta (2 pb por lado). Exceso esperado 0.2 %. Ratio 5×. Justo pero OK;
un trade de 1 día es muy sensible a costes.

---

## Resultado del test de tendencia
Fecha 2026-09-15 · datos `data/ndx_norgate_d1.parquet`, IS = 1985-01-31 → 2015-12-31 (7.795 barras).
pct = 0.2, rango ≥ 1.0 × ATR(10) previo.

**Evento largo (abre arriba, cierra abajo): n = 570** (307 desde 2000, con open real)

| h | n | media | mediana | pct_pos | media_base | pct_pos_base | exceso | t_stat |
|---|---|---|---|---|---|---|---|---|
| 1 | 570 | 0.0020 | 0.0013 | 0.549 | 0.0006 | 0.542 | +0.0014 | 2.21 |
| 2 | 570 | 0.0038 | 0.0045 | 0.597 | 0.0012 | 0.543 | +0.0026 | 2.93 |
| 3 | 570 | 0.0044 | 0.0060 | 0.583 | 0.0018 | 0.558 | +0.0026 | 3.21 |
| 5 | 570 | 0.0059 | 0.0063 | 0.577 | 0.0030 | 0.566 | +0.0029 | 3.29 |

`test_permutacion` h=1, n_sim=1000: media 0.0020 vs azar 0.0006 → **p = 0.018**.
Submuestra 2000–2015 (open real): n=307, exceso h=1 +0.27 %, t=2.19, p=0.002 (más fuerte).
Puerta: n ≥ 100 SÍ · exceso > 0 en h=1,2 SÍ · |t| ≥ 2 SÍ · p ≤ 0.05 SÍ → **PASA**. Exceso 0.14 %
(0.27 % con open real) vs coste 0.04 % ida y vuelta: ratio 3.5× (6.8×), en el límite de la puerta.

**Evento corto (abre abajo, cierra arriba): n = 630** (241 desde 2000)

| h | n | media | mediana | pct_pos | media_base | pct_pos_base | exceso | t_stat |
|---|---|---|---|---|---|---|---|---|
| 1 | 630 | 0.0018 | 0.0019 | 0.571 | 0.0006 | 0.542 | +0.0012 | 3.10 |
| 2 | 630 | 0.0021 | 0.0028 | 0.579 | 0.0012 | 0.543 | +0.0009 | 2.50 |
| 3 | 630 | 0.0035 | 0.0045 | 0.584 | 0.0018 | 0.558 | +0.0017 | 3.36 |
| 5 | 630 | 0.0053 | 0.0060 | 0.592 | 0.0030 | 0.566 | +0.0024 | 4.05 |

`test_permutacion` h=1: media +0.0018 vs azar +0.0006 → p = 0.031 **pero en la dirección contraria**
(el precio sigue subiendo: continuación, no reversión). p unilateral a favor del corto ≈ 0.97.
Submuestra 2000–2015: exceso h=1 −0.04 %, t=−0.15, p=0.61 (nada).
Puerta: exceso a favor de la reversión ≤ 0 → **MUERE**. Un día alcista de apertura a cierre en el
NDX no revierte al día siguiente; en el tramo con open artificial incluso continúa.

## Decisión
**Largo pasa a prototipo; corto muerto en tendencia.** La hipótesis tal como se definió (ambas
direcciones) se lleva a prototipo y validación con las dos direcciones — es lo que dice la regla
de partida y no se cambia tras ver el resultado. Si la validación muere por el lado corto, la
versión solo-largos es hipótesis nueva **H004.1** con test nuevo, no un ajuste de esta.
Lo aprendido: la reversión 80-20 en el NDX es asimétrica: funciona tras días de venta (miedo,
sobre-reacción bajista), no tras días de compra (momentum del índice).

## Prototipo y validación (2026-09-15)
Prototipo IS (pct 0.2, hold 1, rango ≥ 1.0 ATR(10), stop 1.5 ATR, 2 pb/lado; entrada apertura Día 2,
salida apertura Día 3): n=1153, PF 0.74, exp −0.044 R, t=−3.77 → muere. Por lado: corto PF 0.57
(t=−5.0), largo PF 0.95. Con open real (2000–2015): corto 1.00, largo 1.12.
Validación `scripts/04_validar_ndx.py ochenta_veinte --rapido` → **DESCARTADA**. PF OOS 1.15 (Norgate,
276 trades) y 1.16 (Darwinex, 361 trades); fallan F1, F2 (eficiencia 0.0), F3 (vecino 0.65) y F5
(sin 2 mejores años 0.77, peor tercio 0.55). Acta en `reportes/ndx_ochenta_veinte/RESUMEN.md`.
Siguiente: H004.1 (solo largos, open real, salida al cierre de Día 2) como hipótesis nueva.
