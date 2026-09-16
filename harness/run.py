"""CLI del harness.

  python -m harness.run nueva 001 oro_nasdaq   crea la carpeta y la ficha de hipótesis
  python -m harness.run run 001                corre fases hasta la siguiente puerta humana
  python -m harness.run ok 001 | no 001        cierra la puerta humana en la que esté
  python -m harness.run status                 tabla de todas las estrategias
  python -m harness.run loop                   corre todas las que estén en fase de agente
  python -m harness.run eficiencia 001         revisión a petición: bloqueos, despilfarro, notas al siguiente agente

  run / ok / loop admiten --sin-eficiencia para no correr el agente de eficiencia tras cada fase.
"""
import argparse
import asyncio
import sys

from . import estado as E
from . import grafo


def cmd_nueva(a):
    e = E.nueva(a.id, a.nombre)
    print(f"Creada estrategias/{e['carpeta']}/ — rellena hipotesis.md y luego: python -m harness.run run {a.id}")


def cmd_eficiencia(a):
    e = E.cargar(a.id)
    e = asyncio.run(grafo.revisar_eficiencia(e))
    print(f"\n> lee estrategias/{e['carpeta']}/eficiencia.md")


def cmd_run(a):
    E.EFICIENCIA_ACTIVA = not getattr(a, "sin_eficiencia", False)
    e = E.cargar(a.id)
    e = asyncio.run(grafo.correr_hasta_puerta(e))
    _aviso(e)


def cmd_ok(a):
    e = E.cargar(a.id)
    salto = {"puerta_hipotesis": "protocolo", "puerta_deploy": "incubacion"}
    if e["fase"] not in salto:
        raise SystemExit(f"{a.id} está en «{e['fase']}», no en una puerta humana.")
    E.anotar(e, e["fase"], "OK_MARIEL")
    e["fase"] = salto[e["fase"]]
    E.guardar(e)
    print(f"{a.id} -> {e['fase']}")
    if e["fase"] in E.FASES_AGENTE and not a.solo_marcar:
        cmd_run(a)


def cmd_no(a):
    e = E.cargar(a.id)
    if e["fase"] not in E.FASES_HUMANAS:
        raise SystemExit(f"{a.id} está en «{e['fase']}», no en una puerta humana.")
    E.anotar(e, e["fase"], "NO_MARIEL")
    e["fase"] = "archivada"
    E.guardar(e)
    print(f"{a.id} -> archivada")


def cmd_status(a):
    filas = E.listar()
    if not filas:
        print("Sin estrategias. Crea una con: python -m harness.run nueva 001 nombre")
        return
    print(f"{'ID':<5}{'nombre':<24}{'fase':<20}{'vueltas':<9}último")
    for e in filas:
        ult = e["historial"][-1] if e["historial"] else None
        ult_s = f"{ult['fecha']} {ult['fase']}->{ult['veredicto']}" if ult else "-"
        print(f"{e['id']:<5}{e['nombre']:<24}{e['fase']:<20}{e['vuelta_motor']:<9}{ult_s}")


def cmd_loop(a):
    E.EFICIENCIA_ACTIVA = not a.sin_eficiencia
    pendientes = [e for e in E.listar() if e["fase"] in E.FASES_AGENTE]
    if not pendientes:
        print("Nada en fase de agente. Todo espera a Mariel o está cerrado.")
    for e in pendientes:
        e = asyncio.run(grafo.correr_hasta_puerta(e))
        _aviso(e)


def _aviso(e):
    if e["fase"] == "puerta_hipotesis":
        print(f"\n> {e['id']} espera tu criterio: lee estrategias/{e['carpeta']}/informe_aed.md -> `ok {e['id']}` o `no {e['id']}`")
    elif e["fase"] == "puerta_deploy":
        print(f"\n> {e['id']} validada. Decide sizing y deploy: lee checklist_deploy.md -> `ok {e['id']}` o `no {e['id']}`")
    elif e["fase"] in E.FASES_FINALES:
        print(f"\n# {e['id']} -> {e['fase']}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # consola Windows
    p = argparse.ArgumentParser(prog="harness", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("nueva"); s.add_argument("id"); s.add_argument("nombre"); s.set_defaults(f=cmd_nueva)
    s = sub.add_parser("run"); s.add_argument("id"); s.add_argument("--sin-eficiencia", action="store_true"); s.set_defaults(f=cmd_run)
    s = sub.add_parser("ok"); s.add_argument("id"); s.add_argument("--solo-marcar", action="store_true"); s.add_argument("--sin-eficiencia", action="store_true"); s.set_defaults(f=cmd_ok)
    s = sub.add_parser("no"); s.add_argument("id"); s.set_defaults(f=cmd_no)
    s = sub.add_parser("status"); s.set_defaults(f=cmd_status)
    s = sub.add_parser("loop"); s.add_argument("--sin-eficiencia", action="store_true"); s.set_defaults(f=cmd_loop)
    s = sub.add_parser("eficiencia"); s.add_argument("id"); s.set_defaults(f=cmd_eficiencia)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
