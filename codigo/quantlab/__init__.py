"""quantlab — base mínima para llevar una idea de trading de 0 a 100.

Pipeline: observación → hipótesis → test de tendencia → prototipo → validación
→ estrategia → incubación → live. Cada módulo cubre una etapa:

- data         carga de OHLC, datos sintéticos, particiones IS/OOS y walk-forward
- indicators   ATR, KAMA / efficiency ratio (Kaufman), ADX, z-score, canales
- tendencies   estudios de evento y probabilidades condicionales (Raschke)
- senales      señales de ejemplo (una función = una regla, pocos parámetros)
- backtest     motor único: ejecución a la apertura siguiente, stop ATR, costes
- metrics      métricas de trades y curva de capital
- validation   IS/OOS, walk-forward, meseta de parámetros, Monte Carlo, stress
- report       RESUMEN.md de ≤40 líneas con el veredicto
"""
from . import data, indicators, tendencies, senales, backtest, metrics, validation, report  # noqa: F401

__version__ = "0.1.0"
