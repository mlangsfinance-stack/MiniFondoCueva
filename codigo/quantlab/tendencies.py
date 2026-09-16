"""Estudios de tendencia (Raschke) y contraste contra el azar (Simons).

Antes de escribir una regla con entradas, stops y salidas, se responde a una
pregunta más simple: *¿después de X, el mercado hace Y más veces de lo normal?*
Si la respuesta es no, no hay nada que optimizar.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def retorno_forward(close: pd.Series, h: int) -> pd.Series:
    return close.shift(-h) / close - 1


def estudio_evento(df: pd.DataFrame, evento: pd.Series, horizontes=(1, 2, 3, 5, 10)) -> pd.DataFrame:
    """Retorno medio tras el evento vs. retorno incondicional, por horizonte.

    ``evento`` es una Series booleana alineada con ``df`` (True = la condición
    se cumple al cierre de esa barra). Devuelve una fila por horizonte con
    n, media, mediana, % positivo, lo mismo para la base y el t-stat.
    """
    ev = evento.reindex(df.index).fillna(False).astype(bool)
    filas = []
    for h in horizontes:
        fwd = retorno_forward(df["close"], h)
        cond = fwd[ev].dropna()
        base = fwd.dropna()
        n = len(cond)
        resto = fwd[~ev].dropna()
        t = cond.mean() / cond.std() * np.sqrt(n) if n > 1 and cond.std() > 0 else np.nan
        # t de Welch de la DIFERENCIA evento vs no-evento: en activos con deriva es el que cuenta
        se = np.sqrt(cond.var() / n + resto.var() / len(resto)) if n > 1 and len(resto) > 1 else np.nan
        t_exceso = (cond.mean() - resto.mean()) / se if se and se > 0 else np.nan
        filas.append({
            "horizonte": h, "n": n,
            "media": cond.mean(), "mediana": cond.median(), "pct_pos": (cond > 0).mean(),
            "media_base": base.mean(), "pct_pos_base": (base > 0).mean(),
            "exceso": cond.mean() - base.mean(), "t_stat": t, "t_exceso": t_exceso,
        })
    return pd.DataFrame(filas).set_index("horizonte")


def prob_rango(df: pd.DataFrame, evento: pd.Series, h: int = 1) -> dict:
    """Probabilidad de que en las próximas h barras se supere el máximo previo
    o se rompa el mínimo previo, tras el evento y en la base (Raschke: rango
    y expansión importan tanto como la dirección)."""
    ev = evento.reindex(df.index).fillna(False).astype(bool)
    max_fwd = df["high"].shift(-1).rolling(h).max().shift(-(h - 1))
    min_fwd = df["low"].shift(-1).rolling(h).min().shift(-(h - 1))
    supera = (max_fwd > df["high"]).where(max_fwd.notna())
    rompe = (min_fwd < df["low"]).where(min_fwd.notna())
    return {
        "h": h, "n": int(ev.sum()),
        "p_supera_alto": float(supera[ev].mean()), "p_supera_alto_base": float(supera.mean()),
        "p_rompe_bajo": float(rompe[ev].mean()), "p_rompe_bajo_base": float(rompe.mean()),
    }


def test_permutacion(df: pd.DataFrame, evento: pd.Series, h: int = 5, n_sim: int = 2000, seed: int = 0) -> dict:
    """p-valor empírico: el retorno medio tras el evento, comparado con el de
    n eventos elegidos al azar. Es el contraste mínimo antes de creer nada."""
    rng = np.random.default_rng(seed)
    ev = evento.reindex(df.index).fillna(False).astype(bool)
    fwd = retorno_forward(df["close"], h).dropna()
    ev = ev.reindex(fwd.index).fillna(False)
    n = int(ev.sum())
    if n == 0:
        return {"h": h, "n": 0, "media": np.nan, "p_valor": np.nan}
    observado = fwd[ev].mean()
    pool = fwd.to_numpy()
    sims = np.array([pool[rng.choice(len(pool), n, replace=False)].mean() for _ in range(n_sim)])
    return {"h": h, "n": n, "media": float(observado), "media_azar": float(sims.mean()),
            "p_valor": float((sims >= observado).mean())}
