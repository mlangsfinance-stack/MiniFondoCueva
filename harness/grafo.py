"""El grafo: qué agente corre en cada fase, qué veredicto espera y a dónde salta.

    investigacion --EDGE--> puerta_hipotesis --ok--> protocolo --> motor --> validacion --APROBADA--> puerta_deploy --ok--> incubacion
         |NO_EDGE                |no                                  |RECHAZADA (<=3 vueltas) -> motor       |no
         v                       v                                    |RECHAZADA (4a vez)      -> archivada   v
      archivada              archivada                                                                    archivada
"""
import re

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query

from . import estado as E

AGENTES = E.RAIZ / ".claude" / "agents"


# ---------- agentes ----------

def cargar_agente(nombre: str) -> dict:
    """Lee .claude/agents/<nombre>.md: frontmatter simple (clave: valor) + cuerpo como system prompt."""
    texto = (AGENTES / f"{nombre}.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        raise SystemExit(f"{nombre}.md no tiene frontmatter")
    meta = {}
    for linea in m.group(1).splitlines():
        if ":" in linea:
            k, v = linea.split(":", 1)
            meta[k.strip()] = v.strip()
    tools = [t.strip() for t in meta.get("tools", "Read, Glob, Grep").split(",") if t.strip()]
    return {"nombre": nombre, "tools": tools, "model": meta.get("model"), "prompt": m.group(2).strip()}


async def ejecutar(nombre_agente: str, tarea: str) -> dict:
    """Lanza un agente sobre una tarea. Devuelve veredicto, sesión y coste."""
    spec = cargar_agente(nombre_agente)
    opts = ClaudeAgentOptions(
        system_prompt=spec["prompt"],
        allowed_tools=spec["tools"],
        permission_mode="acceptEdits",
        cwd=str(E.RAIZ),
        setting_sources=["project"],
        model=spec["model"],
        max_turns=120,
    )
    print(f"\n=== {nombre_agente} ===")
    ultimo_texto = ""
    sesion = coste = None
    async for msg in query(prompt=tarea, options=opts):
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock) and b.text.strip():
                    print(b.text)
                    ultimo_texto = b.text
        elif isinstance(msg, ResultMessage):
            sesion, coste = msg.session_id, msg.total_cost_usd
            if msg.is_error:
                print(f"[error del agente] {msg.result}")
    m = re.search(r"VEREDICTO:\s*([A-Z_]+)", ultimo_texto)
    return {"veredicto": m.group(1) if m else "SIN_VEREDICTO", "sesion": sesion, "coste": coste}


# ---------- tareas por fase ----------

def _ctx(estado: dict) -> str:
    return f"Estrategia {estado['id']} «{estado['nombre']}». Carpeta: estrategias/{estado['carpeta']}/."


def tarea_investigacion(estado: dict) -> str:
    return (f"{_ctx(estado)} Lee hipotesis.md y haz el AED completo según docs/PROTOCOLO.md (pasos 01-02). "
            f"Escribe informe_aed.md en la carpeta y el código exploratorio en codigo/exploratorio_{estado['id']}.py. "
            f"Termina con VEREDICTO: EDGE o VEREDICTO: NO_EDGE.")


def tarea_protocolo(estado: dict) -> str:
    return (f"{_ctx(estado)} Lee hipotesis.md e informe_aed.md y redacta reglas.md: entrada, salida, filtros, riesgo, "
            f"parámetros con rangos, y los criterios de validación concretos (docs/PROTOCOLO.md, paso 03). "
            f"Termina con VEREDICTO: OK.")


def tarea_motor(estado: dict) -> str:
    vuelta = estado["vuelta_motor"]
    extra = ""
    if vuelta > 0:
        extra = (f" Es la vuelta {vuelta + 1}: lee informe_validacion.md, corrige SOLO lo que rechazó el validador "
                 f"y no toques los criterios.")
    return (f"{_ctx(estado)} Implementa reglas.md en codigo/estrategias/{estado['carpeta']}.py, corre backtest IS/OOS, "
            f"optimización, robustez y sizing (docs/PROTOCOLO.md pasos 04-07). Guarda salidas en reportes/{estado['carpeta']}/ "
            f"y el resumen en informe_motor.md.{extra} Termina con VEREDICTO: OK.")


def tarea_validacion(estado: dict) -> str:
    return (f"{_ctx(estado)} Audita informe_motor.md y reportes/{estado['carpeta']}/ contra reglas.md y docs/PROTOCOLO.md. "
            f"Rehaz los números clave tú mismo, no te fíes del informe. Escribe informe_validacion.md con el veredicto "
            f"razonado y, si aprueba, checklist_deploy.md. Termina con VEREDICTO: APROBADA o VEREDICTO: RECHAZADA.")


# ---------- transiciones ----------

async def avanzar(estado: dict) -> dict:
    """Ejecuta UNA fase de agente y mueve el estado. Devuelve el estado actualizado."""
    fase = estado["fase"]
    if fase not in E.FASES_AGENTE:
        return estado

    if fase == "investigacion":
        r = await ejecutar("investigador", tarea_investigacion(estado))
        siguiente = {"EDGE": "puerta_hipotesis", "NO_EDGE": "archivada"}.get(r["veredicto"])
    elif fase == "protocolo":
        r = await ejecutar("protocolo", tarea_protocolo(estado))
        siguiente = {"OK": "motor"}.get(r["veredicto"])
    elif fase == "motor":
        r = await ejecutar("motor", tarea_motor(estado))
        estado["vuelta_motor"] += 1
        siguiente = {"OK": "validacion"}.get(r["veredicto"])
    else:  # validacion
        r = await ejecutar("validador", tarea_validacion(estado))
        if r["veredicto"] == "APROBADA":
            siguiente = "puerta_deploy"
        elif r["veredicto"] == "RECHAZADA":
            siguiente = "motor" if estado["vuelta_motor"] < E.MAX_VUELTAS_MOTOR else "archivada"
        else:
            siguiente = None

    E.anotar(estado, fase, r["veredicto"], r["sesion"], r["coste"])
    if siguiente is None:
        # Veredicto inesperado: no avanzamos; queda en la misma fase para que Mariel mire la bitácora.
        print(f"[{fase}] veredicto {r['veredicto']!r} no reconocido; la estrategia se queda en {fase}.")
    else:
        estado["fase"] = siguiente
        print(f"[{fase}] {r['veredicto']} -> {siguiente}")
    E.guardar(estado)
    return estado


async def correr_hasta_puerta(estado: dict) -> dict:
    """Encadena fases de agente hasta topar con una puerta humana, un final o un veredicto raro."""
    while estado["fase"] in E.FASES_AGENTE:
        fase_antes = estado["fase"]
        estado = await avanzar(estado)
        if estado["fase"] == fase_antes:
            break
    return estado
