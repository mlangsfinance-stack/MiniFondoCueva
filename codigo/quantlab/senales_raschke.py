"""Señales de raschke para el NDX. Cada señal: una función ≤30 líneas, ≤4 params.
PLANES[nombre] = dict(fn, params, grid, meseta, config={...opcional para backtest.Config...})

Fuente: Raschke & Connors, *Street Smarts* (1995). Adaptadas a barras diarias; las
simplificaciones están documentadas en estrategias/003_raschke_holy_grail/hipotesis.md y
estrategias/004_raschke_ochenta_veinte/hipotesis.md.

NOTA: la copia **canónica** de estas señales vive en `codigo/estrategias/<ID>_<nombre>.py`, que es
la que usa `codigo/validar.py` y la que escriben los agentes. Este módulo lo mantienen los scripts
del laboratorio (`codigo/scripts/04_validar_ndx.py`, `05_charts_ndx.py`). Las dos copias tienen que
dar la misma señal: lo vigila `tests/test_estrategias_coinciden.py`.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import *  # noqa: F401,F403


def holy_grail(df: pd.DataFrame, adx_min: float = 30, ema_n: int = 20, hold: int = 5, adx_n: int = 14) -> pd.Series:
    """H001 — Holy Grail SOLO LARGOS: ADX fuerte y +DI > -DI, el low toca la EMA y el cierre
    queda encima → continuación. Se mantiene ``hold`` barras; el stop ATR del motor cubre el fallo."""
    a, pdi, mdi = adx(df, adx_n)
    e = ema(df["close"], ema_n)
    toque = (a > adx_min) & (pdi > mdi) & (df["low"] <= e) & (df["close"] > e)
    return toque.astype(int).rolling(hold, min_periods=1).max().fillna(0).astype(int)


def ochenta_veinte(df: pd.DataFrame, pct: float = 0.2, hold: int = 1, atr_mult_rango: float = 1.0,
                   atr_n: int = 10) -> pd.Series:
    """H004 — 80-20 (Taylor/Crabel vía Street Smarts), ambas direcciones: día que abre en el
    ``pct`` superior de su rango y cierra en el ``pct`` inferior → largo al día siguiente;
    el espejo → corto. Solo si el rango del día ≥ ``atr_mult_rango`` × ATR(atr_n) previo."""
    rango = df["high"] - df["low"]
    r = rango.replace(0, np.nan)
    pos_open = (df["open"] - df["low"]) / r
    pos_close = (df["close"] - df["low"]) / r
    grande = rango >= atr_mult_rango * atr(df, atr_n).shift(1)
    ev_largo = (pos_open >= 1 - pct) & (pos_close <= pct) & grande
    ev_corto = (pos_open <= pct) & (pos_close >= 1 - pct) & grande
    largo = ev_largo.astype(int).rolling(hold, min_periods=1).max()
    corto = ev_corto.astype(int).rolling(hold, min_periods=1).max()
    return (largo - corto).fillna(0).astype(int)


PLANES: dict = {
    "holy_grail": dict(
        fn=holy_grail,
        params=dict(adx_min=30, ema_n=20, hold=5),
        grid=[dict(adx_min=a, ema_n=e, hold=5) for a in (25, 30, 35) for e in (15, 20, 25)],  # 9
        meseta=(("adx_min", [20, 25, 30, 35, 40]), ("ema_n", [10, 15, 20, 25, 30])),
        config=dict(stop_atr=2.0, max_barras=5),
    ),
    "ochenta_veinte": dict(
        fn=ochenta_veinte,
        params=dict(pct=0.2, hold=1, atr_mult_rango=1.0),
        grid=[dict(pct=p, hold=1, atr_mult_rango=m) for p in (0.15, 0.2, 0.25) for m in (0.8, 1.0, 1.2)],  # 9
        meseta=(("pct", [0.1, 0.15, 0.2, 0.25, 0.3]), ("atr_mult_rango", [0.6, 0.8, 1.0, 1.2, 1.4])),
        config=dict(stop_atr=1.5, max_barras=1),
    ),
}
