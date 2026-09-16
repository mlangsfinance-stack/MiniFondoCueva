"""
Exploratorio 003 · nasdaq_overnight
-----------------------------------
Pregunta: ¿la deriva del NDX se concentra en el tramo overnight (close[t] -> open[t+1])
y no en el intradía (open[t] -> close[t])? ¿Supera los costes? ¿Es estable?

Solo IS: fechas < 2021-01-01. OOS no se toca aquí.
Sin reglas de trading, sin equity, sin PF. Solo el fenómeno crudo.
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CSV = RAIZ / "data" / "NDX_D1.csv"
CORTE = pd.Timestamp("2021-01-01")
COSTE_LADO_PTS = 1.5 + 1.0          # spread + slippage por lado, en puntos
COSTE_RT_PTS = 2 * COSTE_LADO_PTS   # ida y vuelta = 5 puntos

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", lambda x: f"{x:,.4f}")


def seccion(t):
    print("\n" + "=" * 90)
    print(t)
    print("=" * 90)


def resumen(s, nombre):
    s = s.dropna()
    n = len(s)
    m = s.mean()
    sd = s.std(ddof=1)
    t = m / (sd / np.sqrt(n)) if n > 1 else np.nan
    return pd.Series({
        "n": n, "media_%": m * 100, "mediana_%": s.median() * 100, "std_%": sd * 100,
        "t_stat": t, "pct_pos": (s > 0).mean() * 100,
        "suma_%": s.sum() * 100, "p05_%": s.quantile(0.05) * 100, "p95_%": s.quantile(0.95) * 100,
    }, name=nombre)


# ---------------------------------------------------------------- datos
df = pd.read_csv(CSV, parse_dates=["fecha"]).sort_values("fecha").reset_index(drop=True)
df = df[df["fecha"] < CORTE].copy()
print(f"Filas IS: {len(df)}  ({df['fecha'].min().date()} -> {df['fecha'].max().date()})")

# tramos (todo en retornos simples)
df["r_intra"] = df["close"] / df["open"] - 1                      # open[t] -> close[t]
df["r_over"] = df["open"].shift(-1) / df["close"] - 1             # close[t] -> open[t+1]
df["r_cc"] = df["close"].shift(-1) / df["close"] - 1              # close[t] -> close[t+1]
df["gap_pts"] = df["open"].shift(-1) - df["close"]                # el overnight en puntos
df["rango_pts"] = df["high"] - df["low"]
df["dias_hasta_sig"] = (df["fecha"].shift(-1) - df["fecha"]).dt.days
df["anio"] = df["fecha"].dt.year
df["dow"] = df["fecha"].dt.dayofweek  # 0=lun

# ---------------------------------------------------------------- 0. ¿qué es "open" y "close" en este CFD?
seccion("0. Naturaleza de la vela: ¿el gap overnight es un gap real o es una vela de ~24h?")
print("Tamaño del gap |open[t+1]-close[t]| vs rango intradía high-low (puntos):")
q = pd.DataFrame({
    "|gap| pts": df["gap_pts"].abs().describe(percentiles=[.5, .75, .9, .99]),
    "rango H-L pts": df["rango_pts"].describe(percentiles=[.5, .75, .9, .99]),
})
print(q)
ratio = (df["gap_pts"].abs() / df["rango_pts"]).median()
print(f"\nMediana |gap| / rango_HL = {ratio:.3f}")
print("Std overnight vs std intradía (%):", f"{df['r_over'].std()*100:.3f} vs {df['r_intra'].std()*100:.3f}")
print("Ratio var_over / var_cc:", f"{df['r_over'].var()/df['r_cc'].var():.3f}")
print("\nDistribución de días entre velas consecutivas (1 = día siguiente, 3 = fin de semana):")
print(df["dias_hasta_sig"].value_counts().sort_index().head(8))
print("\nLectura: si |gap| es una fracción pequeña del rango y var_over/var_cc es muy baja,")
print("el CFD cotiza casi 24h y 'open/close' de la vela D1 NO son la subasta de apertura/cierre del cash.")

# ---------------------------------------------------------------- 1. tramos, resumen global IS
seccion("1. Retorno por tramo — IS completo")
tab = pd.concat([resumen(df["r_over"], "overnight"), resumen(df["r_intra"], "intradia"), resumen(df["r_cc"], "close-close")], axis=1).T
print(tab)
# diferencia pareada overnight - intradía
d = (df["r_over"] - df["r_intra"]).dropna()
print(f"\nDiferencia pareada overnight - intradía: media {d.mean()*100:.4f}%  t={d.mean()/(d.std()/np.sqrt(len(d))):.2f}")

# ---------------------------------------------------------------- 2. costes
seccion("2. Efecto vs costes (el punto crítico)")
gap_med_pts = df["gap_pts"].mean()
print(f"Gap overnight medio: {gap_med_pts:.2f} pts   |  coste ida+vuelta: {COSTE_RT_PTS:.1f} pts")
print(f"Gap overnight mediano: {df['gap_pts'].median():.2f} pts")
neto = df["gap_pts"] - COSTE_RT_PTS
print(f"Gap medio neto de costes: {neto.mean():.2f} pts  (t={neto.mean()/(neto.std()/np.sqrt(neto.notna().sum())):.2f})")
print(f"% de noches cuyo gap > coste RT (5 pts): {(df['gap_pts'] > COSTE_RT_PTS).mean()*100:.1f}%")
print("\nCoste RT como % del precio, por año (los costes en puntos pesan más cuando el índice vale menos):")
cp = df.groupby("anio").apply(lambda g: pd.Series({
    "precio_medio": g["close"].mean(),
    "coste_RT_%": COSTE_RT_PTS / g["close"].mean() * 100,
    "over_medio_%": g["r_over"].mean() * 100,
    "over_neto_%": (g["r_over"] - COSTE_RT_PTS / g["close"]).mean() * 100,
    "gap_medio_pts": g["gap_pts"].mean(),
    "gap_neto_pts": (g["gap_pts"] - COSTE_RT_PTS).mean(),
}))
print(cp)
print(f"\nTOTAL IS: suma gap bruto {df['gap_pts'].sum():,.0f} pts | coste total {COSTE_RT_PTS*df['gap_pts'].notna().sum():,.0f} pts | neto {neto.sum():,.0f} pts")
print(f"TOTAL IS en %: over bruto {df['r_over'].sum()*100:.1f}% | over neto {(df['r_over'] - COSTE_RT_PTS/df['close']).sum()*100:.1f}% | intradía {df['r_intra'].sum()*100:.1f}%")

# ---------------------------------------------------------------- 3. estabilidad por año
seccion("3. Estabilidad por año (retorno medio diario %, suma anual %, % noches positivas)")
por_anio = df.groupby("anio").agg(
    n=("r_over", "count"),
    over_media=("r_over", lambda s: s.mean() * 100),
    intra_media=("r_intra", lambda s: s.mean() * 100),
    over_suma=("r_over", lambda s: s.sum() * 100),
    intra_suma=("r_intra", lambda s: s.sum() * 100),
    cc_suma=("r_cc", lambda s: s.sum() * 100),
    over_pos=("r_over", lambda s: (s > 0).mean() * 100),
    over_t=("r_over", lambda s: s.mean() / (s.std() / np.sqrt(s.count()))),
)
print(por_anio)
print(f"\nAños con overnight suma > 0: {(por_anio['over_suma']>0).sum()}/{len(por_anio)}")
print(f"Años con overnight > intradía: {(por_anio['over_suma']>por_anio['intra_suma']).sum()}/{len(por_anio)}")
print(f"Años con overnight NETO de costes > 0: {(cp['over_neto_%']>0).sum()}/{len(cp)}")

# ---------------------------------------------------------------- 4. quitar mejores años
seccion("4. Sin los 2 mejores años overnight (y sin los 2 mejores de intradía, para comparar)")
mejores = por_anio["over_suma"].nlargest(2).index.tolist()
sub = df[~df["anio"].isin(mejores)]
print(f"Mejores años overnight: {mejores}")
print(pd.concat([resumen(sub["r_over"], "overnight sin 2 mejores"), resumen(sub["r_intra"], "intradia mismo subset")], axis=1).T)
neto_sub = sub["gap_pts"] - COSTE_RT_PTS
print(f"Gap neto sin 2 mejores años: media {neto_sub.mean():.2f} pts, suma {neto_sub.sum():,.0f} pts")
print(f"Overnight neto % sin 2 mejores años: suma {(sub['r_over'] - COSTE_RT_PTS/sub['close']).sum()*100:.1f}%")

# quitar los 2 peores también (robustez simétrica)
peores = por_anio["over_suma"].nsmallest(2).index.tolist()
sub2 = df[~df["anio"].isin(mejores + peores)]
print(f"\nSin 2 mejores ({mejores}) NI 2 peores ({peores}): over media {sub2['r_over'].mean()*100:.4f}% suma {sub2['r_over'].sum()*100:.1f}% | intra suma {sub2['r_intra'].sum()*100:.1f}%")

# ---------------------------------------------------------------- 5. dependencia de pocas velas
seccion("5. ¿Depende de pocas noches? Recorte de colas")
ro = df["r_over"].dropna()
for k in [1, 5, 10, 20, 50]:
    sin_top = ro.drop(ro.nlargest(k).index)
    print(f"Sin las {k:>2} mejores noches: media {sin_top.mean()*100:.4f}%  suma {sin_top.sum()*100:.1f}%  t={sin_top.mean()/(sin_top.std()/np.sqrt(len(sin_top))):.2f}")
sin_ambas = ro.drop(ro.nlargest(20).index).drop(ro.nsmallest(20).index)
print(f"Sin 20 mejores NI 20 peores: media {sin_ambas.mean()*100:.4f}% suma {sin_ambas.sum()*100:.1f}%")
w = ro.clip(ro.quantile(0.01), ro.quantile(0.99))
print(f"Winsorizado 1%/99%: media {w.mean()*100:.4f}%  t={w.mean()/(w.std()/np.sqrt(len(w))):.2f}")
print(f"Aporte de las 20 mejores noches a la suma total: {ro.nlargest(20).sum()/ro.sum()*100:.1f}%")

# ---------------------------------------------------------------- 6. dia de la semana
seccion("6. Por día de la semana del cierre (0=lun ... 4=vie; vie = fin de semana en medio)")
dow = df.groupby("dow").agg(
    n=("r_over", "count"),
    over_media=("r_over", lambda s: s.mean() * 100),
    over_pos=("r_over", lambda s: (s > 0).mean() * 100),
    over_t=("r_over", lambda s: s.mean() / (s.std() / np.sqrt(s.count()))),
    gap_neto_pts=("gap_pts", lambda s: (s - COSTE_RT_PTS).mean()),
    intra_media=("r_intra", lambda s: s.mean() * 100),
)
dow.index = [["lun", "mar", "mie", "jue", "vie", "sab", "dom"][i] for i in dow.index]
print(dow)

# ---------------------------------------------------------------- 6b. anatomía del gap: ¿hay un sesgo mecánico?
seccion("6b. Anatomía del gap en puntos por año: ¿sesgo mecánico del rollover/ajuste?")
print("Si el gap está sesgado a negativo con mediana estable y % positivas muy bajo, huele a ajuste")
print("mecánico del CFD (financiación/dividendos aplicados en el precio al cambio de día), no a mercado.")
anat = df.groupby("anio")["gap_pts"].agg(
    n="count", media="mean", mediana="median",
    pct_pos=lambda s: (s > 0).mean() * 100,
    pct_cero=lambda s: (s == 0).mean() * 100,
    pct_neg=lambda s: (s < 0).mean() * 100,
    p25=lambda s: s.quantile(0.25), p75=lambda s: s.quantile(0.75),
    abs_mediana=lambda s: s.abs().median(),
)
print(anat)
print("\nValores de gap más frecuentes en 2016-2017 (redondeado a 0.1 pt):")
print(df[df["anio"].isin([2016, 2017])]["gap_pts"].round(1).value_counts().head(8))

# ---------------------------------------------------------------- 7. regimen
seccion("7. Régimen: tendencia (close vs SMA200) y volatilidad (std 20d de r_cc, terciles)")
df["sma200"] = df["close"].rolling(200).mean()
df["alcista"] = np.where(df["sma200"].isna(), np.nan, (df["close"] > df["sma200"]).astype(float))
df["vol20"] = df["r_cc"].rolling(20).std().shift(1)  # vol conocida al cierre de t (sin mirar t+1)
df["vol_ter"] = pd.qcut(df["vol20"], 3, labels=["baja", "media", "alta"])


def por_grupo(col):
    g = df.groupby(col, observed=True).agg(
        n=("r_over", "count"),
        over_media=("r_over", lambda s: s.mean() * 100),
        over_t=("r_over", lambda s: s.mean() / (s.std() / np.sqrt(s.count()))),
        over_suma=("r_over", lambda s: s.sum() * 100),
        intra_media=("r_intra", lambda s: s.mean() * 100),
        intra_suma=("r_intra", lambda s: s.sum() * 100),
        gap_neto_pts=("gap_pts", lambda s: (s - COSTE_RT_PTS).mean()),
    )
    return g


print("Por tendencia (1 = close > SMA200):")
print(por_grupo("alcista"))
print("\nPor tercil de volatilidad 20d:")
print(por_grupo("vol_ter"))

# ---------------------------------------------------------------- 8. persistencia / condicional al dia
seccion("8. Persistencia y condicionales simples")
print("Autocorrelación overnight lag1..5:", [f"{ro.autocorr(l):.3f}" for l in range(1, 6)])
print("Corr(overnight[t], intradía[t]):", f"{df['r_over'].corr(df['r_intra']):.3f}")
print("Corr(overnight[t], intradía[t+1]):", f"{df['r_over'].corr(df['r_intra'].shift(-1)):.3f}")
cond = df.assign(intra_signo=np.sign(df["r_intra"])).groupby("intra_signo").agg(
    n=("r_over", "count"), over_media=("r_over", lambda s: s.mean() * 100), over_t=("r_over", lambda s: s.mean() / (s.std() / np.sqrt(s.count())))
)
print("\nOvernight condicionado al signo del intradía del mismo día:")
print(cond)

# ---------------------------------------------------------------- 9. ventanas rodantes
seccion("9. Ventanas rodantes de 2 años (retorno overnight medio, t, neto pts) — mirar si hay tramos muertos")
df["r_over_neto"] = df["r_over"] - COSTE_RT_PTS / df["close"]
for ini in range(2008, 2020):
    w = df[(df["anio"] >= ini) & (df["anio"] <= ini + 1)]
    if len(w) < 200:
        continue
    s = w["r_over"].dropna()
    print(f"{ini}-{ini+1}: n={len(s):4d} over media {s.mean()*100:+.4f}% t={s.mean()/(s.std()/np.sqrt(len(s))):+.2f} | "
          f"neto suma {w['r_over_neto'].sum()*100:+.1f}% | intra suma {w['r_intra'].sum()*100:+.1f}%")

# ---------------------------------------------------------------- 10. mitades IS
seccion("10. Mitades del IS")
mitad = df["fecha"].iloc[len(df) // 2]
for nombre, m in [("1ª mitad", df[df["fecha"] < mitad]), ("2ª mitad", df[df["fecha"] >= mitad])]:
    s = m["r_over"].dropna()
    print(f"{nombre} ({m['fecha'].min().date()} -> {m['fecha'].max().date()}): over media {s.mean()*100:+.4f}% t={s.mean()/(s.std()/np.sqrt(len(s))):+.2f} "
          f"| neto suma {m['r_over_neto'].sum()*100:+.1f}% | intra suma {m['r_intra'].sum()*100:+.1f}% | cc suma {m['r_cc'].sum()*100:+.1f}%")

print("\nFin del exploratorio.")
