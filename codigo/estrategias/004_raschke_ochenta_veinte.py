"""004 · raschke_ochenta_veinte — patrón 80-20 de reversión de un día (ambos lados).

Raschke & Connors, *Street Smarts* (1995), "80-20's" (de Taylor vía Crabel): un día que abre en
el extremo alto de su rango y cierra en el extremo bajo agota a los vendedores; al día siguiente
suele revertir. Y el espejo. Se exige rango amplio para no operar días sin contenido.

La señal es una función de ≤30 líneas. El motor de ejecución, las métricas y las 5 fases de
validación viven en `codigo/quantlab/`; aquí solo se define QUÉ se opera, no CÓMO se ejecuta.

Look-ahead: el filtro de rango compara contra el ATR **previo** (`shift(1)`) y el motor ejecuta
en la APERTURA de la barra siguiente al evento.

VEREDICTO 2026-09-15: DESCARTADA. PF OOS 1.15 / 1.16. El lado largo tenía tendencia real
(p = 0.018) pero el corto es continuación, no reversión; juntos dan PF 0.74 en IS. Acta:
`reportes/004_raschke_ochenta_veinte/RESUMEN.md`.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from quantlab.indicators import atr


def senal(df: pd.DataFrame, pct: float = 0.2, hold: int = 1, atr_mult_rango: float = 1.0,
          atr_n: int = 10) -> pd.Series:
    """1 = largo, -1 = corto, 0 = fuera. Día que abre en el `pct` superior de su rango y cierra
    en el `pct` inferior → largo al día siguiente; el espejo → corto. Solo si el rango del día
    ≥ `atr_mult_rango` × ATR(atr_n) previo. El stop (1.5×ATR) y el tope de 1 barra los pone el motor."""
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


PLAN = dict(
    fn=senal,
    params=dict(pct=0.2, hold=1, atr_mult_rango=1.0),
    grid=[dict(pct=p, hold=1, atr_mult_rango=m) for p in (0.15, 0.2, 0.25) for m in (0.8, 1.0, 1.2)],  # 9
    meseta=(("pct", [0.1, 0.15, 0.2, 0.25, 0.3]), ("atr_mult_rango", [0.6, 0.8, 1.0, 1.2, 1.4])),
    config=dict(stop_atr=1.5, max_barras=1),
)
