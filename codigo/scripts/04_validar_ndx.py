"""Validación NDX con dos series: IS = Norgate < 2016 · OOS = 2016+ en Norgate Y en Darwinex.

Uso:  python codigo/scripts/04_validar_ndx.py <senal> [--rapido]
La señal y su plan (params, grid, meseta, config) se buscan en los módulos
quantlab.senales_kaufman y quantlab.senales_raschke (dict PLANES).
Escribe reportes/<ID>_<nombre>/RESUMEN.md (la carpeta oficial de esa estrategia).
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # consola Windows

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))

from quantlab import backtest, data, report, validation
from quantlab import senales_kaufman, senales_raschke

RAIZ = Path(__file__).resolve().parents[2]
CORTE = "2016-01-01"
COSTE_LADO = 0.0002  # 2 pb por lado: ~1.5 pt de spread/2 + slippage sobre NDX ~8.000

PLANES = {**senales_kaufman.PLANES, **senales_raschke.PLANES}
# Carpeta oficial de cada señal en reportes/ (la fusión de 2026-09-16 retiró el prefijo ndx_).
CARPETA = {"breakout_er": "001_kaufman_breakout_er", "mr_2dias": "002_kaufman_mr_2dias",
           "holy_grail": "003_raschke_holy_grail", "ochenta_veinte": "004_raschke_ochenta_veinte"}

args = [a for a in sys.argv[1:] if not a.startswith("--")]
rapido = "--rapido" in sys.argv
nombre = args[0]
plan = PLANES[nombre]

norgate = data.cargar(RAIZ / "data" / "ndx_norgate_d1.parquet")
darwinex = data.cargar(RAIZ / "data" / "ndx_darwinex_d1.parquet")

cfg = backtest.Config(coste_pct=COSTE_LADO, riesgo_pct=0.01, **plan.get("config", {}))
r = validation.validar(norgate, plan["fn"], plan["params"], plan["grid"], plan["meseta"], cfg=cfg,
                       corte=CORTE, oos_extra={"darwinex": darwinex}, n_sim=1000 if rapido else 5000)
ruta = report.guardar(CARPETA.get(nombre, nombre), r, RAIZ / "reportes")
print(ruta.read_text(encoding="utf-8"))
print(f"-> {ruta}")
