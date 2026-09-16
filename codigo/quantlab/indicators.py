"""Indicadores. Solo los que hacen falta para las señales de ejemplo.

Kaufman: el Efficiency Ratio mide señal/ruido; KAMA adapta la velocidad de la
media a ese ratio. Es la forma más honesta de "seguir tendencia" sin elegir
a mano un periodo que solo funcionó en el pasado.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def true_range(df: pd.DataFrame) -> pd.Series:
    prev = df["close"].shift(1)
    return pd.concat([df["high"] - df["low"], (df["high"] - prev).abs(), (df["low"] - prev).abs()], axis=1).max(axis=1)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    return true_range(df).ewm(alpha=1 / n, adjust=False).mean()


def efficiency_ratio(close: pd.Series, n: int = 10) -> pd.Series:
    """ER de Kaufman: |desplazamiento neto| / suma de |desplazamientos|. 1 = línea recta, 0 = ruido puro."""
    direccion = (close - close.shift(n)).abs()
    ruido = close.diff().abs().rolling(n).sum()
    return (direccion / ruido.replace(0, np.nan)).fillna(0.0)


def kama(close: pd.Series, n: int = 10, rapida: int = 2, lenta: int = 30) -> pd.Series:
    """Kaufman Adaptive Moving Average."""
    er = efficiency_ratio(close, n)
    sc = (er * (2 / (rapida + 1) - 2 / (lenta + 1)) + 2 / (lenta + 1)) ** 2
    vals, scv = close.to_numpy(float), sc.to_numpy(float)
    out = np.full(len(vals), np.nan)
    if len(vals) > n:
        out[n - 1] = vals[n - 1]
        for i in range(n, len(vals)):
            out[i] = out[i - 1] + scv[i] * (vals[i] - out[i - 1])
    return pd.Series(out, index=close.index)


def adx(df: pd.DataFrame, n: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Devuelve (ADX, +DI, -DI) con suavizado de Wilder."""
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)
    atr_ = true_range(df).ewm(alpha=1 / n, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1 / n, adjust=False).mean() / atr_
    minus_di = 100 * minus_dm.ewm(alpha=1 / n, adjust=False).mean() / atr_
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1 / n, adjust=False).mean(), plus_di, minus_di


def roc(close: pd.Series, n: int) -> pd.Series:
    return close / close.shift(n) - 1


def zscore(s: pd.Series, n: int) -> pd.Series:
    return (s - s.rolling(n).mean()) / s.rolling(n).std()


def maximo_previo(s: pd.Series, n: int) -> pd.Series:
    """Máximo de las n barras ANTERIORES (excluye la actual: sin look-ahead)."""
    return s.shift(1).rolling(n).max()


def minimo_previo(s: pd.Series, n: int) -> pd.Series:
    return s.shift(1).rolling(n).min()
