"""Test de humo de las funciones de cálculo de app/aed_ndx.py (sin UI)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "codigo"))
sys.path.insert(0, str(RAIZ / "codigo" / "app"))

from quantlab import data  # noqa: E402
import aed_ndx  # noqa: E402


@pytest.fixture(scope="module")
def df():
    return data.sintetico(600, seed=3, autocorr=0.1)


def test_resumen_y_series_basicas(df):
    r = aed_ndx.calcular_resumen(df)
    assert r["barras"] == 600 and r["max_dd"] <= 0 and 0 < r["pct_dias_pos"] < 1
    assert set(aed_ndx.vol_rodante(df).columns) == {"vol_20", "vol_60"}
    assert len(aed_ndx.retornos_por_anio(df)) >= 2
    cmp = aed_ndx.comparar_series(df, df)
    assert cmp["n_solape"] == 600 and cmp["correlacion"] == pytest.approx(1.0)
    assert (cmp["ratio"] == 1).all()


def test_filtro_oos(df):
    corte = pd.Timestamp(aed_ndx.CORTE_OOS)
    d2 = df.copy()
    d2.index = pd.bdate_range("2015-06-01", periods=len(d2))
    assert (aed_ndx.filtrar_periodo(d2, False).index < corte).all()
    assert len(aed_ndx.filtrar_periodo(d2, True)) == len(d2)


def test_regimen(df):
    reg = aed_ndx.calcular_regimen(df, 14, 10)
    assert {"adx", "er", "atr"} <= set(reg.columns)
    pa = aed_ndx.regimen_por_anio(reg, 0.3)
    assert ((pa["pct_adx_30"] >= 0) & (pa["pct_adx_30"] <= 1)).all()
    assert pa["barras"].sum() == len(df)


@pytest.mark.parametrize("nombre", list(aed_ndx.EVENTOS))
def test_eventos_y_estudio(df, nombre):
    params = {k: v[3] for k, v in aed_ndx.EVENTOS[nombre]["params"].items()}
    lados = aed_ndx.eventos(df, nombre, **params)
    assert "largo" in lados
    for ev, d in lados.values():
        assert ev.dtype == bool and len(ev) == len(df)
        res = aed_ndx.estudiar(d, ev, n_sim=50)
        assert list(res["tabla"].index) == list(aed_ndx.HORIZONTES)
        sem = aed_ndx.semaforo(res["tabla"], res["perm"])
        assert len(sem) == 4 and all(isinstance(ok, bool) for ok, _ in sem.values())


def test_equity_desde_trades():
    t = pd.DataFrame({"salida": ["2020-01-03", "2020-01-02", "2020-01-05"], "pnl_pct": [0.1, -0.05, 0.02]})
    eq = aed_ndx.equity_desde_trades(t)
    assert eq.index.is_monotonic_increasing
    assert eq["equity"].iloc[-1] == pytest.approx(0.95 * 1.1 * 1.02)
    assert (eq["drawdown"] <= 0).all()
