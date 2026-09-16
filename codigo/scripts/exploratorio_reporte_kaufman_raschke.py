"""Reporte visual de los backtests de Kaufman y Raschke sobre NDX: métricas, curvas de equity,
drawdown y heatmaps de meseta. No optimiza nada: reproduce cada señal con sus parámetros por
defecto y el mismo setup que codigo/scripts/04_validar_ndx.py (Norgate, IS < 2016, OOS >= 2016, 2 pb/lado).

Uso:  python scripts/exploratorio_reporte_kaufman_raschke.py
Escribe reportes/kaufman_raschke/REPORTE.md + PNGs.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))
from quantlab import backtest, data, metrics, senales, senales_kaufman, senales_raschke  # noqa: E402
from quantlab.validation import fase_meseta, Criterios  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "reportes" / "kaufman_raschke"
OUT.mkdir(parents=True, exist_ok=True)
CORTE = pd.Timestamp("2016-01-01")
COSTE_LADO = 0.0002

# Paleta (dataviz/palette.md): IS azul, OOS naranja, sequential azul para heatmaps.
AZUL, NARANJA, GRIS, TEXTO, TEXTO2 = "#2a78d6", "#eb6834", "#c3c2b7", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": GRIS, "axes.labelcolor": TEXTO2, "xtick.color": TEXTO2,
                     "ytick.color": TEXTO2, "grid.color": "#ebeae7", "figure.facecolor": "#fcfcfb",
                     "axes.facecolor": "#fcfcfb"})

# Señal, plan y escuela. kama_tendencia solo tenía validación sintética: aquí se corre en NDX por primera vez.
PLANES = {
    "breakout_er":    ("Kaufman", senales_kaufman.PLANES["breakout_er"]),
    "mr_2dias":       ("Kaufman", senales_kaufman.PLANES["mr_2dias"]),
    "kama_tendencia": ("Kaufman", dict(fn=senales.kama_tendencia, params={"n": 10, "er_min": 0.3},
                                       meseta=(("n", [6, 8, 10, 14, 20]), ("er_min", [0.1, 0.2, 0.3, 0.4, 0.5])),
                                       config={})),
    "holy_grail":     ("Raschke", senales_raschke.PLANES["holy_grail"]),
    "ochenta_veinte": ("Raschke", senales_raschke.PLANES["ochenta_veinte"]),
}

df = data.cargar(RAIZ / "data" / "ndx_norgate_d1.parquet")
d_is = df[df.index < CORTE]


def correr(fn, params, cfg, d):
    return backtest.backtest(d, fn(d, **params), cfg)


def fmt(m):
    return {k: (f"{v:.3f}" if isinstance(v, float) and np.isfinite(v) else str(v)) for k, v in m.items()}


filas, curvas = [], {}
for nombre, (escuela, plan) in PLANES.items():
    cfg = backtest.Config(coste_pct=COSTE_LADO, riesgo_pct=0.01, **plan.get("config", {}))
    fn, params = plan["fn"], plan["params"]
    # Curva completa (equity encadenada) + métricas por tramo, cada tramo con su capital inicial.
    r_full = correr(fn, params, cfg, df)
    r_is = correr(fn, params, cfg, df[df.index < CORTE])
    r_oos = correr(fn, params, cfg, df[df.index >= CORTE])
    m_is, m_oos = metrics.metricas(r_is), metrics.metricas(r_oos)
    curvas[nombre] = (escuela, r_full, r_is, r_oos)
    for tramo, m in (("IS", m_is), ("OOS", m_oos)):
        filas.append({"escuela": escuela, "senal": nombre, "tramo": tramo, **m})
    # Meseta sobre IS (nunca OOS), PF como objetivo, igual que validation.validar.
    sup = fase_meseta(d_is, fn, params, plan["meseta"][0], plan["meseta"][1], cfg, Criterios())["superficie"]
    sup.to_csv(OUT / f"meseta_{nombre}.csv")
    curvas[nombre] += (sup,)
    print(f"{nombre:<16} IS PF {m_is['profit_factor']:.2f} DD {m_is['max_dd']:.1%} | OOS PF {m_oos['profit_factor']:.2f} DD {m_oos['max_dd']:.1%}")

tabla = pd.DataFrame(filas)
tabla.to_csv(OUT / "metricas.csv", index=False)

# ---------- Figura 1: curvas de equity (base 100) con IS/OOS ----------
fig, axes = plt.subplots(len(PLANES), 1, figsize=(10, 2.6 * len(PLANES)), sharex=True)
for ax, (nombre, (escuela, r_full, *_)) in zip(axes, curvas.items()):
    eq = r_full.equity / r_full.equity.iloc[0] * 100
    ax.plot(eq[eq.index < CORTE], color=AZUL, lw=1.6, label="IS")
    ax.plot(eq[eq.index >= CORTE], color=NARANJA, lw=1.6, label="OOS")
    ax.axvline(CORTE, color=GRIS, lw=1, ls="--")
    ax.set_title(f"{escuela} · {nombre}", loc="left", color=TEXTO, fontweight="bold")
    ax.grid(True, axis="y")
    ax.text(0.995, 0.05, f"fin {eq.iloc[-1]:.0f}", transform=ax.transAxes, ha="right", color=TEXTO2)
axes[0].legend(loc="upper left", frameon=False)
axes[-1].set_xlabel("NDX diario · Norgate · base 100 · riesgo 1 %/trade · 2 pb/lado")
fig.tight_layout()
fig.savefig(OUT / "equity.png", dpi=150)
plt.close(fig)

# ---------- Figura 2: drawdown ----------
fig, axes = plt.subplots(len(PLANES), 1, figsize=(10, 2.2 * len(PLANES)), sharex=True)
for ax, (nombre, (escuela, r_full, *_)) in zip(axes, curvas.items()):
    dd = (r_full.equity / r_full.equity.cummax() - 1) * 100
    ax.fill_between(dd.index, dd, 0, where=dd.index < CORTE, color=AZUL, alpha=0.35, lw=0)
    ax.fill_between(dd.index, dd, 0, where=dd.index >= CORTE, color=NARANJA, alpha=0.35, lw=0)
    ax.plot(dd, color=TEXTO2, lw=0.6)
    ax.axvline(CORTE, color=GRIS, lw=1, ls="--")
    ax.set_title(f"{escuela} · {nombre} · max DD {dd.min():.1f} %", loc="left", color=TEXTO, fontweight="bold")
    ax.set_ylim(min(dd.min() * 1.1, -1), 0.5)
    ax.grid(True, axis="y")
axes[-1].set_xlabel("Drawdown (%) sobre la curva encadenada · azul IS · naranja OOS")
fig.tight_layout()
fig.savefig(OUT / "drawdown.png", dpi=150)
plt.close(fig)

# ---------- Figura 3: heatmaps de meseta (PF en IS) ----------
fig, axes = plt.subplots(1, len(PLANES), figsize=(4.2 * len(PLANES), 4.2))
for ax, (nombre, (escuela, _, _, _, sup)) in zip(axes, curvas.items()):
    v = sup.to_numpy(float)
    im = ax.imshow(v, cmap="Blues", vmin=0.8, vmax=max(1.6, np.nanmax(v)), aspect="auto")
    ax.set_xticks(range(len(sup.columns)), [str(c) for c in sup.columns])
    ax.set_yticks(range(len(sup.index)), [str(i) for i in sup.index])
    ax.set_xlabel(sup.columns.name); ax.set_ylabel(sup.index.name)
    ax.set_title(f"{escuela} · {nombre}\nPF en IS", loc="left", color=TEXTO, fontsize=9, fontweight="bold")
    for i in range(v.shape[0]):
        for j in range(v.shape[1]):
            if np.isfinite(v[i, j]):
                ax.text(j, i, f"{v[i, j]:.2f}", ha="center", va="center", fontsize=7,
                        color="white" if v[i, j] > 1.35 else TEXTO)
    # centro = params por defecto
    p = PLANES[nombre][1]["params"]
    n1, n2 = sup.index.name, sup.columns.name
    if p[n1] in list(sup.index) and p[n2] in list(sup.columns):
        ax.add_patch(plt.Rectangle((list(sup.columns).index(p[n2]) - 0.5, list(sup.index).index(p[n1]) - 0.5),
                                   1, 1, fill=False, ec=NARANJA, lw=2))
    for s in ax.spines.values():
        s.set_visible(False)
fig.suptitle("Meseta: profit factor sobre IS (< 2016). Recuadro naranja = parámetros por defecto. Blanco = < 10 trades.",
             x=0.01, ha="left", color=TEXTO2, fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "heatmaps.png", dpi=150)
plt.close(fig)

# ---------- Figura 4: PnL por año OOS ----------
fig, axes = plt.subplots(1, len(PLANES), figsize=(3.6 * len(PLANES), 3), sharey=False)
for ax, (nombre, (escuela, _, _, r_oos, _)) in zip(axes, curvas.items()):
    pa = metrics.pnl_por_anio(r_oos.trades) / r_oos.config.capital * 100
    ax.bar(pa.index.astype(str), pa.values, color=[NARANJA if x >= 0 else TEXTO2 for x in pa.values], width=0.7)
    ax.axhline(0, color=GRIS, lw=1)
    ax.set_title(f"{nombre}", loc="left", color=TEXTO, fontsize=9, fontweight="bold")
    ax.tick_params(axis="x", rotation=60)
    ax.grid(True, axis="y")
fig.suptitle("PnL por año en OOS (% del capital inicial del tramo)", x=0.01, ha="left", color=TEXTO2, fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "pnl_anual_oos.png", dpi=150)
plt.close(fig)

# ---------- REPORTE.md ----------
cols = ["n_trades", "profit_factor", "pf_sin_mejor", "win_rate", "expectancia_R", "cagr", "max_dd", "sharpe", "mar", "t_stat", "trades_anio", "pct_stop"]
lineas = ["# Backtests Kaufman y Raschke sobre NDX — reporte visual", "",
          f"Setup común: NDX diario Norgate ({df.index[0].date()} → {df.index[-1].date()}), IS < 2016-01-01, OOS ≥ 2016-01-01, "
          "coste 2 pb por lado, riesgo 1 % del equity por trade, stop ATR según cada plan. Parámetros por defecto de cada señal, "
          "sin optimizar. Métricas de cada tramo calculadas con su propio capital inicial (100 k).", "",
          "Veredictos oficiales (5 fases, `reportes/<ID>_*/RESUMEN.md`): **todas DESCARTADAS**. `kama_tendencia` solo tenía "
          "validación sintética; aquí se corre en NDX por primera vez y **no** ha pasado por las 5 fases.", "",
          "![equity](equity.png)", "", "![drawdown](drawdown.png)", "", "![heatmaps](heatmaps.png)", "", "![pnl](pnl_anual_oos.png)", ""]
for escuela in ("Kaufman", "Raschke"):
    lineas += [f"## {escuela}", ""]
    for nombre in [n for n, (e, _) in PLANES.items() if e == escuela]:
        sub = tabla[tabla.senal == nombre].set_index("tramo")[cols].T
        lineas += [f"### {nombre}", "", "| métrica | IS | OOS |", "|---|---|---|"]
        for k, row in sub.iterrows():
            f = lambda v: f"{v:.3f}" if isinstance(v, float) and np.isfinite(v) else str(v)
            lineas.append(f"| {k} | {f(row['IS'])} | {f(row['OOS'])} |")
        lineas.append("")
lineas += ["## Ficheros", "", "- `metricas.csv` — tabla completa IS/OOS por señal",
           "- `meseta_<senal>.csv` — superficie PF en IS por señal (la del heatmap)",
           "- `equity.png`, `drawdown.png`, `heatmaps.png`, `pnl_anual_oos.png`", ""]
(OUT / "REPORTE.md").write_text("\n".join(lineas), encoding="utf-8")
print(f"-> {OUT / 'REPORTE.md'}")
