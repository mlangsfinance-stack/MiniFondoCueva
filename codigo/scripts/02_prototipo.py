"""Etapa 40-55: prototipo. La regla más simple que captura la tendencia,
con stop y costes, en TODA la muestra (todavía no se separa IS/OOS: aquí
solo se comprueba que la mecánica funciona y que el edge sobrevive a costes).

Uso:  python scripts/02_prototipo.py <senal> [ruta_datos]
      senal en: kama_tendencia | holy_grail | ruptura_donchian
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))

from quantlab import backtest, data, metrics, senales

nombre = sys.argv[1] if len(sys.argv) > 1 else "kama_tendencia"
df = data.cargar(sys.argv[2]) if len(sys.argv) > 2 else data.sintetico(autocorr=0.15)
fn = senales.CATALOGO[nombre]

cfg = backtest.Config(coste_pct=0.0005, riesgo_pct=0.01, stop_atr=2.0)
res = backtest.backtest(df, fn(df), cfg)
m = metrics.metricas(res)

print(f"Señal: {nombre}   barras: {len(df)}   config: {cfg}\n")
for k, v in m.items():
    print(f"  {k:16s} {v:>10.4f}" if isinstance(v, float) else f"  {k:16s} {v:>10}")
print("\nMotivos de salida:", res.trades["motivo"].value_counts().to_dict())
print("PnL por año:", metrics.pnl_por_anio(res.trades).round(0).to_dict())
print("\nCriterio de paso a validación: PF > 1.2 con costes, >= 100 trades, expectancia_R > 0.1, t_stat > 2.")
