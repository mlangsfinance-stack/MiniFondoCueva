"""Estado de cada estrategia: un estado.json en su carpeta. Nada más."""
import json
import datetime as dt
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ESTRATEGIAS = RAIZ / "estrategias"

# Fases del grafo. Las "puerta_*" las cierra Mariel; el resto las cierra un agente.
FASES_AGENTE = {"investigacion", "protocolo", "motor", "validacion"}
FASES_HUMANAS = {"puerta_hipotesis", "puerta_deploy"}
FASES_FINALES = {"incubacion", "archivada"}

MAX_VUELTAS_MOTOR = 3  # validación rechazada → vuelve al motor, como mucho 3 veces


def ahora() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def carpeta(id_: str) -> Path:
    hits = sorted(ESTRATEGIAS.glob(f"{id_}_*"))
    if not hits:
        raise SystemExit(f"No existe ninguna estrategia con ID {id_} en {ESTRATEGIAS}")
    return hits[0]


def cargar(id_: str) -> dict:
    return json.loads((carpeta(id_) / "estado.json").read_text(encoding="utf-8"))


def guardar(estado: dict) -> None:
    ruta = ESTRATEGIAS / estado["carpeta"] / "estado.json"
    ruta.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")


def nueva(id_: str, nombre: str) -> dict:
    nombre_carpeta = f"{id_}_{nombre}"
    ruta = ESTRATEGIAS / nombre_carpeta
    if ruta.exists():
        raise SystemExit(f"Ya existe {ruta}")
    ruta.mkdir(parents=True)
    plantilla = (RAIZ / "docs" / "PLANTILLA_HIPOTESIS.md").read_text(encoding="utf-8")
    (ruta / "hipotesis.md").write_text(plantilla.replace("{ID}", id_).replace("{NOMBRE}", nombre), encoding="utf-8")
    (ruta / "bitacora.md").write_text(f"# Bitácora {nombre_carpeta}\n\n", encoding="utf-8")
    estado = {
        "id": id_,
        "nombre": nombre,
        "carpeta": nombre_carpeta,
        "fase": "investigacion",
        "vuelta_motor": 0,
        "creada": ahora(),
        "historial": [],
    }
    guardar(estado)
    return estado


def listar() -> list[dict]:
    out = []
    for f in sorted(ESTRATEGIAS.glob("*/estado.json")):
        out.append(json.loads(f.read_text(encoding="utf-8")))
    return out


def anotar(estado: dict, fase: str, veredicto: str, sesion: str | None = None, coste: float | None = None) -> None:
    """Deja rastro en estado.json y en la bitácora humana."""
    entrada = {"fecha": ahora(), "fase": fase, "veredicto": veredicto, "sesion": sesion, "coste_usd": coste}
    estado["historial"].append(entrada)
    linea = f"- {entrada['fecha']} · **{fase}** → {veredicto}"
    if coste is not None:
        linea += f" · ${coste:.2f}"
    if sesion:
        linea += f" · sesión `{sesion}`"
    with (ESTRATEGIAS / estado["carpeta"] / "bitacora.md").open("a", encoding="utf-8") as f:
        f.write(linea + "\n")
