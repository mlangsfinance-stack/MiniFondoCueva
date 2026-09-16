"""
Exploratorio 002 · nasdaq_sma_cross
-----------------------------------
AED (paso 02 TIS). Mide el fenómeno crudo: ¿los retornos diarios del NDX con SMA rápida > SMA lenta
son mejores que la base incondicional y que los días con SMA rápida < SMA lenta?

Sin reglas de trading, sin stops, sin curvas de equity. Solo IS (< 2021-01-01).

Uso:  .venv/Scripts/python codigo/exploratorio_005.py
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "NDX_D1.csv"
CORTE = pd.Timestamp("2021-01-01")

FAST = [10, 20, 30, 50, 75, 100]
SLOW = [100, 150, 200, 250, 300]
PAR_REF = (50, 200)           # par de referencia para tablas detalladas
COSTE_LADO = 1.5 + 1.0        # spread 1.5 + slippage 1 (puntos), por lado
RNG = np.random.default_rng(42)

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", lambda x: f"{x:,.4f}")


# --------------------------------------------------------------------------- datos
def cargar() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["fecha"]).sort_values("fecha").set_index("fecha")
    df = df[~df.index.duplicated(keep="last")]
    assert (df["close"] > 0).all()
    return df


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula SMAs sobre TODO el histórico (solo mira hacia atrás) y luego corta a IS."""
    out = df.copy()
    out["ret"] = np.log(out["close"]).diff()                 # retorno cierre-a-cierre del día t
    for n in sorted(set(FAST + SLOW)):
        out[f"sma{n}"] = out["close"].rolling(n).mean()
    return out


def senal(df: pd.DataFrame, f: int, s: int) -> pd.Series:
    """+1 si SMA_f > SMA_s al cierre de t-1 (la señal que se conoce antes de vivir el retorno de t)."""
    sg = (df[f"sma{f}"] > df[f"sma{s}"]).astype(float)
    sg[df[f"sma{f}"].isna() | df[f"sma{s}"].isna()] = np.nan   # calentamiento: sin señal, no "abajo"
    return sg.shift(1)


def tstat(x: pd.Series) -> float:
    x = x.dropna()
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 and x.std() > 0 else np.nan


def resumen(r: pd.Series) -> dict:
    r = r.dropna()
    return dict(
        n=len(r),
        media_bp=r.mean() * 1e4,
        std_bp=r.std() * 1e4,
        t=tstat(r),
        anual=r.mean() * 252,
        sharpe=r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan,
        pos=(r > 0).mean(),
        p05_bp=r.quantile(0.05) * 1e4,
        peor_bp=r.min() * 1e4,
    )


# --------------------------------------------------------------------------- bloques
def bloque_base(is_: pd.DataFrame) -> None:
    print("=" * 100)
    print("1. BASE INCONDICIONAL (IS)")
    print("=" * 100)
    print(f"Rango IS: {is_.index[0].date()} -> {is_.index[-1].date()}  |  velas: {len(is_)}")
    print(pd.DataFrame([resumen(is_["ret"])], index=["base"]).T)
    print("\nPor año:")
    por_anio = is_.groupby(is_.index.year)["ret"].agg(
        n="count", media_bp=lambda x: x.mean() * 1e4, anual=lambda x: x.sum()
    )
    print(por_anio)


def bloque_rejilla(is_: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 100)
    print("2. REJILLA rápida x lenta — retorno medio diario (bp) arriba / abajo / spread y t del spread")
    print("=" * 100)
    filas = []
    base = is_["ret"].mean()
    for f, s in product(FAST, SLOW):
        if f >= s:
            continue
        sg = senal(is_, f, s)
        r_up = is_.loc[sg == 1, "ret"]
        r_dn = is_.loc[sg == 0, "ret"]
        # t del spread (dos muestras, Welch)
        se = np.sqrt(r_up.var(ddof=1) / len(r_up) + r_dn.var(ddof=1) / len(r_dn))
        cruces = int((sg.diff().abs() == 1).sum())
        filas.append(dict(
            fast=f, slow=s,
            pct_arriba=sg.mean(),
            up_bp=r_up.mean() * 1e4, dn_bp=r_dn.mean() * 1e4, base_bp=base * 1e4,
            spread_bp=(r_up.mean() - r_dn.mean()) * 1e4,
            t_spread=(r_up.mean() - r_dn.mean()) / se,
            up_std_bp=r_up.std() * 1e4, dn_std_bp=r_dn.std() * 1e4,
            sharpe_up=r_up.mean() / r_up.std() * np.sqrt(252),
            sharpe_base=base / is_["ret"].std() * np.sqrt(252),
            cruces=cruces, cruces_anio=cruces / (len(is_) / 252),
        ))
    g = pd.DataFrame(filas)
    print(g.to_string(index=False))
    print("\nResumen rejilla:")
    print(f"  spread > 0 en {(g.spread_bp > 0).mean():.0%} de pares | mediana spread = {g.spread_bp.median():.2f} bp"
          f" | mediana t = {g.t_spread.median():.2f} | min t = {g.t_spread.min():.2f}")
    print(f"  up_bp > base en {(g.up_bp > g.base_bp).mean():.0%} de pares | dn_bp < 0 en {(g.dn_bp < 0).mean():.0%}")
    print(f"  sharpe_up > sharpe_base en {(g.sharpe_up > g.sharpe_base).mean():.0%} de pares")
    return g


def bloque_deriva(is_: pd.DataFrame, g: pd.DataFrame) -> None:
    """¿Es solo la deriva alcista? Comparar 'largo solo cuando arriba' vs 'largo siempre' en términos crudos."""
    print("\n" + "=" * 100)
    print("3. ¿SOLO DERIVA ALCISTA? — filtro vs largo siempre (sin costes, log-ret acumulado y volatilidad)")
    print("   (mismo periodo para ambos: desde que la SMA lenta existe; el calentamiento no cuenta)")
    print("=" * 100)
    filas = []
    for _, row in g.iterrows():
        f, s = int(row.fast), int(row.slow)
        sg = senal(is_, f, s)
        m = sg.notna()
        base = is_.loc[m, "ret"]
        filt = base * sg[m]
        filas.append(dict(
            fast=f, slow=s,
            acum_filtro=filt.sum(), acum_largo=base.sum(),
            vol_filtro=filt.std() * np.sqrt(252), vol_largo=base.std() * np.sqrt(252),
            sharpe_filtro=filt.mean() / filt.std() * np.sqrt(252),
            sharpe_largo=base.mean() / base.std() * np.sqrt(252),
            captura_alcista=filt[base > 0].sum() / base[base > 0].sum(),
            captura_bajista=filt[base < 0].sum() / base[base < 0].sum(),
        ))
    d = pd.DataFrame(filas)
    print(d.to_string(index=False))
    print("\n  acum_filtro > acum_largo en", f"{(d.acum_filtro > d.acum_largo).mean():.0%} de pares;",
          "sharpe_filtro > sharpe_largo en", f"{(d.sharpe_filtro > d.sharpe_largo).mean():.0%}")
    print("  captura_bajista = fracción de la suma de días negativos que el filtro se come (menor = mejor);",
          "captura_alcista = idem días positivos (mayor = mejor)")


def bloque_anios(is_: pd.DataFrame, f: int, s: int) -> pd.DataFrame:
    print("\n" + "=" * 100)
    print(f"4. ESTABILIDAD POR AÑO — par de referencia {f}/{s}: media diaria (bp) arriba / abajo / base")
    print("=" * 100)
    sg = senal(is_, f, s)
    tmp = is_.assign(sg=sg, anio=is_.index.year).dropna(subset=["sg"])
    filas = []
    for a, gg in tmp.groupby("anio"):
        up, dn = gg.loc[gg.sg == 1, "ret"], gg.loc[gg.sg == 0, "ret"]
        filas.append(dict(
            anio=a, n=len(gg), pct_arriba=gg.sg.mean(),
            up_bp=up.mean() * 1e4 if len(up) else np.nan, n_up=len(up),
            dn_bp=dn.mean() * 1e4 if len(dn) else np.nan, n_dn=len(dn),
            base_bp=gg.ret.mean() * 1e4,
            spread_bp=(up.mean() - dn.mean()) * 1e4 if len(up) and len(dn) else np.nan,
            filtro_acum=(gg.ret * gg.sg).sum(), largo_acum=gg.ret.sum(),
        ))
    y = pd.DataFrame(filas).set_index("anio")
    print(y)
    v = y.spread_bp.dropna()
    print(f"\n  spread > 0 en {(v > 0).sum()}/{len(v)} años con ambos regímenes | "
          f"up > base en {(y.up_bp > y.base_bp).sum()}/{len(y)} años | "
          f"filtro >= largo en {(y.filtro_acum >= y.largo_acum).sum()}/{len(y)} años")
    return y


def bloque_rejilla_por_anio(is_: pd.DataFrame, g: pd.DataFrame) -> None:
    """Para cada año, mediana del spread (arriba - abajo) a través de toda la rejilla."""
    print("\n" + "=" * 100)
    print("5. ESTABILIDAD POR AÑO EN TODA LA REJILLA — mediana y % de pares con spread > 0 cada año")
    print("=" * 100)
    anios = sorted(is_.index.year.unique())
    tabla = {}
    for _, row in g.iterrows():
        f, s = int(row.fast), int(row.slow)
        sg = senal(is_, f, s)
        tmp = is_.assign(sg=sg, anio=is_.index.year).dropna(subset=["sg"])
        col = {}
        for a in anios:
            gg = tmp[tmp.anio == a]
            up, dn = gg.loc[gg.sg == 1, "ret"], gg.loc[gg.sg == 0, "ret"]
            col[a] = (up.mean() - dn.mean()) * 1e4 if len(up) > 5 and len(dn) > 5 else np.nan
        tabla[(f, s)] = col
    t = pd.DataFrame(tabla)
    res = pd.DataFrame(dict(
        pares_validos=t.notna().sum(axis=1),
        mediana_spread_bp=t.median(axis=1),
        pct_pos=(t > 0).sum(axis=1) / t.notna().sum(axis=1),
    ))
    print(res)
    print("  (año sin pares válidos = no hubo ambos regímenes ese año con >5 días)")


def bloque_jackknife(is_: pd.DataFrame, f: int, s: int) -> None:
    print("\n" + "=" * 100)
    print(f"6. ¿QUÉ LO MATA? — jackknife por año y sin los mejores años ({f}/{s})")
    print("=" * 100)
    sg = senal(is_, f, s)
    tmp = is_.assign(sg=sg, anio=is_.index.year).dropna(subset=["sg"])

    def spread(d: pd.DataFrame) -> tuple[float, float]:
        up, dn = d.loc[d.sg == 1, "ret"], d.loc[d.sg == 0, "ret"]
        se = np.sqrt(up.var(ddof=1) / len(up) + dn.var(ddof=1) / len(dn))
        return (up.mean() - dn.mean()) * 1e4, (up.mean() - dn.mean()) / se

    full = spread(tmp)
    print(f"  completo: spread={full[0]:.2f} bp  t={full[1]:.2f}")
    filas = []
    for a in sorted(tmp.anio.unique()):
        sp, t = spread(tmp[tmp.anio != a])
        filas.append(dict(sin_anio=a, spread_bp=sp, t=t))
    jk = pd.DataFrame(filas).set_index("sin_anio")
    print(jk.T)

    # contribución de cada año al spread: años ordenados por (filtro - largo) acumulado
    contrib = tmp.groupby("anio").apply(lambda d: (d.ret * d.sg).sum() - d.ret.sum() * d.sg.mean()).sort_values()
    print("\n  Sin los 2 años que más aportan al spread:", list(contrib.index[-2:]))
    sp, t = spread(tmp[~tmp.anio.isin(contrib.index[-2:])])
    print(f"    spread={sp:.2f} bp  t={t:.2f}")
    print("  Sin 2008-2009 (crash + rebote):")
    sp, t = spread(tmp[~tmp.anio.isin([2008, 2009])])
    print(f"    spread={sp:.2f} bp  t={t:.2f}")
    print("  Sin 2020 (covid):")
    sp, t = spread(tmp[tmp.anio != 2020])
    print(f"    spread={sp:.2f} bp  t={t:.2f}")
    print("  Sin 2008, 2009 y 2020:")
    sp, t = spread(tmp[~tmp.anio.isin([2008, 2009, 2020])])
    print(f"    spread={sp:.2f} bp  t={t:.2f}")


def bloque_placebo(is_: pd.DataFrame, f: int, s: int, n_iter: int = 2000) -> None:
    """Placebo por desplazamiento circular: se rota la señal respecto a los retornos.
    Conserva la autocorrelación de la señal (bloques largos) y de los retornos. Si el spread real
    no está en la cola de la distribución placebo, la asociación es compatible con azar."""
    print("\n" + "=" * 100)
    print(f"7. PLACEBO — desplazamiento circular de la señal ({f}/{s}, {n_iter} rotaciones)")
    print("=" * 100)
    sg = senal(is_, f, s)
    m = sg.notna()
    r = is_.loc[m, "ret"].to_numpy()
    sgv = sg[m].to_numpy()
    def sh(x: np.ndarray) -> float:
        return x.mean() / x.std() * np.sqrt(252)

    real = r[sgv == 1].mean() - r[sgv == 0].mean()
    real_acum = (r * sgv).sum()
    real_sh = sh(r * sgv)
    n = len(r)
    sp, ac, shp = np.empty(n_iter), np.empty(n_iter), np.empty(n_iter)
    for i in range(n_iter):
        k = RNG.integers(20, n - 20)
        s_ = np.roll(sgv, k)
        sp[i] = r[s_ == 1].mean() - r[s_ == 0].mean()
        ac[i] = (r * s_).sum()
        shp[i] = sh(r * s_)
    print(f"  spread real = {real*1e4:.2f} bp | placebo: media={sp.mean()*1e4:.2f}, p95={np.quantile(sp,0.95)*1e4:.2f},"
          f" p99={np.quantile(sp,0.99)*1e4:.2f} bp | p-valor (una cola) = {(sp >= real).mean():.4f}")
    print(f"  acumulado filtro real = {real_acum:.3f} | placebo: media={ac.mean():.3f}, p95={np.quantile(ac,0.95):.3f}"
          f" | p-valor = {(ac >= real_acum).mean():.4f}")
    print(f"  sharpe filtro real = {real_sh:.3f} | placebo: media={shp.mean():.3f}, p95={np.quantile(shp,0.95):.3f}"
          f" | p-valor = {(shp >= real_sh).mean():.4f}")
    print(f"  (largo siempre en el mismo periodo: acumula {r.sum():.3f}, sharpe {sh(r):.3f}; "
          f"la señal está arriba el {sgv.mean():.0%} del tiempo)")
    idx = np.argsort(r)[:20]
    print(f"  de los 20 peores días del periodo, el filtro está DENTRO en {int(sgv[idx].sum())}")


def bloque_eventos(is_: pd.DataFrame, f: int, s: int) -> None:
    """Retornos forward tras el cruce (evento), comparados con la base incondicional."""
    print("\n" + "=" * 100)
    print(f"8. EVENTOS DE CRUCE — retorno forward acumulado (bp) tras cruce arriba / abajo vs base ({f}/{s})")
    print("=" * 100)
    sg = senal(is_, f, s)
    d = sg.diff()
    up_idx = np.where(d.to_numpy() == 1)[0]
    dn_idx = np.where(d.to_numpy() == -1)[0]
    r = is_["ret"].to_numpy()
    hor = [1, 5, 10, 20, 60, 120]
    filas = []
    for h in hor:
        fw = np.array([r[i:i + h].sum() for i in range(len(r) - h)])
        up = fw[[i for i in up_idx if i < len(fw)]]
        dn = fw[[i for i in dn_idx if i < len(fw)]]
        filas.append(dict(
            h=h, base_bp=fw.mean() * 1e4, base_pos=(fw > 0).mean(),
            n_up=len(up), up_bp=up.mean() * 1e4, up_pos=(up > 0).mean(), up_t=tstat(pd.Series(up)),
            n_dn=len(dn), dn_bp=dn.mean() * 1e4, dn_pos=(dn > 0).mean(),
        ))
    print(pd.DataFrame(filas).to_string(index=False))
    # duración de los tramos arriba
    tramos = (sg != sg.shift()).cumsum()
    dur = sg.groupby(tramos).agg(["first", "size"]).dropna()
    print("\n  Duración de tramos (días): arriba ->", dur[dur["first"] == 1]["size"].describe()[["count", "mean", "50%", "min", "max"]].round(0).to_dict())
    print("                             abajo  ->", dur[dur["first"] == 0]["size"].describe()[["count", "mean", "50%", "min", "max"]].round(0).to_dict())


def bloque_regimen(is_: pd.DataFrame, f: int, s: int) -> None:
    print("\n" + "=" * 100)
    print(f"9. POR RÉGIMEN DE VOLATILIDAD (terciles de vol 20d realizada, t-1) — {f}/{s}")
    print("=" * 100)
    vol = is_["ret"].rolling(20).std().shift(1)
    sg = senal(is_, f, s)
    tmp = is_.assign(sg=sg, vol=vol).dropna(subset=["sg", "vol"])
    tmp["ter"] = pd.qcut(tmp.vol, 3, labels=["baja", "media", "alta"])
    filas = []
    for ter, gg in tmp.groupby("ter", observed=True):
        up, dn = gg.loc[gg.sg == 1, "ret"], gg.loc[gg.sg == 0, "ret"]
        filas.append(dict(vol=ter, n=len(gg), pct_arriba=gg.sg.mean(), up_bp=up.mean() * 1e4, n_up=len(up),
                          dn_bp=dn.mean() * 1e4, n_dn=len(dn), base_bp=gg.ret.mean() * 1e4,
                          spread_bp=(up.mean() - dn.mean()) * 1e4))
    print(pd.DataFrame(filas).to_string(index=False))


def bloque_una_media(is_: pd.DataFrame) -> None:
    """¿Añade algo la media rápida? Compara con precio > SMA lenta (1 parámetro)."""
    print("\n" + "=" * 100)
    print("10. ¿APORTA LA MEDIA RÁPIDA? — precio(t-1) > SMA lenta vs cruce de medias")
    print("=" * 100)
    filas = []
    for s in SLOW:
        sg = (is_["close"] > is_[f"sma{s}"]).astype(float)
        sg[is_[f"sma{s}"].isna()] = np.nan
        sg = sg.shift(1)
        up, dn = is_.loc[sg == 1, "ret"], is_.loc[sg == 0, "ret"]
        se = np.sqrt(up.var(ddof=1) / len(up) + dn.var(ddof=1) / len(dn))
        cruces = int((sg.diff().abs() == 1).sum())
        filas.append(dict(regla=f"close>sma{s}", pct_arriba=sg.mean(), up_bp=up.mean() * 1e4, dn_bp=dn.mean() * 1e4,
                          spread_bp=(up.mean() - dn.mean()) * 1e4, t_spread=(up.mean() - dn.mean()) / se,
                          acum_filtro=(is_.ret * sg.fillna(0)).sum(), cruces=cruces))
    print(pd.DataFrame(filas).to_string(index=False))


def bloque_costes(is_: pd.DataFrame, g: pd.DataFrame) -> None:
    print("\n" + "=" * 100)
    print("11. TAMAÑO DEL EFECTO FRENTE A COSTES (spread 1.5 + slip 1 por lado = 5 puntos ida y vuelta)")
    print("=" * 100)
    px_med = is_["close"].median()
    anios = len(is_) / 252
    print(f"  precio mediano IS = {px_med:,.0f} -> coste ida+vuelta = {2*COSTE_LADO} pts = {2*COSTE_LADO/px_med*1e4:.1f} bp por operación")
    filas = []
    for _, row in g.iterrows():
        f, s = int(row.fast), int(row.slow)
        sg = senal(is_, f, s).fillna(0)
        filt_acum = (is_.ret * sg).sum()
        # coste en log-ret: cada cruce arriba -> entrada, cada cruce abajo -> salida; se usa el precio del día
        cambios = sg.diff().abs() == 1
        coste = (COSTE_LADO / is_.loc[cambios, "close"]).sum()
        filas.append(dict(fast=f, slow=s, cruces_anio=row.cruces / anios, acum_filtro=filt_acum, coste_total=coste,
                          coste_pct_del_acum=coste / filt_acum if filt_acum > 0 else np.nan,
                          exceso_vs_largo=filt_acum - is_.ret.sum(),
                          exceso_neto_vs_largo=filt_acum - coste - is_.ret.sum()))
    c = pd.DataFrame(filas)
    print(c.to_string(index=False))
    print(f"\n  coste medio = {c.coste_pct_del_acum.median():.1%} del acumulado del filtro (mediana rejilla)")
    print(f"  exceso neto vs largo siempre > 0 en {(c.exceso_neto_vs_largo > 0).mean():.0%} de pares")


# --------------------------------------------------------------------------- main
def main() -> int:
    df = preparar(cargar())
    is_ = df[df.index < CORTE].copy()
    print(f"Datos totales: {df.index[0].date()} -> {df.index[-1].date()} ({len(df)} velas). "
          f"IS < {CORTE.date()}: {len(is_)} velas. OOS NO se mira.")

    bloque_base(is_)
    g = bloque_rejilla(is_)
    bloque_deriva(is_, g)
    bloque_anios(is_, *PAR_REF)
    bloque_rejilla_por_anio(is_, g)
    bloque_jackknife(is_, *PAR_REF)
    bloque_placebo(is_, *PAR_REF)
    bloque_placebo(is_, 20, 100, n_iter=2000)
    bloque_eventos(is_, *PAR_REF)
    bloque_regimen(is_, *PAR_REF)
    bloque_una_media(is_)
    bloque_costes(is_, g)
    return 0


if __name__ == "__main__":
    sys.exit(main())
