"""Protocolo de validación en 5 fases. Los umbrales viven en ``Criterios`` y
son defaults calibrables; cambiarlos para una estrategia concreta se anota en
su ficha con el motivo. No se omite ninguna fase.

Fase 1  IS/OOS          el edge sobrevive a datos no vistos
Fase 2  Walk-forward    sobrevive a re-optimizar en el tiempo
Fase 3  Meseta          sobrevive a mover los parámetros (Kaufman)
Fase 4  Monte Carlo     sobrevive a reordenar la suerte
Fase 5  Stress          sobrevive a costes, a perder los mejores años y al peor régimen
"""
from __future__ import annotations

import itertools
from dataclasses import asdict, dataclass, replace
from typing import Callable

import numpy as np
import pandas as pd

from .backtest import Config, Resultado, backtest
from .data import split_is_oos, ventanas_walk_forward
from .metrics import metricas, pnl_por_anio, profit_factor

FnSenal = Callable[..., pd.Series]


@dataclass
class Criterios:
    # Fase 1
    pf_oos_min: float = 1.3
    trades_oos_min: int = 30
    maxdd_oos_max: float = 0.20
    pf_sin_mejor_min: float = 1.0
    # Concentración (TIS): PF quitando las 5 mejores operaciones. Si la estrategia se vuelve
    # plana al quitarlas, no hay edge: hay cinco eventos afortunados. Con el mínimo de 30
    # trades OOS el test siempre es evaluable; por debajo devuelve nan y cuenta como fallo,
    # pero ahí ya falla también `trades_oos`.
    pf_sin_top5_min: float = 1.0
    # Fase 2
    wf_eficiencia_min: float = 0.5
    wf_ventanas_pos_min: float = 0.6
    # Fase 3
    meseta_caida_max: float = 0.30     # ningún vecino cae más de un 30 % respecto al centro
    meseta_pf_min: float = 1.2         # todos los vecinos de la meseta 3x3 por encima de esto
    # Fase 4
    mc_p5_retorno_min: float = 0.0
    mc_p95_dd_max: float = 0.25
    mc_ruina_dd: float = 0.35          # qué DD se considera ruina
    mc_ruina_max: float = 0.05
    # Fase 5
    stress_pf_min: float = 1.1


def evaluar(df: pd.DataFrame, fn: FnSenal, params: dict, cfg: Config) -> tuple[Resultado, dict]:
    res = backtest(df, fn(df, **params), cfg)
    return res, metricas(res)


# ---------------------------------------------------------------- Fase 1
def _checks_oos(m: dict, crit: Criterios, sufijo: str = "") -> dict:
    return {
        f"pf_oos{sufijo}": (m["profit_factor"], ">=", crit.pf_oos_min),
        f"trades_oos{sufijo}": (m["n_trades"], ">=", crit.trades_oos_min),
        f"maxdd_oos{sufijo}": (abs(m["max_dd"]), "<", crit.maxdd_oos_max),
        f"pf_sin_mejor_oos{sufijo}": (m["pf_sin_mejor"], ">", crit.pf_sin_mejor_min),
        f"pf_sin_top5_oos{sufijo}": (m["pf_sin_top5"], ">", crit.pf_sin_top5_min),
    }


def fase_is_oos(df, fn, params, cfg, crit: Criterios, corte=0.7, oos_extra: dict | None = None) -> dict:
    """``oos_extra`` = {"nombre": df_otra_serie}: se evalúa su tramo >= corte con los
    mismos criterios (p. ej. el instrumento real además del índice)."""
    d_is, d_oos = split_is_oos(df, corte)
    _, m_is = evaluar(d_is, fn, params, cfg)
    res_oos, m_oos = evaluar(d_oos, fn, params, cfg)
    checks = _checks_oos(m_oos, crit)
    extra = {}
    for nombre, d2 in (oos_extra or {}).items():
        _, d2_oos = split_is_oos(d2, corte) if isinstance(corte, str) else (None, d2)
        _, m2 = evaluar(d2_oos, fn, params, cfg)
        extra[nombre] = m2
        checks.update(_checks_oos(m2, crit, f"_{nombre}"))
    return {"is": m_is, "oos": m_oos, "oos_extra": extra, "checks": checks, "pasa": _todo(checks),
            "trades_oos": res_oos.trades}


# ---------------------------------------------------------------- Fase 2
def fase_walk_forward(df, fn, grid: list[dict], cfg, crit: Criterios, n_ventanas=5, frac_is=0.7,
                      objetivo="profit_factor") -> dict:
    """En cada ventana elige los params con mejor ``objetivo`` en IS y los aplica
    al OOS. Eficiencia WF = retorno anualizado OOS / retorno anualizado IS."""
    filas, ret_is, ret_oos = [], [], []
    for k, (d_is, d_oos) in enumerate(ventanas_walk_forward(df, n_ventanas, frac_is)):
        mejor, mejor_m = None, None
        for p in grid:
            _, m = evaluar(d_is, fn, p, cfg)
            if m["n_trades"] >= 10 and (mejor_m is None or m[objetivo] > mejor_m[objetivo]):
                mejor, mejor_m = p, m
        if mejor is None:
            filas.append({"ventana": k, "params": None, "cagr_is": np.nan, "cagr_oos": np.nan, "pf_oos": np.nan, "n_oos": 0})
            continue
        _, m_oos = evaluar(d_oos, fn, mejor, cfg)
        filas.append({"ventana": k, "params": mejor, "cagr_is": mejor_m["cagr"], "cagr_oos": m_oos["cagr"],
                      "pf_oos": m_oos["profit_factor"], "n_oos": m_oos["n_trades"]})
        ret_is.append(mejor_m["cagr"])
        ret_oos.append(m_oos["cagr"])
    tabla = pd.DataFrame(filas)
    eficiencia = (np.mean(ret_oos) / np.mean(ret_is)) if ret_is and np.mean(ret_is) > 0 else 0.0
    pct_pos = float(np.mean([r > 0 for r in ret_oos])) if ret_oos else 0.0
    checks = {"wf_eficiencia": (float(eficiencia), ">=", crit.wf_eficiencia_min),
              "wf_ventanas_pos": (pct_pos, ">=", crit.wf_ventanas_pos_min)}
    return {"tabla": tabla, "checks": checks, "pasa": _todo(checks)}


# ---------------------------------------------------------------- Fase 3
def fase_meseta(df, fn, params, p1: tuple[str, list], p2: tuple[str, list], cfg, crit: Criterios,
                objetivo="profit_factor") -> dict:
    """Superficie objetivo sobre dos parámetros. Se busca meseta, no pico:
    el centro y sus 8 vecinos deben estar por encima de ``meseta_pf_min`` y
    ninguno caer más de ``meseta_caida_max`` respecto al centro."""
    n1, v1 = p1
    n2, v2 = p2
    sup = pd.DataFrame(index=v1, columns=v2, dtype=float)
    for a, b in itertools.product(v1, v2):
        _, m = evaluar(df, fn, {**params, n1: a, n2: b}, cfg)
        sup.loc[a, b] = m[objetivo] if m["n_trades"] >= 10 else np.nan
    sup.index.name, sup.columns.name = n1, n2
    i = v1.index(params[n1]) if params[n1] in v1 else len(v1) // 2
    j = v2.index(params[n2]) if params[n2] in v2 else len(v2) // 2
    i0, i1, j0, j1 = max(i - 1, 0), min(i + 2, len(v1)), max(j - 1, 0), min(j + 2, len(v2))
    vecinos = sup.iloc[i0:i1, j0:j1].to_numpy(float)
    centro = float(sup.iloc[i, j])
    vec_validos = vecinos[~np.isnan(vecinos)]
    caida = float(1 - vec_validos.min() / centro) if centro > 0 and len(vec_validos) else 1.0
    checks = {"meseta_es_3x3": (int((~np.isnan(vecinos)).sum()), ">=", 9),
              "meseta_min_vecino": (float(vec_validos.min()) if len(vec_validos) else 0.0, ">=", crit.meseta_pf_min),
              "meseta_caida": (caida, "<=", crit.meseta_caida_max)}
    return {"superficie": sup, "centro": centro, "checks": checks, "pasa": _todo(checks)}


# ---------------------------------------------------------------- Fase 4
def fase_monte_carlo(trades: pd.DataFrame, crit: Criterios, n_sim=5000, seed=0) -> dict:
    """Bootstrap: remuestrea n trades CON reemplazo n_sim veces (retorno % sobre
    equity, compuesto) y mira colas. No se permuta el orden: el retorno final es
    invariante a la permutación y solo variaría el DD."""
    rng = np.random.default_rng(seed)
    r = trades["pnl_pct"].to_numpy(float)
    if len(r) == 0:
        checks = {"mc_p5_retorno": (0.0, ">", crit.mc_p5_retorno_min), "mc_p95_dd": (1.0, "<", crit.mc_p95_dd_max),
                  "mc_ruina": (1.0, "<", crit.mc_ruina_max)}
        return {"p50_retorno": 0.0, "p50_dd": 0.0, "checks": checks, "pasa": False}
    finales, dds = np.empty(n_sim), np.empty(n_sim)
    for k in range(n_sim):
        eq = np.cumprod(1 + rng.choice(r, size=len(r), replace=True))
        finales[k] = eq[-1] - 1
        dds[k] = (eq / np.maximum.accumulate(eq) - 1).min()
    ruina = float((dds <= -crit.mc_ruina_dd).mean())
    checks = {"mc_p5_retorno": (float(np.percentile(finales, 5)), ">", crit.mc_p5_retorno_min),
              "mc_p95_dd": (float(-np.percentile(dds, 5)), "<", crit.mc_p95_dd_max),
              "mc_ruina": (ruina, "<", crit.mc_ruina_max)}
    return {"p50_retorno": float(np.median(finales)), "p50_dd": float(-np.median(dds)),
            "checks": checks, "pasa": _todo(checks)}


# ---------------------------------------------------------------- Fase 5
def fase_stress(df, fn, params, cfg, crit: Criterios, corte=0.7) -> dict:
    """Tres golpes: costes x2 en OOS; PF total sin los 2 mejores años; PF del
    peor tercio de la muestra. Todos deben quedar por encima de stress_pf_min."""
    _, d_oos = split_is_oos(df, corte)
    _, m_costes = evaluar(d_oos, fn, params, replace(cfg, coste_pct=cfg.coste_pct * 2))
    res_tot, _ = evaluar(df, fn, params, cfg)
    anual = pnl_por_anio(res_tot.trades)
    peores = anual.drop(anual.nlargest(2).index).index if len(anual) > 2 else anual.index
    t = res_tot.trades
    pf_sin_mejores = profit_factor(t[t["salida"].dt.year.isin(peores)]["pnl"]) if len(t) else 0.0
    tercio = len(df) // 3
    pf_tercios = []
    for k in range(3):
        _, m = evaluar(df.iloc[k * tercio:(k + 1) * tercio if k < 2 else len(df)], fn, params, cfg)
        pf_tercios.append(m["profit_factor"])
    checks = {"stress_costes_x2_pf_oos": (m_costes["profit_factor"], ">=", crit.stress_pf_min),
              "stress_sin_2_mejores_anios_pf": (pf_sin_mejores, ">=", crit.stress_pf_min),
              "stress_peor_tercio_pf": (float(min(pf_tercios)), ">=", crit.stress_pf_min)}
    return {"pf_tercios": pf_tercios, "checks": checks, "pasa": _todo(checks)}


# ---------------------------------------------------------------- Todo junto
def validar(df: pd.DataFrame, fn: FnSenal, params: dict, grid: list[dict], meseta: tuple[tuple, tuple],
            cfg: Config | None = None, crit: Criterios | None = None, corte=0.7, n_ventanas=5,
            n_sim=5000, oos_extra: dict | None = None, meseta_solo_is: bool = True) -> dict:
    """``corte``: fracción o fecha ("2016-01-01"). ``oos_extra``: otras series cuyo tramo
    OOS también debe pasar Fase 1. La meseta se calcula sobre IS (no toca el OOS)."""
    cfg, crit = cfg or Config(), crit or Criterios()
    d_is, _ = split_is_oos(df, corte)
    f1 = fase_is_oos(df, fn, params, cfg, crit, corte, oos_extra)
    f2 = fase_walk_forward(df, fn, grid, cfg, crit, n_ventanas, 0.7)
    f3 = fase_meseta(d_is if meseta_solo_is else df, fn, params, meseta[0], meseta[1], cfg, crit)
    f4 = fase_monte_carlo(f1["trades_oos"], crit, n_sim)
    f5 = fase_stress(df, fn, params, cfg, crit, corte)
    fases = {"1_is_oos": f1, "2_walk_forward": f2, "3_meseta": f3, "4_monte_carlo": f4, "5_stress": f5}
    pasa = all(f["pasa"] for f in fases.values())
    frontera = crit.pf_oos_min - 0.05 <= f1["oos"]["profit_factor"] <= crit.pf_oos_min + 0.05
    veredicto = "VALIDADA" if pasa else ("FRONTERA - revisar a mano" if frontera else "DESCARTADA")
    return {"params": params, "config": asdict(cfg), "criterios": asdict(crit), "fases": fases,
            "pasa": pasa, "veredicto": veredicto}


def _cmp(v, op, u) -> bool:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return False
    return {">": v > u, ">=": v >= u, "<": v < u, "<=": v <= u}[op]


def _todo(checks: dict) -> bool:
    return all(_cmp(*c) for c in checks.values())
