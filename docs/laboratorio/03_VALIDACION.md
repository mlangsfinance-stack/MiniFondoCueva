# 03 — Validación: prototipo y las 5 fases

## 1. Prototipo (tramo 40–55)

La regla más simple que captura la tendencia confirmada. Con costes y stop desde el minuto uno.

**Forma de una señal** (`codigo/quantlab/senales.py`):
- Una función `senal(df, **params) -> pd.Series` con valores {-1, 0, 1} = posición deseada al
  cierre de cada barra. El motor la ejecuta en la apertura siguiente.
- ≤ 30 líneas, ≤ 4 parámetros, sin estado oculto (nada de variables globales, nada de "recordar" trades).
- Sin look-ahead: cada valor usa solo datos hasta esa barra. `indicators.maximo_previo` y
  el test `test_indicadores_sin_lookahead` son la referencia.

**Motor** (`quantlab.backtest`): uno solo. Ejecución en apertura siguiente, stop k·ATR
intrabarra con gap en contra, costes por lado sobre nocional, riesgo fijo por trade. Si una
estrategia necesita otra mecánica (órdenes límite, salida parcial…), se añade **al motor** con
test, no se escribe un motor aparte.

**Puerta a validación**, sobre toda la muestra y con costes realistas:
PF > 1.2 · ≥ 100 trades · expectancia > 0.1 R · t-stat > 2 · el resultado no depende de un año
(PnL por año: ≥ 60 % de años positivos).

Aquí todavía **no** se optimiza. Los parámetros son los "naturales" de la hipótesis (ADX 30 porque
es el umbral clásico, no porque 31 dé más). Si el prototipo no pasa con parámetros naturales,
lo normal es que la tendencia era débil: volver atrás, no afinar.

## 2. Las 5 fases (tramo 55–75)

Se ejecutan todas, en orden, con una sola orden (`codigo/scripts/03_validar.py`). Los umbrales viven en
`validation.Criterios`; son defaults calibrables **para el laboratorio entero**, no para una
estrategia. Cambiar uno se documenta en este fichero con fecha y motivo.

### Fase 1 — IS / OOS · *¿sobrevive a datos no vistos?*
- Partición temporal 70/30. El OOS se evalúa **una vez** con los parámetros del prototipo.
- Puerta: PF OOS ≥ 1.3 · ≥ 30 trades OOS · MaxDD OOS < 20 % · PF OOS sin el mejor trade > 1.0.
- Frontera (PF OOS 1.25–1.35): no se decide a máquina; se revisa a mano y se anota.

### Fase 2 — Walk-forward · *¿sobrevive a re-optimizar en el tiempo?*
- 5 ventanas rodantes; en cada una se elige el mejor parámetro del grid en IS y se aplica al OOS.
- Grid pequeño (Kaufman): pocos parámetros, rangos amplios, pasos gruesos. Un grid de 500
  combinaciones es un generador de ajuste, no una prueba.
- Puerta: eficiencia WF (CAGR OOS medio / CAGR IS medio) ≥ 0.5 · ≥ 60 % de ventanas OOS positivas.

### Fase 3 — Meseta de parámetros · *¿sobrevive a mover los parámetros?*
- Superficie PF sobre los dos parámetros principales (5×5). Se mira el centro y sus 8 vecinos.
- Puerta: los 9 existen (≥ 10 trades cada uno) · todos PF ≥ 1.2 · ningún vecino cae > 30 % respecto al centro.
- Si el centro es el máximo aislado de la superficie, es un pico: se descarta aunque pase lo demás.

### Fase 4 — Monte Carlo · *¿sobrevive a reordenar la suerte?*
- 5.000 permutaciones del orden de los trades OOS (retorno % sobre equity, compuesto).
- Puerta: p5 del retorno final > 0 · p95 del MaxDD < 25 % · probabilidad de DD ≥ 35 % < 5 %.
- El cono resultante (p5–p95 de equity) es la referencia para incubación y live.

### Fase 5 — Stress · *¿sobrevive al mundo real?*
- Costes ×2 en OOS → PF ≥ 1.1.
- PF de toda la muestra sin los 2 mejores años → ≥ 1.1.
- PF del peor tercio de la muestra → ≥ 1.1.

### Veredicto
- Todo en verde → **VALIDADA**. Pasa a `estrategias/3_validacion/` → `4_incubacion/` con ficha.
- Fase 1 en frontera → **revisión manual**, se documenta la decisión.
- Cualquier otra cosa → **DESCARTADA** con el RESUMEN.md como acta.

## 3. Multi-mercado y multi-régimen (cuando aplica)

Si la hipótesis se formuló para una familia de activos, la validación se corre en cada uno y se
exige: pasa Fase 1 en ≥ 2/3 de los activos, y el agregado pasa todo. Un edge que solo vive en
un activo se puede operar, pero se etiqueta como tal y se le exige más historial en incubación.

## 4. Salida: RESUMEN.md

`reportes/<nombre>/RESUMEN.md`, ≤ 40 líneas: veredicto, parámetros, métricas IS/OOS, tabla de
checks por fase, walk-forward por ventana, PF por tercios. Es lo único que se relee después.
Los CSV (trades OOS, meseta, WF) quedan al lado para auditoría, no para lectura.

## 5. Umbrales — historial de cambios

| Fecha | Umbral | Antes | Después | Motivo |
|---|---|---|---|---|
| 2026-09-15 | (defaults iniciales) | — | ver `validation.Criterios` | arranque del laboratorio |
