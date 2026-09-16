# 01 — El proceso 0 → 100

Ocho tramos. Cada tramo tiene **entrada** (qué hace falta para empezar), **trabajo**,
**puerta** (criterio numérico para salir) y **entregable** (qué queda escrito).
Una idea solo avanza cruzando la puerta; si no la cruza, va a `estrategias/x_descartadas/`
con el motivo. El número es el "porcentaje de camino": sirve para saber dónde está cada cosa.

| # | Tramo | Entrada | Puerta para salir | Entregable |
|---|---|---|---|---|
| 0–10 | **Observación** | Una idea, de donde venga | Se puede escribir en una frase qué hace el mercado después de qué | Nota en `estrategias/REGISTRO.md` (estado `idea`) |
| 10–25 | **Hipótesis** | Idea escrita | Ficha completa: mecanismo, universo, predicción, métrica, criterio de muerte | `estrategias/<ID>_<nombre>/hipotesis.md` |
| 25–40 | **Tendencia** | Ficha + datos | n ≥ 100 eventos · exceso > 0 en ≥ 2 horizontes · \|t\| ≥ 2 · p-valor permutación ≤ 0.05 · en ≥ 2 mercados si aplica | Tabla de evento pegada en la ficha |
| 40–55 | **Prototipo** | Tendencia confirmada | Señal ≤ 30 líneas, ≤ 4 parámetros · con costes: PF > 1.2 · ≥ 100 trades · expectancia > 0.1 R · t-stat > 2 | Función en `codigo/quantlab/senales.py` (o módulo propio) + métricas |
| 55–75 | **Validación** | Prototipo que pasa | Las 5 fases en verde ([03_VALIDACION.md](03_VALIDACION.md)) | `reportes/<nombre>/RESUMEN.md` |
| 75–85 | **Estrategia** | Validada | Ficha completa: sizing, límites, correlación con lo existente, plan de ejecución, plan de retirada | `estrategias/<ID>_<nombre>/ (fase incubacion)` |
| 85–95 | **Incubación** | Estrategia especificada | ≥ 3 meses o ≥ 30 trades en paper/forward · resultado dentro del cono Monte Carlo · paridad con la plataforma real | Sección "Incubación" de la ficha |
| 95–100 | **Live + monitor** | Incubación superada | Operando con capital; revisión mensual contra el cono; regla de retirada activa | `estrategias/5_live/` + registro mensual |

## Reglas transversales

- **Un tramo por sesión.** Testar tendencia, prototipar y validar son sesiones distintas. Mezclarlas
  es la forma más rápida de mirar el OOS "sin querer".
- **Ida sin vuelta atrás gratis.** Si en validación se toca la regla, se vuelve a **Prototipo** con
  hipótesis nueva (Hxxx.1) y cuenta como test nuevo en el registro.
- **El registro es sagrado.** Cada test, pase o no, es una fila en `estrategias/REGISTRO.md`. Ese
  número (cuántas cosas has probado) es el que corrige el umbral de significación.
- **Descartar es un resultado.** Ficha a `x_descartadas/` con: en qué puerta murió, con qué
  números, qué se aprendió. Se relee antes de proponer ideas parecidas.

## Qué se hace con qué herramienta

```
Observación   → cuaderno / diario de mercado (Raschke). Nada de código todavía.
Hipótesis     → docs/laboratorio/PLANTILLA_HIPOTESIS_laboratorio.md
Tendencia     → codigo/scripts/01_tendencia.py   quantlab.tendencies (estudio_evento, prob_rango, test_permutacion)
Prototipo     → codigo/scripts/02_prototipo.py   quantlab.senales + quantlab.backtest + quantlab.metrics
Validación    → codigo/scripts/03_validar.py     quantlab.validation (5 fases) + quantlab.report
Estrategia    → docs/laboratorio/PLANTILLA_ESTRATEGIA_laboratorio.md (sizing, cartera, ejecución, retirada: docs/04)
Incubación    → plataforma real en paper + comparación con el cono MC del RESUMEN
Live          → misma ficha; sección de monitor mensual
```

## Tiempos orientativos

Observación y hipótesis: horas. Tendencia: una sesión. Prototipo: una o dos sesiones.
Validación: una sesión de máquina, otra de lectura. Incubación: meses. Si una idea lleva
semanas en prototipo, es que se está optimizando: volver a la hipótesis.
