"""Motor de backtest único. No se escribe un motor por estrategia.

Modelo de ejecución (conservador a propósito):
- La señal se calcula al cierre de la barra i-1 y se ejecuta en la APERTURA de i.
- Stop inicial a k*ATR, evaluado intrabarra con high/low; si el mercado abre
  más allá del stop se rellena en la apertura (gap en contra, nunca a favor).
- Costes por lado como fracción del nocional (comisión + slippage + spread/2).
- Tamaño: riesgo fijo por trade sobre el equity actual (fixed fractional).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .indicators import atr


@dataclass
class Config:
    capital: float = 100_000.0
    coste_pct: float = 0.0005        # por lado, sobre el nocional
    riesgo_pct: float = 0.01         # fracción del equity arriesgada hasta el stop
    stop_atr: float | None = 2.0     # None = sin stop inicial
    atr_n: int = 14
    max_barras: int | None = None    # salida por tiempo
    fraccion_sin_stop: float = 0.25  # nocional/equity cuando no hay stop
    barras_anio: int = 252


@dataclass
class Resultado:
    trades: pd.DataFrame
    equity: pd.Series
    senal: pd.Series
    config: Config = field(default_factory=Config)


COLS_TRADE = ["entrada", "salida", "lado", "precio_entrada", "precio_salida", "unidades",
              "pnl", "pnl_pct", "R", "barras", "motivo"]


def backtest(df: pd.DataFrame, senal: pd.Series, cfg: Config | None = None) -> Resultado:
    cfg = cfg or Config()
    senal = senal.reindex(df.index).fillna(0).astype(int)
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    a = atr(df, cfg.atr_n).to_numpy(float)
    s = senal.to_numpy()
    idx = df.index
    n = len(df)

    equity = cfg.capital
    eq = np.empty(n)
    trades: list[dict] = []
    pos = 0
    unidades = precio_ent = riesgo_ini = 0.0
    stop: float | None = None
    i_ent = 0
    eq_ent = equity

    def abrir(i: int, lado: int, precio: float) -> None:
        nonlocal pos, unidades, precio_ent, stop, i_ent, riesgo_ini, eq_ent
        if cfg.stop_atr is not None:
            if np.isnan(a[i - 1]) or a[i - 1] <= 0:
                return
            dist = cfg.stop_atr * a[i - 1]
            unidades = equity * cfg.riesgo_pct / dist
            stop = precio - lado * dist
            riesgo_ini = unidades * dist
        else:
            unidades = equity * cfg.fraccion_sin_stop / precio
            stop = None
            riesgo_ini = equity * cfg.riesgo_pct
        pos, precio_ent, i_ent, eq_ent = lado, precio, i, equity

    def cerrar(i: int, precio: float, motivo: str) -> None:
        nonlocal pos, equity
        bruto = pos * unidades * (precio - precio_ent)
        costes = cfg.coste_pct * unidades * (precio + precio_ent)
        pnl = bruto - costes
        equity += pnl
        trades.append({"entrada": idx[i_ent], "salida": idx[i], "lado": pos,
                       "precio_entrada": precio_ent, "precio_salida": precio, "unidades": unidades,
                       "pnl": pnl, "pnl_pct": pnl / eq_ent, "R": pnl / riesgo_ini if riesgo_ini else np.nan,
                       "barras": i - i_ent, "motivo": motivo})
        pos = 0

    eq[0] = equity
    for i in range(1, n):
        deseada = s[i - 1]
        # 1) cambios de posición decididos al cierre anterior -> apertura de hoy
        if pos != 0 and deseada != pos:
            cerrar(i, o[i], "senal")
        if pos == 0 and deseada != 0:
            abrir(i, int(deseada), o[i])
        # 2) stop intrabarra
        if pos != 0 and stop is not None:
            if pos == 1 and l[i] <= stop:
                cerrar(i, min(stop, o[i]), "stop")
            elif pos == -1 and h[i] >= stop:
                cerrar(i, max(stop, o[i]), "stop")
        # 3) salida por tiempo
        if pos != 0 and cfg.max_barras and i - i_ent >= cfg.max_barras:
            cerrar(i, c[i], "tiempo")
        eq[i] = equity + (pos * unidades * (c[i] - precio_ent) if pos else 0.0)
    if pos != 0:
        cerrar(n - 1, c[n - 1], "fin")
        eq[n - 1] = equity

    trades_df = pd.DataFrame(trades, columns=COLS_TRADE)
    return Resultado(trades=trades_df, equity=pd.Series(eq, index=idx, name="equity"), senal=senal, config=cfg)
