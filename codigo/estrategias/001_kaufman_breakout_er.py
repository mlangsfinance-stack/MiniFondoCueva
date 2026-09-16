"""001 · kaufman_breakout_er — ruptura de canal N días filtrada por Efficiency Ratio (solo largos).

Kaufman, *Trading Systems and Methods* (5ª ed.): cap. 5 (N-day breakout) y cap. 17 (Efficiency
Ratio). *Smarter Trading*: los sistemas de ruptura fallan cuando el ratio señal/ruido es bajo.

La señal es una función de ≤30 líneas. El motor de ejecución, las métricas y las 5 fases de
validación viven en `codigo/quantlab/`; aquí solo se define QUÉ se opera, no CÓMO se ejecuta.

Look-ahead: `maximo_previo` y `minimo_previo` excluyen la barra actual (shift(1)), y el motor
ejecuta cada señal en la APERTURA de la barra siguiente. Ninguna señal usa datos de su propia barra.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from quantlab.indicators import efficiency_ratio, maximo_previo, minimo_previo


def senal(df: pd.DataFrame, n_entrada: int = 40, n_salida: int = 20, er_n: int = 10,
          er_min: float = 0.3) -> pd.Series:
    """1 = largo, 0 = fuera. Entra si close > máx(high) de n_entrada barras previas y ER(er_n) ≥ er_min.
    Sale si close < mín(low) de n_salida barras previas. El stop catastrófico (3×ATR) lo pone el motor."""
    er = efficiency_ratio(df["close"], er_n)
    entra = (df["close"] > maximo_previo(df["high"], n_entrada)) & (er >= er_min)
    sale = df["close"] < minimo_previo(df["low"], n_salida)
    pos = pd.Series(np.nan, index=df.index)
    pos[sale] = 0
    pos[entra] = 1
    return pos.ffill().fillna(0).astype(int)


# Plan de validación: parámetros por defecto (los de Kaufman, no salen de buscar), rejilla de
# walk-forward (pequeña: pasos gruesos, rangos amplios) y ejes de la meseta 5×5.
PLAN = dict(
    fn=senal,
    params=dict(n_entrada=40, n_salida=20, er_n=10, er_min=0.3),
    grid=[dict(n_entrada=a, n_salida=20, er_n=10, er_min=b) for a in (20, 40, 60) for b in (0.2, 0.3, 0.4)]
         + [dict(n_entrada=40, n_salida=10, er_n=10, er_min=0.3), dict(n_entrada=40, n_salida=40, er_n=10, er_min=0.3)],
    meseta=(("n_entrada", [20, 30, 40, 50, 60]), ("er_min", [0.1, 0.2, 0.3, 0.4, 0.5])),
    # Stop ancho a propósito: en un breakout la salida principal es el canal; 2×ATR cae dentro
    # del ruido normal de un movimiento de 40 días.
    config=dict(stop_atr=3.0),
)
