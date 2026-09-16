"""Señales de Kaufman para el NDX. Cada señal: una función ≤30 líneas, ≤4 params.
PLANES[nombre] = dict(fn, params, grid, meseta, config={...opcional para backtest.Config...})

Fuentes: Kaufman, *Trading Systems and Methods* (5ª ed.) cap. 5 (N-day breakout), cap. 15
(patrones de días consecutivos), cap. 17 (Efficiency Ratio); *Smarter Trading* (ruido de mercado).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import *  # noqa: F401,F403


def breakout_er(df: pd.DataFrame, n_entrada: int = 40, n_salida: int = 20, er_n: int = 10,
                er_min: float = 0.3) -> pd.Series:
    """Kaufman: ruptura del máximo de n_entrada barras SOLO si el tramo previo es poco ruidoso
    (ER ≥ er_min). Salida al perder el mínimo de n_salida barras. Solo largos: la deriva del
    índice y la naturaleza de las caídas (pánico, no tendencia) desaconsejan el lado corto."""
    er = efficiency_ratio(df["close"], er_n)
    entra = (df["close"] > maximo_previo(df["high"], n_entrada)) & (er >= er_min)
    sale = df["close"] < minimo_previo(df["low"], n_salida)
    pos = pd.Series(np.nan, index=df.index)
    pos[sale] = 0
    pos[entra] = 1
    return pos.ffill().fillna(0).astype(int)


def mr_2dias(df: pd.DataFrame, sma_n: int = 200, hold: int = 2) -> pd.Series:
    """Kaufman: reversión de corto plazo a favor de la tendencia de fondo. Largo tras dos
    cierres consecutivos a la baja con close > SMA(sma_n); corto tras dos al alza con
    close < SMA. Se mantiene ``hold`` barras (la señal persiste; un evento nuevo la renueva).
    El stop ATR lo pone el motor vía config."""
    c = df["close"]
    media = sma(c, sma_n)
    baja2 = (c < c.shift(1)) & (c.shift(1) < c.shift(2))
    sube2 = (c > c.shift(1)) & (c.shift(1) > c.shift(2))
    largo = (baja2 & (c > media)).astype(int).rolling(hold, min_periods=1).max()
    corto = (sube2 & (c < media)).astype(int).rolling(hold, min_periods=1).max()
    return (largo - corto).fillna(0).astype(int)


PLANES: dict = {
    "breakout_er": dict(
        fn=breakout_er,
        params=dict(n_entrada=40, n_salida=20, er_n=10, er_min=0.3),
        # grid pequeño (Kaufman): pasos gruesos, rangos amplios. 11 combinaciones.
        grid=[dict(n_entrada=a, n_salida=20, er_n=10, er_min=b) for a in (20, 40, 60) for b in (0.2, 0.3, 0.4)]
             + [dict(n_entrada=40, n_salida=10, er_n=10, er_min=0.3), dict(n_entrada=40, n_salida=40, er_n=10, er_min=0.3)],
        meseta=(("n_entrada", [20, 30, 40, 50, 60]), ("er_min", [0.1, 0.2, 0.3, 0.4, 0.5])),
        # Stop catastrófico ancho: en un breakout la salida principal es el canal (Kaufman, TSM
        # cap. 5); 2×ATR(14) cae dentro del ruido normal de un movimiento de 40 días.
        config=dict(stop_atr=3.0),
    ),
    "mr_2dias": dict(
        fn=mr_2dias,
        params=dict(sma_n=200, hold=2),
        grid=[dict(sma_n=a, hold=b) for a in (100, 200, 300) for b in (1, 2, 3)],  # 9 combinaciones
        # hold=2 no puede ir en el centro de 5 enteros ≥1; queda en índice 1 y el 3x3 se calcula
        # sobre hold ∈ {1,2,3}. No se fija max_barras en config: capar en el motor haría
        # idénticas las celdas hold ≥ 2 de la meseta (meseta falsa). El tiempo lo lleva la señal.
        meseta=(("sma_n", [100, 150, 200, 250, 300]), ("hold", [1, 2, 3, 4, 5])),
        config=dict(stop_atr=2.0),
    ),
}
