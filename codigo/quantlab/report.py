"""RESUMEN.md: lo único que se lee después de una validación. Máximo 40 líneas."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .validation import _cmp


def _f(v) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        if np.isnan(v):
            return "n/a"
        if np.isinf(v):
            return "inf"
        return f"{v:.3f}" if abs(v) < 10 else f"{v:.1f}"
    return str(v)


def resumen_md(nombre: str, r: dict) -> str:
    L = [f"# {nombre} — RESUMEN de validación", "",
         f"**Veredicto: {r['veredicto']}**  ·  params: `{r['params']}`", ""]
    f1 = r["fases"]["1_is_oos"]
    cols = {"IS": f1["is"], "OOS": f1["oos"], **{f"OOS {k}": v for k, v in f1.get("oos_extra", {}).items()}}
    L += ["| métrica | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for k in ("n_trades", "profit_factor", "pf_sin_mejor", "pf_sin_top5", "cagr", "max_dd", "sharpe",
              "expectancia_R", "win_rate", "t_stat"):
        L.append(f"| {k} | " + " | ".join(_f(m[k]) for m in cols.values()) + " |")
    L += ["", "| fase | check | valor | umbral | ok |", "|---|---|---|---|---|"]
    for fase, d in r["fases"].items():
        for nombre_c, (v, op, u) in d["checks"].items():
            ok = "OK" if _cmp(v, op, u) else "FALLA"
            L.append(f"| {fase} | {nombre_c} | {_f(v)} | {op} {_f(u)} | {ok} |")
    f2 = r["fases"]["2_walk_forward"]["tabla"]
    if len(f2):
        L += ["", "Walk-forward por ventana (cagr OOS): " + ", ".join(_f(x) for x in f2["cagr_oos"])]
    L += ["", f"Stress — PF por tercios: {[round(x, 2) for x in r['fases']['5_stress']['pf_tercios']]}"]
    return "\n".join(L) + "\n"


def guardar(nombre: str, r: dict, carpeta: str | Path = "reportes") -> Path:
    destino = Path(carpeta) / nombre
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "RESUMEN.md").write_text(resumen_md(nombre, r), encoding="utf-8")
    r["fases"]["3_meseta"]["superficie"].to_csv(destino / "meseta.csv")
    r["fases"]["2_walk_forward"]["tabla"].to_csv(destino / "walk_forward.csv", index=False)
    r["fases"]["1_is_oos"]["trades_oos"].to_csv(destino / "trades_oos.csv", index=False)
    return destino / "RESUMEN.md"
