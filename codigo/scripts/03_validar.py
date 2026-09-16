"""Etapa 55-75: validación completa (5 fases) y RESUMEN.md.

Uso:  python codigo/scripts/03_validar.py <senal> [ruta_datos] [--rapido]
Escribe reportes/<senal>/RESUMEN.md (+ meseta.csv, walk_forward.csv, trades_oos.csv).
"""
import itertools
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # consola Windows

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))

from quantlab import backtest, data, report, senales, validation

RAIZ = Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
rapido = "--rapido" in sys.argv
nombre = args[0] if args else "kama_tendencia"
df = data.cargar(args[1]) if len(args) > 1 else data.sintetico(n=4000, autocorr=0.15)
fn = senales.CATALOGO[nombre]

# Parámetros base, grid de walk-forward y ejes de la meseta, por señal.
# Regla: grid pequeño (Kaufman): pocos parámetros, rangos amplios, pasos gruesos.
PLANES = {
    "kama_tendencia": dict(
        params={"n": 10, "er_min": 0.3},
        grid=[{"n": n, "er_min": e} for n, e in itertools.product([8, 10, 14, 20], [0.2, 0.3, 0.4])],
        meseta=(("n", [6, 8, 10, 14, 20]), ("er_min", [0.1, 0.2, 0.3, 0.4, 0.5])),
    ),
    "holy_grail": dict(
        params={"adx_min": 30, "hold": 5},
        grid=[{"adx_min": a, "hold": h} for a, h in itertools.product([25, 30, 35], [3, 5, 8])],
        meseta=(("adx_min", [20, 25, 30, 35, 40]), ("hold", [2, 3, 5, 8, 12])),
    ),
    "ruptura_donchian": dict(
        params={"n_entrada": 50, "n_salida": 20},
        grid=[{"n_entrada": a, "n_salida": b} for a, b in itertools.product([30, 50, 80], [10, 20, 40])],
        meseta=(("n_entrada", [20, 30, 50, 80, 120]), ("n_salida", [5, 10, 20, 40, 60])),
    ),
}
plan = PLANES[nombre]
cfg = backtest.Config(coste_pct=0.0005, riesgo_pct=0.01, stop_atr=2.0)

r = validation.validar(df, fn, plan["params"], plan["grid"], plan["meseta"], cfg=cfg,
                       n_sim=500 if rapido else 5000)
ruta = report.guardar(nombre, r, RAIZ / "reportes")
print(ruta.read_text(encoding="utf-8"))
print(f"-> {ruta}")
