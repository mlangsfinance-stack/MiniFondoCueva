"""Señales de ejemplo. Regla de la casa: una función = una regla, pocas líneas,
pocos parámetros, sin estado oculto. Devuelven la posición deseada al CIERRE
de cada barra (1 largo, -1 corto, 0 fuera); el motor la ejecuta en la apertura
siguiente. Toda señal recibe ``df`` y parámetros con nombre.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import adx, ema, efficiency_ratio, kama, maximo_previo, minimo_previo


def kama_tendencia(df: pd.DataFrame, n: int = 10, rapida: int = 2, lenta: int = 30, er_min: float = 0.3) -> pd.Series:
    """Kaufman: largo si la KAMA sube, corto si baja; fuera si el ER dice que es ruido."""
    k = kama(df["close"], n, rapida, lenta)
    er = efficiency_ratio(df["close"], n)
    pendiente = np.sign(k.diff()).fillna(0)
    return pd.Series(np.where(er >= er_min, pendiente, 0), index=df.index).astype(int)


def holy_grail(df: pd.DataFrame, adx_n: int = 14, adx_min: float = 30, ema_n: int = 20, hold: int = 5) -> pd.Series:
    """Raschke: en tendencia fuerte (ADX alto) un retroceso a la EMA20 es continuación.
    Se mantiene ``hold`` barras; el stop ATR del motor cubre el fallo."""
    a, pdi, mdi = adx(df, adx_n)
    e = ema(df["close"], ema_n)
    fuerte = a > adx_min
    toque_largo = fuerte & (pdi > mdi) & (df["low"] <= e) & (df["close"] > e)
    toque_corto = fuerte & (mdi > pdi) & (df["high"] >= e) & (df["close"] < e)
    largo = toque_largo.astype(int).rolling(hold, min_periods=1).max()
    corto = toque_corto.astype(int).rolling(hold, min_periods=1).max()
    return (largo - corto).fillna(0).astype(int)


def ruptura_donchian(df: pd.DataFrame, n_entrada: int = 50, n_salida: int = 20) -> pd.Series:
    """Ruptura de canal (Turtle): entra al superar el máximo de n_entrada barras,
    sale al perder el mínimo de n_salida. Simétrico para cortos."""
    entra_l = df["close"] > maximo_previo(df["high"], n_entrada)
    sale_l = df["close"] < minimo_previo(df["low"], n_salida)
    entra_c = df["close"] < minimo_previo(df["low"], n_entrada)
    sale_c = df["close"] > maximo_previo(df["high"], n_salida)
    pos = pd.Series(np.nan, index=df.index)
    pos[sale_l | sale_c] = 0
    pos[entra_l] = 1
    pos[entra_c] = -1
    return pos.ffill().fillna(0).astype(int)


CATALOGO = {"kama_tendencia": kama_tendencia, "holy_grail": holy_grail, "ruptura_donchian": ruptura_donchian}
