"""003 · raschke_holy_grail — retroceso a la EMA20 dentro de tendencia fuerte (solo largos).

Raschke & Connors, *Street Smarts* (1995), "Holy Grail": con ADX alto la tendencia está viva;
el primer retroceso a la media móvil es continuación, no giro. Adaptada a barras diarias.

La señal es una función de ≤30 líneas. El motor de ejecución, las métricas y las 5 fases de
validación viven en `codigo/quantlab/`; aquí solo se define QUÉ se opera, no CÓMO se ejecuta.

Look-ahead: el motor ejecuta la señal en la APERTURA de la barra siguiente, así que usar el
low/close de la barra del evento no adelanta información.

VEREDICTO 2026-09-15: DESCARTADA. PF OOS 1.05 cash / 0.56 CFD con 13 / 23 trades. ADX>30 en el
NDX diario son ~2 eventos al año y solo vive 1999-2012: sin muestra y sin PF. Acta:
`reportes/003_raschke_holy_grail/RESUMEN.md`.
"""
from __future__ import annotations

import pandas as pd

from quantlab.indicators import adx, ema


def senal(df: pd.DataFrame, adx_min: float = 30, ema_n: int = 20, hold: int = 5,
          adx_n: int = 14) -> pd.Series:
    """1 = largo, 0 = fuera. Entra si ADX(adx_n) > adx_min y +DI > -DI (tendencia alcista viva),
    el low toca la EMA(ema_n) y el cierre queda por encima. Se mantiene `hold` barras; la salida
    por fallo la da el stop ATR (2×) y el tope de 5 barras que pone el motor."""
    a, pdi, mdi = adx(df, adx_n)
    e = ema(df["close"], ema_n)
    toque = (a > adx_min) & (pdi > mdi) & (df["low"] <= e) & (df["close"] > e)
    return toque.astype(int).rolling(hold, min_periods=1).max().fillna(0).astype(int)


PLAN = dict(
    fn=senal,
    params=dict(adx_min=30, ema_n=20, hold=5),
    grid=[dict(adx_min=a, ema_n=e, hold=5) for a in (25, 30, 35) for e in (15, 20, 25)],  # 9
    meseta=(("adx_min", [20, 25, 30, 35, 40]), ("ema_n", [10, 15, 20, 25, 30])),
    config=dict(stop_atr=2.0, max_barras=5),
)
