"""Panel Streamlit del harness: estado de cada estrategia, entregables y logs en vivo.

    .venv\\Scripts\\streamlit run harness/dashboard.py
"""
import json
import subprocess
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from harness import estado as E  # noqa: E402

ENTREGABLES = ["hipotesis.md", "informe_aed.md", "reglas.md", "informe_motor.md",
               "informe_validacion.md", "checklist_deploy.md", "eficiencia.md", "bitacora.md"]
PUERTAS = {"puerta_hipotesis": ("informe_aed.md", "¿Hay edge y merece reglas?"),
           "puerta_deploy": ("checklist_deploy.md", "¿Sizing y deploy?")}
COLOR = {"investigacion": "🟠", "protocolo": "🟠", "motor": "🟠", "validacion": "🟠",
         "puerta_hipotesis": "🟢", "puerta_deploy": "🟢", "incubacion": "✅", "archivada": "⚫"}

st.set_page_config(page_title="CUEVA", page_icon="🕳️", layout="wide")
st.title("🕳️ CUEVA — línea de producción")

auto = st.sidebar.toggle("Auto-refresco (10 s)", value=True)
if auto:
    st.markdown("<meta http-equiv='refresh' content='10'>", unsafe_allow_html=True)
st.sidebar.caption("🟠 agente trabajando · 🟢 espera tu criterio · ✅ incubación · ⚫ archivada")

# ---------- tabla general ----------
estrategias = E.listar()
if not estrategias:
    st.info("Sin estrategias. `python -m harness.run nueva 00X nombre`")
    st.stop()

filas = []
for e in estrategias:
    ult = e["historial"][-1] if e["historial"] else {}
    coste = sum(h.get("coste_usd") or 0 for h in e["historial"])
    filas.append({"ID": e["id"], "Nombre": e["nombre"], "Fase": f"{COLOR.get(e['fase'], '')} {e['fase']}",
                  "Vueltas motor": e["vuelta_motor"], "Último": f"{ult.get('fase', '-')} → {ult.get('veredicto', '-')}",
                  "Cuándo": ult.get("fecha", "-"), "Coste $": round(coste, 2)})
st.dataframe(filas, hide_index=True, width="stretch")

# ---------- detalle ----------
ids = [e["id"] for e in estrategias]
sel = st.sidebar.radio("Estrategia", ids, format_func=lambda i: f"{i} · {next(x['nombre'] for x in estrategias if x['id'] == i)}")
e = next(x for x in estrategias if x["id"] == sel)
carpeta = E.ESTRATEGIAS / e["carpeta"]
st.header(f"{e['id']} · {e['nombre']} — {COLOR.get(e['fase'], '')} {e['fase']}")

# Puerta humana: los pasos verdes se cierran aquí o por CLI, nunca por un agente.
if e["fase"] in PUERTAS:
    fichero, pregunta = PUERTAS[e["fase"]]
    st.success(f"**Espera tu criterio.** {pregunta} Lee `{fichero}` abajo.")
    c1, c2, _ = st.columns([1, 1, 6])
    if c1.button("✅ OK", key="ok"):
        subprocess.Popen([str(RAIZ / ".venv/Scripts/python"), "-m", "harness.run", "ok", e["id"]], cwd=RAIZ,
                         stdout=open(RAIZ / "reportes" / f"log_{e['id']}.txt", "a"), stderr=subprocess.STDOUT)
        st.toast(f"{e['id']} → siguiente fase; el harness sigue en segundo plano (mira el log).")
    if c2.button("⛔ NO", key="no"):
        subprocess.run([str(RAIZ / ".venv/Scripts/python"), "-m", "harness.run", "no", e["id"]], cwd=RAIZ)
        st.rerun()
elif e["fase"] in E.FASES_AGENTE:
    if st.button(f"▶ Correr {e['fase']} (sin eficiencia)"):
        subprocess.Popen([str(RAIZ / ".venv/Scripts/python"), "-m", "harness.run", "run", e["id"], "--sin-eficiencia"],
                         cwd=RAIZ, stdout=open(RAIZ / "reportes" / f"log_{e['id']}.txt", "a"), stderr=subprocess.STDOUT)
        st.toast(f"Lanzado {e['id']} en segundo plano.")

tabs = st.tabs(["Log en vivo", "Entregables", "Historial", "Reportes"])

with tabs[0]:
    log = RAIZ / "reportes" / f"log_{e['id']}.txt"
    if log.exists():
        texto = log.read_text(encoding="utf-8", errors="replace")
        st.code(texto[-12000:] or "(vacío)", language=None)
    else:
        st.caption("Sin log todavía. Aparece cuando corre el harness con salida a `reportes/log_<ID>.txt`.")

with tabs[1]:
    presentes = [f for f in ENTREGABLES if (carpeta / f).exists()]
    if not presentes:
        st.caption("Nada aún.")
    for f in presentes:
        with st.expander(f, expanded=(f in ("informe_aed.md", "informe_validacion.md") and e["fase"] in PUERTAS)):
            st.markdown((carpeta / f).read_text(encoding="utf-8", errors="replace"))

with tabs[2]:
    if e["historial"]:
        st.dataframe(e["historial"], hide_index=True, width="stretch")
    else:
        st.caption("Sin historial.")
    with st.expander("estado.json"):
        st.json(e)

with tabs[3]:
    rep = RAIZ / "reportes" / e["carpeta"]
    ficheros = sorted(rep.glob("*")) if rep.exists() else []
    if not ficheros:
        st.caption("Sin reportes (los genera el motor).")
    for f in ficheros:
        if f.suffix == ".csv":
            import pandas as pd
            with st.expander(f.name):
                st.dataframe(pd.read_csv(f).head(200), width="stretch")
        elif f.suffix in (".png", ".jpg"):
            st.image(str(f), caption=f.name)
        elif f.suffix in (".md", ".txt", ".json"):
            with st.expander(f.name):
                st.code(f.read_text(encoding="utf-8", errors="replace")[:12000], language=None)
