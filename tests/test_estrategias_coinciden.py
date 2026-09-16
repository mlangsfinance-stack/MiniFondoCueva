"""Las estrategias 001-004 existen en dos sitios por historia, no por diseño.

`codigo/estrategias/<ID>_<nombre>.py` es la copia **canónica** (la que usa `codigo/validar.py` y
la que escriben los agentes). `codigo/quantlab/senales_kaufman.py` y `senales_raschke.py` son la
copia del laboratorio, de la que todavía tiran `codigo/scripts/04_validar_ndx.py`,
`05_charts_ndx.py` y el exploratorio de Kaufman/Raschke.

Mientras las dos existan tienen que dar **exactamente** la misma señal y el mismo plan: si se
separan, los números de `estrategias/REGISTRO.md` dejan de ser reproducibles sin que nadie se
entere. Este test es el que impide esa deriva.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "codigo"))

from quantlab import data, senales_kaufman, senales_raschke  # noqa: E402

PLANES_LAB = {**senales_kaufman.PLANES, **senales_raschke.PLANES}

# fichero canónico -> clave en los PLANES del laboratorio
PAREJAS = [
    ("001_kaufman_breakout_er", "breakout_er"),
    ("002_kaufman_mr_2dias", "mr_2dias"),
    ("003_raschke_holy_grail", "holy_grail"),
    ("004_raschke_ochenta_veinte", "ochenta_veinte"),
]


def _cargar(stem: str):
    ruta = RAIZ / "codigo" / "estrategias" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(stem, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def df():
    return data.sintetico(n=1500, autocorr=0.05)


@pytest.mark.parametrize("stem,clave", PAREJAS)
def test_senal_identica(df, stem, clave):
    plan = _cargar(stem).PLAN
    lab = PLANES_LAB[clave]
    esperada = lab["fn"](df, **lab["params"])
    obtenida = plan["fn"](df, **plan["params"])
    assert obtenida.equals(esperada), f"{stem} se ha separado de quantlab.{clave}"


@pytest.mark.parametrize("stem,clave", PAREJAS)
def test_plan_identico(stem, clave):
    plan = _cargar(stem).PLAN
    lab = PLANES_LAB[clave]
    for campo in ("params", "grid", "meseta"):
        assert plan[campo] == lab[campo], f"{stem}: {campo} difiere de quantlab.{clave}"
    assert plan.get("config", {}) == lab.get("config", {}), f"{stem}: config difiere"


@pytest.mark.parametrize("stem,_clave", PAREJAS)
def test_estrategia_es_validable(stem, _clave):
    """Lo que `codigo/validar.py` espera encontrar: una `senal` y un `PLAN` con sus cuatro claves."""
    mod = _cargar(stem)
    assert callable(mod.senal)
    assert {"fn", "params", "grid", "meseta"} <= set(mod.PLAN)
