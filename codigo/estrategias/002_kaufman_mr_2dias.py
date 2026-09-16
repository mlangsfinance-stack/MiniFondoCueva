"""002 · kaufman_mr_2dias — reversión de 2 días a favor de la tendencia de fondo (ambos lados).

Kaufman, *Trading Systems and Methods* (5ª ed.) cap. 15: tras varios cierres consecutivos en la
misma dirección aparece un sesgo de reversión a corto plazo. Aquí solo se opera esa reversión
cuando va **a favor** de la tendencia de fondo (SMA 200), que es lo que le da premisa.

La señal es una función de ≤30 líneas. El motor de ejecución, las métricas y las 5 fases de
validación viven en `codigo/quantlab/`; aquí solo se define QUÉ se opera, no CÓMO se ejecuta.

Look-ahead: todas las comparaciones usan cierres ya formados (`shift`), y el motor ejecuta cada
señal en la APERTURA de la barra siguiente. Ninguna señal usa datos de su propia barra.

VEREDICTO 2026-09-15: DESCARTADA. PF OOS 1.35 cash / 1.23 CFD; falla F1 en CFD, la meseta es un
pico (vecino 0.86) y costes ×2 la dejan en 1.09. Acta: `reportes/002_kaufman_mr_2dias/RESUMEN.md`.
"""
from __future__ import annotations

import pandas as pd

from quantlab.indicators import sma


def senal(df: pd.DataFrame, sma_n: int = 200, hold: int = 2) -> pd.Series:
    """1 = largo, -1 = corto, 0 = fuera. Largo tras dos cierres consecutivos a la baja con
    close > SMA(sma_n); corto tras dos al alza con close < SMA. Se mantiene `hold` barras
    (un evento nuevo renueva la señal). El stop catastrófico (2×ATR) lo pone el motor."""
    c = df["close"]
    media = sma(c, sma_n)
    baja2 = (c < c.shift(1)) & (c.shift(1) < c.shift(2))
    sube2 = (c > c.shift(1)) & (c.shift(1) > c.shift(2))
    largo = (baja2 & (c > media)).astype(int).rolling(hold, min_periods=1).max()
    corto = (sube2 & (c < media)).astype(int).rolling(hold, min_periods=1).max()
    return (largo - corto).fillna(0).astype(int)


# hold=2 no puede ir en el centro de 5 enteros ≥1: queda en índice 1 y el 3x3 se calcula sobre
# hold ∈ {1,2,3}. No se fija max_barras en config: capar en el motor haría idénticas las celdas
# hold ≥ 2 de la meseta (meseta falsa). El tiempo en mercado lo lleva la señal.
PLAN = dict(
    fn=senal,
    params=dict(sma_n=200, hold=2),
    grid=[dict(sma_n=a, hold=b) for a in (100, 200, 300) for b in (1, 2, 3)],  # 9 combinaciones
    meseta=(("sma_n", [100, 150, 200, 250, 300]), ("hold", [1, 2, 3, 4, 5])),
    config=dict(stop_atr=2.0),
)
