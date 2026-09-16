"""Tests de humo del pipeline. Corren en segundos con datos sintéticos."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codigo"))

from quantlab import backtest, data, indicators, metrics, senales, tendencies, validation, report  # noqa: E402


@pytest.fixture(scope="module")
def df():
    return data.sintetico(n=1500, seed=1, autocorr=0.15)


def test_sintetico_es_ohlc_coherente(df):
    assert (df["high"] >= df[["open", "close"]].max(axis=1)).all()
    assert (df["low"] <= df[["open", "close"]].min(axis=1)).all()
    assert df.index.is_monotonic_increasing


def test_indicadores_sin_lookahead(df):
    """Un indicador no puede cambiar su valor pasado cuando llegan barras nuevas."""
    completo = indicators.kama(df["close"]).iloc[:1000]
    truncado = indicators.kama(df["close"].iloc[:1000])
    pd.testing.assert_series_equal(completo, truncado)
    assert indicators.maximo_previo(df["high"], 20).iloc[25] == df["high"].iloc[5:25].max()


def test_efficiency_ratio_en_rango(df):
    er = indicators.efficiency_ratio(df["close"], 10)
    assert ((er >= 0) & (er <= 1 + 1e-9)).all()


def test_backtest_ejecuta_en_apertura_siguiente(df):
    senal = pd.Series(0, index=df.index)
    senal.iloc[100] = 1
    senal.iloc[101] = 0
    res = backtest.backtest(df, senal, backtest.Config(stop_atr=None, coste_pct=0.0))
    t = res.trades
    assert len(t) == 1
    assert t.loc[0, "entrada"] == df.index[101] and t.loc[0, "salida"] == df.index[102]
    assert t.loc[0, "precio_entrada"] == df["open"].iloc[101]
    assert t.loc[0, "precio_salida"] == df["open"].iloc[102]


def test_stop_se_rellena_en_gap_en_contra(df):
    d = df.copy()
    senal = pd.Series(0, index=d.index)
    senal.iloc[200:260] = 1
    d.iloc[210, d.columns.get_loc("open")] = d["close"].iloc[209] * 0.80  # gap del -20 %
    d.iloc[210, d.columns.get_loc("low")] = d["open"].iloc[210] * 0.99
    res = backtest.backtest(d, senal, backtest.Config(stop_atr=2.0))
    t = res.trades.iloc[0]
    assert t["motivo"] == "stop" and t["precio_salida"] == pytest.approx(d["open"].iloc[210])


def test_equity_cuadra_con_trades(df):
    res = backtest.backtest(df, senales.kama_tendencia(df), backtest.Config())
    assert res.equity.iloc[-1] == pytest.approx(res.config.capital + res.trades["pnl"].sum())


def test_senales_devuelven_solo_menos1_0_1(df):
    for fn in senales.CATALOGO.values():
        s = fn(df)
        assert set(s.unique()) <= {-1, 0, 1} and len(s) == len(df)


def test_metricas_coherentes(df):
    res = backtest.backtest(df, senales.ruptura_donchian(df), backtest.Config())
    m = metrics.metricas(res)
    assert m["n_trades"] == len(res.trades)
    assert -1 <= m["max_dd"] <= 0
    assert 0 <= m["win_rate"] <= 1


def test_estudio_evento_y_permutacion(df):
    evento = df["close"] > indicators.sma(df["close"], 50)
    tab = tendencies.estudio_evento(df, evento, horizontes=(1, 5))
    assert list(tab.index) == [1, 5] and (tab["n"] > 0).all()
    p = tendencies.test_permutacion(df, evento, h=5, n_sim=200)
    assert 0 <= p["p_valor"] <= 1


def test_placebo_no_pasa_validacion():
    """Ruido puro sin autocorrelación: el protocolo debe descartar la señal."""
    d = data.sintetico(n=2500, seed=7, autocorr=0.0, deriva=0.0)
    r = validation.validar(d, senales.kama_tendencia, {"n": 10, "er_min": 0.3},
                           grid=[{"n": n, "er_min": 0.3} for n in (8, 10, 14)],
                           meseta=(("n", [8, 10, 14]), ("er_min", [0.2, 0.3, 0.4])), n_sim=200)
    assert r["pasa"] is False


def test_resumen_md_se_escribe(df, tmp_path):
    r = validation.validar(df, senales.kama_tendencia, {"n": 10, "er_min": 0.3},
                           grid=[{"n": 10, "er_min": 0.3}, {"n": 14, "er_min": 0.3}],
                           meseta=(("n", [8, 10, 14]), ("er_min", [0.2, 0.3, 0.4])), n_sim=200)
    ruta = report.guardar("prueba", r, tmp_path)
    texto = ruta.read_text(encoding="utf-8")
    assert "Veredicto" in texto and texto.count("\n") <= 40
