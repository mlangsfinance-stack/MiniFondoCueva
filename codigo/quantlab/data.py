"""Carga y partición de datos OHLC.

Convención: DataFrame indexado por fecha (ascendente) con columnas en minúscula
``open, high, low, close`` y opcionalmente ``volume``.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

COLUMNAS = ["open", "high", "low", "close"]


def cargar(path: str | Path) -> pd.DataFrame:
    """Lee CSV o parquet y normaliza nombres de columna e índice temporal."""
    p = Path(path)
    if p.suffix == ".parquet":
        df = pd.read_parquet(p)
    else:
        df = pd.read_csv(p)
    df.columns = [str(c).strip().lower() for c in df.columns]
    if not isinstance(df.index, pd.DatetimeIndex):
        col_fecha = next((c for c in df.columns if c in ("date", "datetime", "time", "fecha")), df.columns[0])
        df[col_fecha] = pd.to_datetime(df[col_fecha])
        df = df.set_index(col_fecha)
    df = df.rename(columns={"adj close": "close", "adj_close": "close", "vol": "volume"})
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas {faltan}; hay {list(df.columns)}")
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    return df[COLUMNAS + (["volume"] if "volume" in df.columns else [])].astype(float)


def sintetico(n: int = 3000, seed: int = 42, vol: float = 0.012, deriva: float = 0.0002,
              autocorr: float = 0.05, inicio: str = "2010-01-01") -> pd.DataFrame:
    """Serie OHLC sintética (AR(1) sobre log-retornos) para probar el pipeline.

    Sirve para comprobar que el código funciona, NO para sacar conclusiones:
    con ``autocorr=0`` ninguna regla debería tener edge (test de placebo).
    """
    rng = np.random.default_rng(seed)
    eps = rng.normal(deriva, vol, n)
    ret = np.empty(n)
    ret[0] = eps[0]
    for i in range(1, n):
        ret[i] = autocorr * ret[i - 1] + eps[i]
    close = 100.0 * np.exp(np.cumsum(ret))
    prev = np.r_[100.0, close[:-1]]
    open_ = prev * np.exp(rng.normal(0, vol * 0.25, n))
    high = np.maximum(open_, close) * np.exp(np.abs(rng.normal(0, vol * 0.5, n)))
    low = np.minimum(open_, close) * np.exp(-np.abs(rng.normal(0, vol * 0.5, n)))
    idx = pd.bdate_range(inicio, periods=n)
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close,
                         "volume": rng.integers(1e5, 1e6, n).astype(float)}, index=idx)


def split_is_oos(df: pd.DataFrame, corte: float | str = 0.7) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Partición temporal: primero IS, después OOS. El OOS se toca UNA vez.

    ``corte`` es una fracción (0.7 = 70 % IS) o una fecha ("2016-01-01": OOS desde ahí).
    """
    if isinstance(corte, str):
        f = pd.Timestamp(corte)
        return df[df.index < f], df[df.index >= f]
    k = int(len(df) * corte)
    return df.iloc[:k], df.iloc[k:]


def ventanas_walk_forward(df: pd.DataFrame, n_ventanas: int = 5, frac_is: float = 0.7
                          ) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """Ventanas rodantes: cada OOS va precedido de su IS; los OOS son contiguos.

    Con ``frac_is=0.7`` cada IS es ~2.3× el OOS. Devuelve [(is_1, oos_1), ...].
    """
    r = frac_is / (1 - frac_is)
    oos_len = int(len(df) / (n_ventanas + r))
    is_len = int(r * oos_len)
    ventanas = []
    for k in range(n_ventanas):
        a = k * oos_len
        b = a + is_len
        c = min(b + oos_len, len(df))
        ventanas.append((df.iloc[a:b], df.iloc[b:c]))
    return ventanas
