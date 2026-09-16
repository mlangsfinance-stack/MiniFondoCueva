"""Validación de 5 fases de una estrategia del repo sobre tus datos.

Uso:
  python codigo/validar.py 001 data/NDX_D1.csv                       IS/OOS por fecha de corte
  python codigo/validar.py 001 data/NDX_D1.csv --corte 2016-01-01
  python codigo/validar.py 001 data/NDX_D1.csv --oos-extra data/NDX_darwinex_D1.csv
  python codigo/validar.py 001 --sintetico                            placebo: NO debe pasar
  añade --rapido para Monte Carlo de 1 000 barajados en vez de 5 000

La estrategia se busca en codigo/estrategias/<ID>_*.py y debe exponer `PLAN`.
Escribe reportes/<carpeta>/RESUMEN.md (+ meseta.csv, walk_forward.csv, trades_oos.csv).
Sin datos, `--sintetico` usa una serie AR(1) con autocorr 0: si una regla "pasa" ahí, algo está mal.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "codigo"))

from quantlab import backtest, data, report, validation  # noqa: E402


def cargar_plan(id_: str):
    hits = sorted((RAIZ / "codigo" / "estrategias").glob(f"{id_}_*.py"))
    if not hits:
        raise SystemExit(f"No hay codigo/estrategias/{id_}_*.py")
    spec = importlib.util.spec_from_file_location(hits[0].stem, hits[0])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return hits[0].stem, mod.PLAN


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("id")
    p.add_argument("datos", nargs="?")
    p.add_argument("--corte", default="2016-01-01", help="fecha desde la que empieza el OOS (o fracción, p. ej. 0.7)")
    p.add_argument("--oos-extra", help="segunda serie (p. ej. CFD del broker) sobre la que repetir el OOS")
    p.add_argument("--coste", type=float, default=0.0002, help="coste por lado sobre el nocional (0.0002 = 2 pb)")
    p.add_argument("--riesgo", type=float, default=0.01, help="fracción del equity arriesgada por trade")
    p.add_argument("--sintetico", action="store_true")
    p.add_argument("--rapido", action="store_true")
    a = p.parse_args()

    carpeta, plan = cargar_plan(a.id)
    if a.sintetico:
        df = data.sintetico(n=4000, autocorr=0.0)
        corte = 0.7
    elif a.datos:
        df = data.cargar(a.datos)
        corte = float(a.corte) if a.corte.replace(".", "", 1).isdigit() else a.corte
    else:
        raise SystemExit("Indica un fichero de datos o --sintetico")
    oos_extra = {"extra": data.cargar(a.oos_extra)} if a.oos_extra else None

    cfg = backtest.Config(coste_pct=a.coste, riesgo_pct=a.riesgo, **plan.get("config", {}))
    r = validation.validar(df, plan["fn"], plan["params"], plan["grid"], plan["meseta"], cfg=cfg,
                           corte=corte, oos_extra=oos_extra, n_sim=1000 if a.rapido else 5000)
    if a.sintetico:
        carpeta += "_placebo"  # no pisa la validación real
    ruta = report.guardar(carpeta, r, RAIZ / "reportes")
    print(ruta.read_text(encoding="utf-8"))
    print(f"-> {ruta}")


if __name__ == "__main__":
    main()
