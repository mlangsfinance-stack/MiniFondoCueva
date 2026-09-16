"""Métricas. Definiciones en docs/05_METRICAS.md. Todas salen de la lista de
trades y de la curva de equity; nada se calcula de otra forma en otro sitio."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .backtest import Resultado


def max_drawdown(equity: pd.Series) -> float:
    return float((equity / equity.cummax() - 1).min())


def profit_factor(pnl: pd.Series) -> float:
    g = pnl[pnl > 0].sum()
    p = -pnl[pnl < 0].sum()
    return float(g / p) if p > 0 else (np.inf if g > 0 else 0.0)


def metricas(res: Resultado) -> dict:
    t, eq, cfg = res.trades, res.equity, res.config
    n = len(t)
    anios = max(len(eq) / cfg.barras_anio, 1e-9)
    ret = eq.pct_change().dropna()
    out = {
        "n_trades": n,
        "retorno_total": float(eq.iloc[-1] / eq.iloc[0] - 1),
        "cagr": float((eq.iloc[-1] / eq.iloc[0]) ** (1 / anios) - 1) if eq.iloc[-1] > 0 else -1.0,
        "max_dd": max_drawdown(eq),
        "sharpe": float(ret.mean() / ret.std() * np.sqrt(cfg.barras_anio)) if ret.std() > 0 else 0.0,
        "trades_anio": n / anios,
    }
    if n == 0:
        out.update({"profit_factor": 0.0, "pf_sin_mejor": 0.0, "win_rate": 0.0, "expectancia_R": 0.0,
                    "payoff": np.nan, "t_stat": 0.0, "media_barras": 0.0, "pct_stop": 0.0, "mar": np.nan})
        return out
    pnl = t["pnl"]
    out.update({
        "profit_factor": profit_factor(pnl),
        "pf_sin_mejor": profit_factor(pnl.drop(pnl.idxmax())) if n > 1 else 0.0,
        "win_rate": float((pnl > 0).mean()),
        "expectancia_R": float(t["R"].mean()),
        "payoff": float(pnl[pnl > 0].mean() / -pnl[pnl < 0].mean()) if (pnl < 0).any() and (pnl > 0).any() else np.nan,
        "t_stat": float(pnl.mean() / pnl.std() * np.sqrt(n)) if n > 1 and pnl.std() > 0 else 0.0,
        "media_barras": float(t["barras"].mean()),
        "pct_stop": float((t["motivo"] == "stop").mean()),
        "mar": out["cagr"] / abs(out["max_dd"]) if out["max_dd"] < 0 else np.nan,
    })
    return out


def pnl_por_anio(trades: pd.DataFrame) -> pd.Series:
    if trades.empty:
        return pd.Series(dtype=float)
    return trades.groupby(trades["salida"].dt.year)["pnl"].sum()
