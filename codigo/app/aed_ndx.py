"""AED del NASDAQ-100 — app Streamlit.

Lanzar:  streamlit run app/aed_ndx.py

Las funciones de cálculo (sección "Cálculo puro") no tocan Streamlit y se
importan desde tests/test_aed_ndx.py. La UI vive en ``main()``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "codigo"))

from quantlab import data, indicators, tendencies  # noqa: E402

CORTE_OOS = "2016-01-01"
FICHEROS = {
    "Norgate (índice cash, 1985+)": RAIZ / "data" / "ndx_norgate_d1.parquet",
    "Darwinex (CFD, 2008+)": RAIZ / "data" / "ndx_darwinex_d1.parquet",
}
HORIZONTES = (1, 2, 3, 5, 10)
BARRAS_ANIO = 252

# Paleta sobria: 1 azul, 2 naranja, 3 aqua, base gris; estado verde / rojo.
C1, C2, C3, CGRIS = "#2a78d6", "#eb6834", "#1baf7a", "#8a8985"
C_OK, C_KO = "#008300", "#e34948"

EVENTOS = {
    "Holy Grail (Raschke)": {
        "desc": "ADX14 > mínimo, +DI > −DI, y retroceso a la EMA20 (low ≤ EMA20 < close). Continuación de tendencia.",
        "params": {"adx_min": ("ADX mínimo", 15, 45, 30, 1), "n_ema": ("Periodo EMA", 10, 50, 20, 1)},
    },
    "80-20 (Raschke)": {
        "desc": "Día que abre en el 20 % superior del rango y cierra en el 20 % inferior (rango ≥ ATR). "
                "Largo = reversión al alza al día siguiente; corto = el espejo.",
        "params": {"pct": ("Fracción del rango", 0.10, 0.30, 0.20, 0.05),
                   "n_atr": ("Periodo ATR", 5, 30, 10, 1),
                   "mult_atr": ("Rango mínimo (× ATR)", 0.5, 2.0, 1.0, 0.1)},
    },
    "Breakout + ER (Kaufman)": {
        "desc": "Cierre por encima del máximo de las n barras previas con Efficiency Ratio ≥ mínimo (ruptura en mercado eficiente).",
        "params": {"n": ("Barras del canal", 5, 100, 20, 5), "n_er": ("Periodo ER", 5, 30, 10, 1),
                   "er_min": ("ER mínimo", 0.0, 0.8, 0.3, 0.05)},
    },
    "Reversión 2 días (Kaufman)": {
        "desc": "Dos cierres consecutivos a la baja con el precio sobre la SMA200 (largo). Corto: dos al alza bajo la SMA200.",
        "params": {"n_dias": ("Cierres consecutivos", 2, 5, 2, 1), "n_sma": ("Periodo SMA", 50, 300, 200, 10)},
    },
}


# ----------------------------------------------------------------------------
# Cálculo puro (sin Streamlit)
# ----------------------------------------------------------------------------
def filtrar_periodo(df: pd.DataFrame, incluir_oos: bool) -> pd.DataFrame:
    return df if incluir_oos else df[df.index < pd.Timestamp(CORTE_OOS)]


def calcular_resumen(df: pd.DataFrame) -> dict:
    """Barras, fechas, CAGR, vol anualizada, MaxDD, % días positivos, curtosis, asimetría."""
    c = df["close"]
    r = c.pct_change().dropna()
    anios = max(len(c) / BARRAS_ANIO, 1e-9)
    return {
        "barras": int(len(df)),
        "desde": df.index[0].date(),
        "hasta": df.index[-1].date(),
        "cagr": float((c.iloc[-1] / c.iloc[0]) ** (1 / anios) - 1),
        "vol_anual": float(r.std() * np.sqrt(BARRAS_ANIO)),
        "max_dd": float((c / c.cummax() - 1).min()),
        "pct_dias_pos": float((r > 0).mean()),
        "curtosis": float(r.kurt()),
        "asimetria": float(r.skew()),
    }


def retornos_por_anio(df: pd.DataFrame) -> pd.Series:
    c = df["close"]
    return c.groupby(c.index.year).agg(lambda s: s.iloc[-1] / s.iloc[0] - 1)


def vol_rodante(df: pd.DataFrame, ventanas=(20, 60)) -> pd.DataFrame:
    r = df["close"].pct_change()
    return pd.DataFrame({f"vol_{n}": r.rolling(n).std() * np.sqrt(BARRAS_ANIO) for n in ventanas})


def comparar_series(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """Correlación de retornos en el solape y ratio de cierres (a / b)."""
    idx = a.index.intersection(b.index)
    if len(idx) < 3:
        return {"n_solape": int(len(idx)), "correlacion": np.nan, "ratio": pd.Series(dtype=float)}
    ra, rb = a.loc[idx, "close"].pct_change(), b.loc[idx, "close"].pct_change()
    return {"n_solape": int(len(idx)), "correlacion": float(ra.corr(rb)),
            "ratio": a.loc[idx, "close"] / b.loc[idx, "close"]}


def calcular_regimen(df: pd.DataFrame, n_adx: int = 14, n_er: int = 10, n_atr: int = 14) -> pd.DataFrame:
    adx_, pdi, mdi = indicators.adx(df, n_adx)
    return pd.DataFrame({"adx": adx_, "plus_di": pdi, "minus_di": mdi,
                         "er": indicators.efficiency_ratio(df["close"], n_er),
                         "atr": indicators.atr(df, n_atr)})


def regimen_por_anio(reg: pd.DataFrame, er_min: float = 0.3) -> pd.DataFrame:
    g = reg.groupby(reg.index.year)
    return pd.DataFrame({
        "pct_adx_30": g["adx"].apply(lambda s: (s > 30).mean()),
        "pct_adx_25": g["adx"].apply(lambda s: (s > 25).mean()),
        "dias_er_limpio": g["er"].apply(lambda s: int((s > er_min).sum())),
        "er_medio": g["er"].mean(),
        "barras": g.size(),
    })


def _espejo(df: pd.DataFrame) -> pd.DataFrame:
    """Serie invertida (1/precio) para evaluar el lado corto con las mismas funciones:
    un exceso > 0 sobre el espejo es favorable al corto."""
    return pd.DataFrame({"open": 1 / df["open"], "high": 1 / df["low"], "low": 1 / df["high"],
                         "close": 1 / df["close"]}, index=df.index)


def eventos(df: pd.DataFrame, nombre: str, **p) -> dict[str, tuple[pd.Series, pd.DataFrame]]:
    """Devuelve {etiqueta: (evento bool, df sobre el que evaluarlo)} para cada lado."""
    c = df["close"]
    if nombre.startswith("Holy Grail"):
        adx_, pdi, mdi = indicators.adx(df, 14)
        e = indicators.ema(c, int(p.get("n_ema", 20)))
        ev = (adx_ > p.get("adx_min", 30)) & (pdi > mdi) & (df["low"] <= e) & (c > e)
        return {"largo": (ev, df)}
    if nombre.startswith("80-20"):
        pct, mult = p.get("pct", 0.2), p.get("mult_atr", 1.0)
        rango = df["high"] - df["low"]
        a = indicators.atr(df, int(p.get("n_atr", 10)))
        pos_o = (df["open"] - df["low"]) / rango.replace(0, np.nan)
        pos_c = (c - df["low"]) / rango.replace(0, np.nan)
        amplio = rango >= mult * a.shift(1)
        largo = (pos_o >= 1 - pct) & (pos_c <= pct) & amplio
        corto = (pos_o <= pct) & (pos_c >= 1 - pct) & amplio
        return {"largo": (largo.fillna(False), df), "corto": (corto.fillna(False), _espejo(df))}
    if nombre.startswith("Breakout"):
        ev = (c > indicators.maximo_previo(df["high"], int(p.get("n", 20)))) & \
             (indicators.efficiency_ratio(c, int(p.get("n_er", 10))) >= p.get("er_min", 0.3))
        return {"largo": (ev.fillna(False), df)}
    if nombre.startswith("Reversión"):
        k, s = int(p.get("n_dias", 2)), indicators.sma(c, int(p.get("n_sma", 200)))
        baja = pd.concat([c.shift(i) < c.shift(i + 1) for i in range(k)], axis=1).all(axis=1)
        sube = pd.concat([c.shift(i) > c.shift(i + 1) for i in range(k)], axis=1).all(axis=1)
        return {"largo": ((baja & (c > s)).fillna(False), df), "corto": ((sube & (c < s)).fillna(False), _espejo(df))}
    raise ValueError(f"Evento desconocido: {nombre}")


def estudiar(df: pd.DataFrame, ev: pd.Series, n_sim: int = 500) -> dict:
    """Tabla de estudio_evento + prob_rango(h=3) + test_permutacion(h=5)."""
    return {"tabla": tendencies.estudio_evento(df, ev, HORIZONTES),
            "rango": tendencies.prob_rango(df, ev, h=3),
            "perm": tendencies.test_permutacion(df, ev, h=5, n_sim=n_sim)}


def semaforo(tabla: pd.DataFrame, perm: dict) -> dict[str, tuple[bool, str]]:
    """Puerta del tramo tendencia: n ≥ 100, exceso > 0 en ≥ 2 horizontes, |t| ≥ 2, p ≤ 0.05."""
    n = int(tabla["n"].max()) if len(tabla) else 0
    n_pos = int((tabla["exceso"] > 0).sum())
    t_pos = tabla.loc[tabla["exceso"] > 0, "t_stat"]
    t_max = float(t_pos.max()) if t_pos.notna().any() else 0.0
    p = perm.get("p_valor", np.nan)
    return {
        "n ≥ 100": (n >= 100, f"n = {n}"),
        "exceso > 0 en ≥ 2 horizontes": (n_pos >= 2, f"{n_pos} de {len(tabla)}"),
        "t ≥ 2 (con exceso > 0)": (t_max >= 2, f"max t = {t_max:.2f}"),
        "p ≤ 0.05 (permutación, h=5)": (bool(p <= 0.05) if pd.notna(p) else False,
                                        "p = n/d" if pd.isna(p) else f"p = {p:.3f}"),
    }


def equity_desde_trades(trades: pd.DataFrame) -> pd.DataFrame:
    """Equity = cumprod(1 + pnl_pct) ordenada por salida, con drawdown."""
    t = trades.copy()
    if "salida" in t.columns:
        t["salida"] = pd.to_datetime(t["salida"])
        t = t.sort_values("salida").set_index("salida")
    eq = (1 + t["pnl_pct"].astype(float)).cumprod()
    return pd.DataFrame({"equity": eq, "drawdown": eq / eq.cummax() - 1})


def formatear(df: pd.DataFrame, fmt: dict[str, str]) -> pd.DataFrame:
    """Aplica formatos de texto por columna (sin jinja2 / .style)."""
    out = df.copy()
    for col, f in fmt.items():
        if col in out.columns:
            out[col] = out[col].map(lambda x: "n/d" if pd.isna(x) else f.format(x))
    return out


def listar_reportes(raiz: Path = RAIZ) -> list[Path]:
    d = raiz / "reportes"
    return sorted(p for p in d.glob("ndx_*") if p.is_dir()) if d.exists() else []


# ----------------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------------
import streamlit as st  # noqa: E402


@st.cache_data(show_spinner=False)
def cargar(ruta: str) -> pd.DataFrame:
    return data.cargar(ruta)


c_resumen = st.cache_data(show_spinner=False)(calcular_resumen)
c_regimen = st.cache_data(show_spinner=False)(calcular_regimen)
c_eventos = st.cache_data(show_spinner=False)(eventos)
c_estudiar = st.cache_data(show_spinner="Permutaciones...")(estudiar)


def main() -> None:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    st.set_page_config(page_title="AED NDX", layout="wide")

    def pct(x, d=1):
        return "n/d" if pd.isna(x) else f"{x * 100:.{d}f} %"

    def fig_base(fig, titulo="", alto=380, ylog=False):
        fig.update_layout(title=titulo, height=alto, margin=dict(l=40, r=20, t=40, b=30),
                          hovermode="x unified", template="plotly_white",
                          legend=dict(orientation="h", y=1.02, x=0), font=dict(size=12))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#eeeeee", type="log" if ylog else "linear")
        return fig

    # -- sidebar --------------------------------------------------------------
    st.sidebar.header("AED NASDAQ-100")
    incluir_oos = st.sidebar.checkbox("Incluir OOS (2016+)", value=False)
    if incluir_oos:
        st.sidebar.error("Estás mirando el OOS. Cualquier regla que salga de aquí ya no se puede "
                         "validar limpiamente sobre 2016+: el OOS se mira una vez.")
    else:
        st.sidebar.caption(f"Mostrando solo IS (< {CORTE_OOS}).")
    st.sidebar.divider()
    n_er_side = st.sidebar.slider("Periodo ER (Kaufman)", 5, 30, 10, 1)
    n_adx_side = st.sidebar.slider("Periodo ADX", 7, 30, 14, 1)

    series: dict[str, pd.DataFrame] = {}
    for nombre, ruta in FICHEROS.items():
        if ruta.exists():
            series[nombre] = filtrar_periodo(cargar(str(ruta)), incluir_oos)
    if not series:
        st.error("No hay datos en `data/`. Se esperan ndx_norgate_d1.parquet y ndx_darwinex_d1.parquet.")
        return

    tab_datos, tab_reg, tab_tend, tab_res = st.tabs(["Datos", "Régimen", "Tendencias", "Resultados"])

    # -- 1. Datos -------------------------------------------------------------
    with tab_datos:
        opciones = list(series) + (["Ambas"] if len(series) == 2 else [])
        sel = st.selectbox("Serie", opciones, key="serie_datos")
        elegidas = list(series) if sel == "Ambas" else [sel]

        fig = go.Figure()
        for i, nom in enumerate(elegidas):
            fig.add_scatter(x=series[nom].index, y=series[nom]["close"], name=nom, mode="lines",
                            line=dict(width=1.5, color=[C1, C2][i]))
        st.plotly_chart(fig_base(fig, "Cierre (escala log)", ylog=True), width="stretch")

        filas = {nom: c_resumen(series[nom]) for nom in elegidas}
        tabla = pd.DataFrame({
            nom: {"Barras": f"{r['barras']:,}", "Desde": str(r["desde"]), "Hasta": str(r["hasta"]),
                  "CAGR": pct(r["cagr"]), "Vol. anualizada": pct(r["vol_anual"]), "MaxDD": pct(r["max_dd"]),
                  "% días positivos": pct(r["pct_dias_pos"]), "Curtosis": f"{r['curtosis']:.2f}",
                  "Asimetría": f"{r['asimetria']:.2f}"}
            for nom, r in filas.items()})
        st.dataframe(tabla, width="stretch")

        col_a, col_b = st.columns(2)
        with col_a:
            fig = go.Figure()
            for i, nom in enumerate(elegidas):
                r = series[nom]["close"].pct_change().dropna()
                fig.add_histogram(x=r, name=nom, nbinsx=120, opacity=0.65, marker_color=[C1, C2][i])
            fig.update_layout(barmode="overlay")
            fig.update_xaxes(tickformat=".1%")
            st.plotly_chart(fig_base(fig, "Distribución de retornos diarios", alto=320), width="stretch")
        with col_b:
            fig = go.Figure()
            for i, nom in enumerate(elegidas):
                v = vol_rodante(series[nom])
                fig.add_scatter(x=v.index, y=v["vol_20"], name=f"{nom} · 20d", line=dict(width=1, color=[C1, C2][i]))
                fig.add_scatter(x=v.index, y=v["vol_60"], name=f"{nom} · 60d",
                                line=dict(width=1.5, color=[C1, C2][i], dash="dot"))
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig_base(fig, "Volatilidad rodante anualizada (20 / 60 días)", alto=320), width="stretch")

        fig = go.Figure()
        for i, nom in enumerate(elegidas):
            ra = retornos_por_anio(series[nom])
            fig.add_bar(x=ra.index, y=ra.values, name=nom, marker_color=[C1, C2][i])
        fig.update_yaxes(tickformat=".0%")
        fig.update_layout(barmode="group")
        st.plotly_chart(fig_base(fig, "Retorno por año", alto=320), width="stretch")

        if sel == "Ambas":
            a, b = (series[n] for n in elegidas)
            cmp = comparar_series(a, b)
            c1, c2 = st.columns([1, 3])
            c1.metric("Barras en solape", f"{cmp['n_solape']:,}")
            c1.metric("Correlación de retornos", f"{cmp['correlacion']:.4f}" if pd.notna(cmp["correlacion"]) else "n/d")
            if len(cmp["ratio"]):
                fig = go.Figure(go.Scatter(x=cmp["ratio"].index, y=cmp["ratio"].values, mode="lines",
                                           line=dict(width=1.2, color=C3), name="ratio"))
                c2.plotly_chart(fig_base(fig, f"Ratio de cierres {elegidas[0].split(' ')[0]} / {elegidas[1].split(' ')[0]}",
                                         alto=300), width="stretch")
            st.caption("Un ratio estable indica que el CFD replica el índice; las derivas persistentes son "
                       "coste de financiación o dividendos, y afectan a las señales de mantenimiento largo.")

    # -- 2. Régimen -----------------------------------------------------------
    with tab_reg:
        nom = st.selectbox("Serie", list(series), key="serie_reg")
        df = series[nom]
        reg = c_regimen(df, n_adx_side, n_er_side)
        er_min = st.slider("Umbral ER de 'tendencia limpia'", 0.1, 0.6, 0.3, 0.05)
        por_anio = regimen_por_anio(reg, er_min)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06,
                            subplot_titles=(f"ADX({n_adx_side})", f"Efficiency Ratio({n_er_side})"))
        fig.add_scatter(x=reg.index, y=reg["adx"], name="ADX", line=dict(width=1, color=C1), row=1, col=1)
        fig.add_hline(y=30, line=dict(color=CGRIS, dash="dot", width=1), row=1, col=1)
        fig.add_hline(y=25, line=dict(color=CGRIS, dash="dot", width=1), row=1, col=1)
        fig.add_scatter(x=reg.index, y=reg["er"], name="ER", line=dict(width=1, color=C2), row=2, col=1)
        fig.add_hline(y=er_min, line=dict(color=CGRIS, dash="dot", width=1), row=2, col=1)
        st.plotly_chart(fig_base(fig, "", alto=520), width="stretch")

        st.caption(f"Global: ADX > 30 el {pct((reg['adx'] > 30).mean())} de las barras; ADX > 25 el "
                   f"{pct((reg['adx'] > 25).mean())}; ER > {er_min:.2f} el {pct((reg['er'] > er_min).mean())}. "
                   f"ER medio {reg['er'].mean():.3f}.")

        col_a, col_b = st.columns(2)
        with col_a:
            fig = go.Figure()
            fig.add_bar(x=por_anio.index, y=por_anio["pct_adx_25"], name="ADX > 25", marker_color=C3)
            fig.add_bar(x=por_anio.index, y=por_anio["pct_adx_30"], name="ADX > 30", marker_color=C1)
            fig.update_yaxes(tickformat=".0%")
            fig.update_layout(barmode="group")
            st.plotly_chart(fig_base(fig, "% de barras en tendencia (ADX) por año", alto=320), width="stretch")
        with col_b:
            fig = go.Figure(go.Bar(x=por_anio.index, y=por_anio["dias_er_limpio"], marker_color=C2,
                                   name=f"días ER > {er_min:.2f}"))
            st.plotly_chart(fig_base(fig, "Días de tendencia limpia (ER) por año", alto=320), width="stretch")

        col_a, col_b = st.columns(2)
        with col_a:
            fig = go.Figure(go.Histogram(x=reg["er"].dropna(), nbinsx=50, marker_color=C2, name="ER"))
            fig.add_vline(x=er_min, line=dict(color=CGRIS, dash="dot", width=1))
            st.plotly_chart(fig_base(fig, "Distribución del ER", alto=300), width="stretch")
        with col_b:
            dec = por_anio.copy()
            dec["década"] = (dec.index // 10) * 10
            por_dec = dec.groupby("década").agg(pct_adx_30=("pct_adx_30", "mean"), pct_adx_25=("pct_adx_25", "mean"),
                                                 er_medio=("er_medio", "mean"), dias_er_limpio=("dias_er_limpio", "mean"))
            st.markdown("**Por década (media anual)**")
            st.dataframe(formatear(por_dec, {"pct_adx_30": "{:.1%}", "pct_adx_25": "{:.1%}",
                                             "er_medio": "{:.3f}", "dias_er_limpio": "{:.0f}"}), width="stretch")
        st.caption("Kaufman: el ER dice cuánto del recorrido es desplazamiento neto y cuánto ruido. Si las décadas "
                   "recientes tienen menos días limpios, un seguidor de tendencia con parámetros de los 90 va a sufrir.")

    # -- 3. Tendencias --------------------------------------------------------
    with tab_tend:
        c_sel, c_ev = st.columns([1, 1])
        nom = c_sel.selectbox("Serie", list(series), key="serie_tend")
        nombre_ev = c_ev.selectbox("Evento", list(EVENTOS))
        spec = EVENTOS[nombre_ev]
        st.caption(spec["desc"])
        cols = st.columns(len(spec["params"]))
        params = {}
        for col, (k, (label, lo, hi, val, paso)) in zip(cols, spec["params"].items()):
            params[k] = col.slider(label, lo, hi, val, paso, key=f"p_{nombre_ev}_{k}")
        df = series[nom]
        lados = c_eventos(df, nombre_ev, **params)

        for lado, (ev, df_ev) in lados.items():
            st.subheader(f"Lado {lado}  ·  {int(ev.sum())} eventos")
            if lado == "corto":
                st.caption("El corto se evalúa sobre la serie invertida (1/precio): un exceso positivo es favorable al corto.")
            if int(ev.sum()) == 0:
                st.info("Sin eventos con estos parámetros.")
                continue
            res = c_estudiar(df_ev, ev, 500)
            tabla, rango, perm = res["tabla"], res["rango"], res["perm"]

            col_t, col_g = st.columns([3, 2])
            with col_t:
                st.dataframe(formatear(tabla, {"n": "{:.0f}", "media": "{:.3%}", "mediana": "{:.3%}",
                                               "pct_pos": "{:.1%}", "media_base": "{:.3%}",
                                               "pct_pos_base": "{:.1%}", "exceso": "{:.3%}", "t_stat": "{:.2f}"}),
                             width="stretch")
            with col_g:
                fig = go.Figure(go.Bar(x=[str(h) for h in tabla.index], y=tabla["exceso"],
                                       marker_color=[C1 if e > 0 else C_KO for e in tabla["exceso"]], name="exceso"))
                fig.update_yaxes(tickformat=".2%")
                fig.update_xaxes(title="horizonte (barras)")
                st.plotly_chart(fig_base(fig, "Exceso de retorno vs. base", alto=280), width="stretch")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("P(supera alto, 3 barras)", pct(rango["p_supera_alto"]),
                      delta=f"base {pct(rango['p_supera_alto_base'])}", delta_color="off")
            m2.metric("P(rompe bajo, 3 barras)", pct(rango["p_rompe_bajo"]),
                      delta=f"base {pct(rango['p_rompe_bajo_base'])}", delta_color="off")
            m3.metric("Media tras evento (h=5)", pct(perm["media"], 2),
                      delta=f"azar {pct(perm.get('media_azar', np.nan), 2)}", delta_color="off")
            m4.metric("p-valor (500 permutaciones)", f"{perm['p_valor']:.3f}" if pd.notna(perm["p_valor"]) else "n/d")

            sem = semaforo(tabla, perm)
            pasa = all(ok for ok, _ in sem.values())
            cols = st.columns(len(sem))
            for col, (crit, (ok, det)) in zip(cols, sem.items()):
                col.markdown(f"<div style='border-left:4px solid {C_OK if ok else C_KO};padding:4px 8px'>"
                             f"<b>{'PASA' if ok else 'NO'}</b> · {crit}<br><span style='color:{CGRIS}'>{det}</span></div>",
                             unsafe_allow_html=True)
            (st.success if pasa else st.warning)(
                "Cruza la puerta del tramo Tendencia: pasa a prototipo." if pasa
                else "No cruza la puerta. Registrar el test en hipotesis/REGISTRO.md con el motivo.")

    # -- 4. Resultados --------------------------------------------------------
    with tab_res:
        carpetas = listar_reportes()
        if not carpetas:
            st.info("Aún no hay validaciones (se esperan carpetas `reportes/ndx_*/`).")
        else:
            carpeta = st.selectbox("Validación", carpetas, format_func=lambda p: p.name)
            resumen = carpeta / "RESUMEN.md"
            if resumen.exists():
                st.markdown(resumen.read_text(encoding="utf-8"))
            else:
                st.warning("Sin RESUMEN.md en esta carpeta.")

            col_a, col_b = st.columns(2)
            meseta = carpeta / "meseta.csv"
            if meseta.exists():
                m = pd.read_csv(meseta, index_col=0)
                fig = go.Figure(go.Heatmap(z=m.values, x=[str(c) for c in m.columns], y=[str(i) for i in m.index],
                                           colorscale="Blues", colorbar=dict(title="PF"),
                                           text=np.round(m.values, 2), texttemplate="%{text}"))
                fig.update_xaxes(title="parámetro 2")
                fig.update_yaxes(title=m.index.name or "parámetro 1")
                col_a.plotly_chart(fig_base(fig, "Meseta de parámetros (IS)", alto=380), width="stretch")
            else:
                col_a.caption("Sin meseta.csv.")

            wf = carpeta / "walk_forward.csv"
            if wf.exists():
                w = pd.read_csv(wf)
                fmt = {c: "{:.3f}" for c in w.columns if c.startswith(("cagr", "pf"))}
                col_b.markdown("**Walk-forward**")
                col_b.dataframe(formatear(w, fmt), width="stretch", hide_index=True)
            else:
                col_b.caption("Sin walk_forward.csv.")

            tr = carpeta / "trades_oos.csv"
            if tr.exists():
                t = pd.read_csv(tr)
                if len(t) and "pnl_pct" in t.columns:
                    eq = equity_desde_trades(t)
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)
                    fig.add_scatter(x=eq.index, y=eq["equity"], name="equity", line=dict(width=1.5, color=C1), row=1, col=1)
                    fig.add_scatter(x=eq.index, y=eq["drawdown"], name="drawdown", fill="tozeroy",
                                    line=dict(width=1, color=C_KO), row=2, col=1)
                    fig.update_yaxes(tickformat=".0%", row=2, col=1)
                    st.plotly_chart(fig_base(fig, f"Equity OOS ({len(t)} trades, cumprod de 1+pnl_pct) y drawdown", alto=450),
                                    width="stretch")
                    st.caption(f"Retorno OOS acumulado {pct(eq['equity'].iloc[-1] - 1)} · "
                               f"MaxDD {pct(eq['drawdown'].min())}")
                else:
                    st.caption("trades_oos.csv vacío o sin columna pnl_pct.")
            else:
                st.caption("Sin trades_oos.csv.")


if __name__ == "__main__":
    main()
