"""Charts y curvas de las validaciones NDX → reportes/ndx_charts.html (plotly, autocontenido).

Por estrategia: equity Norgate (IS sombreado / OOS) + equity Darwinex, drawdown,
meseta de parámetros (IS), walk-forward por ventana y cono bootstrap de los trades OOS.
Arriba: las 4 curvas OOS (2016+) juntas. Uso: python codigo/scripts/05_charts_ndx.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from quantlab import backtest, data, senales_kaufman, senales_raschke

RAIZ = Path(__file__).resolve().parents[2]
CORTE = pd.Timestamp("2016-01-01")
COSTE = 0.0002
PLANES = {**senales_kaufman.PLANES, **senales_raschke.PLANES}
ORDEN = ["breakout_er", "mr_2dias", "holy_grail", "ochenta_veinte"]
ETIQUETA = {"breakout_er": "Breakout + ER (Kaufman)", "mr_2dias": "Reversión 2 días (Kaufman)",
            "holy_grail": "Holy Grail (Raschke)", "ochenta_veinte": "80-20 (Raschke)"}
# La fusión de 2026-09-16 renombró reportes/ndx_<senal>/ a reportes/<ID>_<nombre>/.
CARPETA = {"breakout_er": "001_kaufman_breakout_er", "mr_2dias": "002_kaufman_mr_2dias",
           "holy_grail": "003_raschke_holy_grail", "ochenta_veinte": "004_raschke_ochenta_veinte"}
# paleta categórica en orden fijo (dataviz): azul, naranja, aqua, amarillo
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, MUTED, GRID, SURF = "#0b0b0b", "#898781", "#e1e0d9", "#fcfcfb"
LAYOUT = dict(paper_bgcolor=SURF, plot_bgcolor=SURF, font=dict(color=INK, size=12),
              hovermode="x unified", margin=dict(l=50, r=20, t=60, b=40),
              legend=dict(orientation="h", y=1.08, x=0))
EJE = dict(gridcolor=GRID, zerolinecolor="#c3c2b7", tickfont=dict(color=MUTED), linecolor="#c3c2b7")

norgate = data.cargar(RAIZ / "data/ndx_norgate_d1.parquet")
darwinex = data.cargar(RAIZ / "data/ndx_darwinex_d1.parquet")


def curva(df, plan):
    cfg = backtest.Config(coste_pct=COSTE, riesgo_pct=0.01, **plan.get("config", {}))
    res = backtest.backtest(df, plan["fn"](df, **plan["params"]), cfg)
    return res.equity / cfg.capital - 1, res.trades


def cono(trades_oos: pd.DataFrame, n_sim=1000, seed=0):
    r = trades_oos["pnl_pct"].to_numpy(float)
    rng = np.random.default_rng(seed)
    sims = np.cumprod(1 + rng.choice(r, size=(n_sim, len(r)), replace=True), axis=1) - 1
    return np.percentile(sims, [5, 50, 95], axis=0), np.cumprod(1 + r) - 1


def fig_estrategia(nombre, plan, color):
    eq_n, _ = curva(norgate, plan)
    eq_d, _ = curva(darwinex, plan)
    dd = (1 + eq_n) / (1 + eq_n).cummax() - 1
    carpeta = RAIZ / "reportes" / CARPETA[nombre]
    meseta = pd.read_csv(carpeta / "meseta.csv", index_col=0)
    wf = pd.read_csv(carpeta / "walk_forward.csv")
    trades_oos = pd.read_csv(carpeta / "trades_oos.csv")
    (p5, p50, p95), real = cono(trades_oos)

    fig = make_subplots(
        rows=3, cols=3, row_heights=[0.45, 0.2, 0.35], vertical_spacing=0.09, horizontal_spacing=0.08,
        specs=[[{"colspan": 3}, None, None], [{"colspan": 3}, None, None], [{}, {}, {}]],
        subplot_titles=("Equity (retorno acumulado sobre capital)", "Drawdown Norgate",
                        f"Meseta IS: PF por {meseta.index.name} × {meseta.columns.name}",
                        "Walk-forward: CAGR OOS por ventana", "Cono bootstrap trades OOS (p5 / p50 / p95)"))
    # 1) equity
    fig.add_vrect(x0=norgate.index[0], x1=CORTE, fillcolor="#e1e0d9", opacity=0.35, line_width=0,
                  annotation_text="IS", annotation_position="top left", row=1, col=1)
    fig.add_vrect(x0=CORTE, x1=norgate.index[-1], fillcolor=SURF, opacity=0, line_width=0,
                  annotation_text="OOS", annotation_position="top left", row=1, col=1)
    fig.add_trace(go.Scatter(x=eq_n.index, y=eq_n * 100, name="Norgate (índice, 1985→)", line=dict(color=CAT[0], width=2),
                             hovertemplate="%{y:.1f} %"), row=1, col=1)
    fig.add_trace(go.Scatter(x=eq_d.index, y=eq_d * 100, name="Darwinex (CFD, 2008→)", line=dict(color=CAT[1], width=2),
                             hovertemplate="%{y:.1f} %"), row=1, col=1)
    # 2) drawdown
    fig.add_trace(go.Scatter(x=dd.index, y=dd * 100, name="Drawdown", line=dict(color=CAT[0], width=1.5),
                             fill="tozeroy", fillcolor="rgba(42,120,214,0.15)", showlegend=False,
                             hovertemplate="%{y:.1f} %"), row=2, col=1)
    # 3) meseta
    fig.add_trace(go.Heatmap(z=meseta.values, x=[str(c) for c in meseta.columns], y=[str(i) for i in meseta.index],
                             colorscale=[[0, "#cde2fb"], [1, "#0d366b"]], zmin=0.5, zmax=max(2.5, np.nanmax(meseta.values)),
                             colorbar=dict(title="PF", x=0.29, len=0.3, y=0.15), showscale=True,
                             text=np.round(meseta.values, 2), texttemplate="%{text}", textfont=dict(size=10),
                             hovertemplate=f"{meseta.index.name}=%{{y}} · {meseta.columns.name}=%{{x}}<br>PF %{{z:.2f}}<extra></extra>"),
                  row=3, col=1)
    # 4) walk-forward
    cols_wf = [CAT[2] if v > 0 else "#e34948" for v in wf["cagr_oos"].fillna(0)]
    fig.add_trace(go.Bar(x=[f"V{k + 1}" for k in wf["ventana"]], y=wf["cagr_oos"] * 100, marker_color=cols_wf,
                         showlegend=False, hovertemplate="CAGR OOS %{y:.2f} %<extra></extra>"), row=3, col=2)
    # 5) cono
    idx = np.arange(1, len(real) + 1)
    fig.add_trace(go.Scatter(x=idx, y=p95 * 100, line=dict(width=0), showlegend=False, hoverinfo="skip"), row=3, col=3)
    fig.add_trace(go.Scatter(x=idx, y=p5 * 100, line=dict(width=0), fill="tonexty", fillcolor="rgba(42,120,214,0.15)",
                             showlegend=False, hoverinfo="skip"), row=3, col=3)
    fig.add_trace(go.Scatter(x=idx, y=p50 * 100, name="p50 bootstrap", line=dict(color=MUTED, width=1.5, dash="dot"),
                             showlegend=False, hovertemplate="p50 %{y:.1f} %"), row=3, col=3)
    fig.add_trace(go.Scatter(x=idx, y=real * 100, name="OOS real", line=dict(color=color, width=2),
                             showlegend=False, hovertemplate="real %{y:.1f} %"), row=3, col=3)

    fig.update_layout(height=900, title=dict(text=f"{ETIQUETA[nombre]} — params {plan['params']}", x=0), **LAYOUT)
    fig.update_xaxes(**EJE)
    fig.update_yaxes(**EJE)
    fig.update_yaxes(ticksuffix=" %", row=1, col=1)
    fig.update_yaxes(ticksuffix=" %", row=2, col=1)
    fig.update_yaxes(ticksuffix=" %", row=3, col=2)
    fig.update_yaxes(ticksuffix=" %", row=3, col=3)
    fig.update_xaxes(title_text="nº trade OOS", row=3, col=3)
    fig.update_xaxes(title_text=meseta.columns.name, row=3, col=1)
    fig.update_yaxes(title_text=meseta.index.name, row=3, col=1)
    return fig


def fig_resumen():
    fig = make_subplots(rows=1, cols=2, subplot_titles=("OOS Norgate 2016+ (rebasado a 0)", "OOS Darwinex 2016+ (rebasado a 0)"),
                        horizontal_spacing=0.07)
    for k, nombre in enumerate(ORDEN):
        for col, df in ((1, norgate), (2, darwinex)):
            eq, _ = curva(df[df.index >= CORTE - pd.Timedelta(days=400)], PLANES[nombre])  # warm-up de indicadores
            eq = eq[eq.index >= CORTE]
            eq = (1 + eq) / (1 + eq.iloc[0]) - 1
            fig.add_trace(go.Scatter(x=eq.index, y=eq * 100, name=ETIQUETA[nombre], legendgroup=nombre,
                                     showlegend=(col == 1), line=dict(color=CAT[k], width=2),
                                     hovertemplate="%{y:.1f} %"), row=1, col=col)
    fig.update_layout(height=460, title=dict(text="Las 4 estrategias en el OOS — mismo sizing (1 % riesgo), 2 pb/lado", x=0), **LAYOUT)
    fig.update_xaxes(**EJE)
    fig.update_yaxes(**EJE, ticksuffix=" %")
    return fig


if __name__ == "__main__":
    partes = ["<html><head><meta charset='utf-8'><title>NDX — charts y curvas</title>"
              f"<style>body{{font-family:Inter,Segoe UI,sans-serif;background:#f9f9f7;color:{INK};margin:24px}}"
              "h1{font-size:22px}h2{font-size:16px;color:#52514e;margin-top:36px}"
              ".nota{font-size:13px;color:#52514e;max-width:900px}</style></head><body>",
              "<h1>NDX — validación de 4 estrategias: charts y curvas</h1>",
              "<p class='nota'>IS = Norgate &lt; 2016 (zona gris) · OOS = 2016+ en Norgate y Darwinex · costes 2 pb/lado · riesgo 1 % por trade, stop ATR. "
              "Las 4 están <b>descartadas</b>; el acta numérica está en <code>reportes/&lt;ID&gt;_*/RESUMEN.md</code>.</p>",
              fig_resumen().to_html(full_html=False, include_plotlyjs=True)]
    for k, nombre in enumerate(ORDEN):
        partes.append(f"<h2>{ETIQUETA[nombre]}</h2>")
        partes.append(fig_estrategia(nombre, PLANES[nombre], CAT[k]).to_html(full_html=False, include_plotlyjs=False))
    partes.append("</body></html>")
    salida = RAIZ / "reportes" / "ndx_charts.html"
    salida.write_text("\n".join(partes), encoding="utf-8")
    print(f"-> {salida}")
