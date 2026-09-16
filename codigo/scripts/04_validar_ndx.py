"""Validación NDX con dos series: IS = Norgate < 2016 · OOS = 2016+ en Norgate Y en Darwinex.

Uso:  python scripts/04_validar_ndx.py <senal> [--rapido]
La señal y su plan (params, grid, meseta, config) se buscan en los módulos
quantlab.senales_kaufman y quantlab.senales_raschke (dict PLANES).
Escribe reportes/ndx_<senal>/RESUMEN.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))

from quantlab import backtest, data, report, validation
from quantlab import senales_kaufman, senales_raschke

RAIZ = Path(__file__).resolve().parents[2]
CORTE = "2016-01-01"
COSTE_LADO = 0.0002  # 2 pb por lado: ~1.5 pt de spread/2 + slippage sobre NDX ~8.000

PLANES = {**senales_kaufman.PLANES, **senales_raschke.PLANES}

args = [a for a in sys.argv[1:] if not a.startswith("--")]
rapido = "--rapido" in sys.argv
nombre = args[0]
plan = PLANES[nombre]

norgate = data.cargar(RAIZ / "data" / "ndx_norgate_d1.parquet")
darwinex = data.cargar(RAIZ / "data" / "ndx_darwinex_d1.parquet")

cfg = backtest.Config(coste_pct=COSTE_LADO, riesgo_pct=0.01, **plan.get("config", {}))
r = validation.validar(norgate, plan["fn"], plan["params"], plan["grid"], plan["meseta"], cfg=cfg,
                       corte=CORTE, oos_extra={"darwinex": darwinex}, n_sim=1000 if rapido else 5000)
ruta = report.guardar(f"ndx_{nombre}", r, RAIZ / "reportes")
print(ruta.read_text(encoding="utf-8"))
print(f"-> {ruta}")
