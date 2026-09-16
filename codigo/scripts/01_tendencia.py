"""Etapa 25-40: test de tendencia. Sin reglas, sin stops, sin optimizar.

Pregunta: tras el evento, ¿el mercado se comporta distinto de lo normal?
Uso:  python scripts/01_tendencia.py [ruta_csv_o_parquet]
Sin ruta usa datos sintéticos (placebo: no debería salir nada).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))

import pandas as pd

from quantlab import data, indicators, tendencies

df = data.cargar(sys.argv[1]) if len(sys.argv) > 1 else data.sintetico(autocorr=0.0)

# --- Define AQUÍ el evento de la hipótesis (ejemplo: H001, Holy Grail) ---
a, pdi, mdi = indicators.adx(df, 14)
e = indicators.ema(df["close"], 20)
evento = (a > 30) & (pdi > mdi) & (df["low"] <= e) & (df["close"] > e)

pd.set_option("display.width", 160)
print(f"Barras: {len(df)}   eventos: {int(evento.sum())}   ({evento.mean():.1%} de las barras)\n")
print("Estudio de evento (retorno forward condicional vs. base):")
print(tendencies.estudio_evento(df, evento).round(4))
print("\nRango:", tendencies.prob_rango(df, evento, h=3))
print("\nPermutación (h=5):", tendencies.test_permutacion(df, evento, h=5))
print("\nCriterio de paso a prototipo: n >= 100, exceso > 0 en 2+ horizontes, |t| >= 2, p_valor <= 0.05.")
