# quant_lab — de 0 a 100: hipótesis → validación → estrategia

Base de trabajo para trading sistemático con un proceso que junta tres escuelas:

| Escuela | Qué aporta al proceso |
|---|---|
| **Jim Simons / Renaissance** | Los datos mandan. Un edge es una anomalía estadística que sobrevive al contraste contra el azar y a costes reales. Muchos edges pequeños y poco correlacionados valen más que uno grande. Todo se registra; nada se cree sin test. |
| **Perry Kaufman** | Robustez antes que rendimiento. Pocos parámetros, mesetas y no picos, adaptación al ruido (Efficiency Ratio / KAMA), probar en varios mercados y regímenes, entender por qué pierde un sistema. |
| **Linda Raschke** | Primero observar: *tendencias* del mercado medidas con estadística simple antes de escribir reglas. Playbook de setups con disparo-stop-salida definidos antes de entrar. Proceso diario, diario de operaciones, riesgo primero. |

La síntesis y los principios están en [00_FILOSOFIA.md](00_FILOSOFIA.md).

## El camino 0 → 100

```
 0 ─ Observación ─ 10 ─ Hipótesis ─ 25 ─ Tendencia ─ 40 ─ Prototipo ─ 55 ─ Validación ─ 75 ─ Estrategia ─ 85 ─ Incubación ─ 95 ─ Live ─ 100
        idea          falsable        ¿existe?        ¿se opera?      5 fases          sizing, cartera     paper/forward     monitor
```

Cada tramo tiene **una entrada, una salida y una puerta** (criterio numérico para pasar). Nada avanza sin cruzar su puerta; lo que no la cruza se marca como descartada en su `estado.json` con el motivo escrito. El detalle: [01_PROCESO_0_A_100.md](01_PROCESO_0_A_100.md).

| Tramo | Doc | Herramienta | Salida |
|---|---|---|---|
| 0–25 Idea → Hipótesis | [02_HIPOTESIS.md](02_HIPOTESIS.md) | `docs/laboratorio/PLANTILLA_HIPOTESIS_laboratorio.md` | `estrategias/<ID>_<nombre>/hipotesis.md` + fila en `estrategias/REGISTRO.md` |
| 25–40 Tendencia | [02_HIPOTESIS.md §4](02_HIPOTESIS.md) | `codigo/scripts/01_tendencia.py` · `quantlab.tendencies` | tabla de evento, p-valor |
| 40–55 Prototipo | [03_VALIDACION.md §1](03_VALIDACION.md) | `codigo/scripts/02_prototipo.py` · `quantlab.senales` | señal ≤30 líneas, métricas con costes |
| 55–75 Validación | [03_VALIDACION.md](03_VALIDACION.md) | `codigo/scripts/03_validar.py` · `quantlab.validation` | `reportes/<nombre>/RESUMEN.md` |
| 75–100 Estrategia → Live | [04_DE_EDGE_A_ESTRATEGIA.md](04_DE_EDGE_A_ESTRATEGIA.md) | `docs/laboratorio/PLANTILLA_ESTRATEGIA_laboratorio.md` | ficha en `estrategias/<ID>_<nombre>/` |

## Estructura

> El laboratorio nació como repo aparte (`quant_lab`) y en la fusión de 2026-09-16 pasó a colgar
> del MINI FONDO. Lo que antes era `src/` es ahora `codigo/`, `scripts/` es `codigo/scripts/`, y
> las fichas sueltas de `hipotesis/` y `estrategias/<estado>/` se unificaron en una carpeta por
> estrategia. Donde vive cada cosa hoy:

```
docs/laboratorio/           el proceso, escrito (estos ficheros)
├── 00_FILOSOFIA.md         las tres escuelas y los 10 principios
├── 01_PROCESO_0_A_100.md   tramos, puertas y entregables
├── 02_HIPOTESIS.md         cómo se formula y se registra una hipótesis; test de tendencia
├── 03_VALIDACION.md        protocolo de 5 fases con criterios
├── 04_DE_EDGE_A_ESTRATEGIA.md  sizing, cartera, ejecución, incubación, monitor, retirada
├── 05_METRICAS.md          definición única de cada métrica
├── 06_ANTIPATRONES.md      cómo se engaña uno mismo, y el checklist para no hacerlo
└── PLANTILLA_HIPOTESIS_laboratorio.md · PLANTILLA_ESTRATEGIA_laboratorio.md

estrategias/<ID>_<nombre>/  una carpeta por estrategia: hipótesis, informes, estado.json, bitácora
estrategias/REGISTRO.md     todo test cuenta · REGISTRO_laboratorio.md: las 17 corridas del lab
codigo/quantlab/            el motor (señales ≤30 líneas, validación, informe)
codigo/estrategias/         la señal canónica de cada estrategia: 001-004
codigo/scripts/             01_tendencia · 02_prototipo · 03_validar · 04_validar_ndx · 05_charts_ndx
codigo/app/aed_ndx.py       el AED interactivo (Streamlit)
reportes/<carpeta>/RESUMEN.md   ≤40 líneas por validación; es lo único que se relee
data/                       OHLC (no se versiona)
tests/                      humo · placebo · coherencia entre las dos copias de las señales
```

## Arranque

```bash
pip install -r requirements.txt
python -m pytest -q                              # 26 tests, <2 s
python codigo/scripts/01_tendencia.py  [datos.csv]      # ¿existe la tendencia?
python codigo/scripts/02_prototipo.py  holy_grail [datos.csv]
python codigo/scripts/03_validar.py    holy_grail [datos.csv] [--rapido]
python codigo/scripts/04_validar_ndx.py breakout_er --rapido   # NDX: IS Norgate <2016, OOS en ambas series
streamlit run codigo/app/aed_ndx.py
```

Sin fichero de datos los scripts usan una serie sintética (`data.sintetico`). Sirve para
comprobar que el código funciona y como **placebo**: con `autocorr=0` ninguna señal
debe pasar la validación (hay un test que lo garantiza).

Formato de datos: CSV o parquet con columna de fecha y `open, high, low, close[, volume]`.

## Estado — NDX, test inicial (2026-09-15)

IS = Norgate < 2016 · OOS = 2016+ en Norgate **y** Darwinex · 2 pb/lado · riesgo 1 %. Acta completa: `reportes/<ID>_*/RESUMEN.md`; registro de las 17 corridas en `estrategias/REGISTRO_laboratorio.md`.

| Estrategia | Escuela | Dir. | Tendencia IS | Proto IS (PF · n · t) | PF OOS Norgate / Darwinex | Muere en | Estado |
|---|---|---|---|---|---|---|---|
| E002 `breakout_er` | Kaufman | L | débil (p 0.28) | 2.22 · 93 · 2.4 | **5.70 / 4.86** (24 / 23 tr) | F1 solo por n<30 | `x_descartadas` — candidata a multi-mercado |
| E003 `mr_2dias` | Kaufman | L+S | débil (p 0.07) | 1.05 · 948 · 0.7 | 1.35 / 1.23 | proto; F1, F3, F5 | `x_descartadas` |
| E001 `holy_grail` | Raschke | L | débil (n 71, p 0.21) | 1.40 · 64 · 1.1 | 1.05 / 0.56 (13 / 23 tr) | F1–F5 | `x_descartadas` — H001.1 ADX 25 / multi-índice |
| E004 `ochenta_veinte` | Raschke | L+S | largo **pasa** (p 0.018) · corto muere | 0.74 · 1153 · −3.8 | 1.15 / 1.16 | proto; F1–F5 | `x_descartadas` — H004.1 solo largos |

**Aviso de datos:** en `ndx_norgate_d1` el `open` es igual al cierre previo en la mayoría de barras
anteriores a ~2000 (índice cash sin open real). Afecta a cualquier regla que use el open (80-20,
gaps). Para esas reglas: usar 2000+ o la serie Darwinex.

**AED interactivo:** `streamlit run codigo/app/aed_ndx.py` (necesita `requirements-extra.txt`) — Datos · Régimen (ADX/ER por año) · Tendencias
(4 eventos con semáforo de la puerta) · Resultados (RESUMEN, meseta, walk-forward, equity OOS).
Por defecto muestra solo IS; el OOS va tras un checkbox con aviso.

## Señales incluidas (ejemplos, no recomendaciones)

| Señal | Escuela | Idea |
|---|---|---|
| `kama_tendencia` | Kaufman | Seguir la pendiente de la KAMA; fuera cuando el ER dice que es ruido |
| `holy_grail` | Raschke | ADX > 30 + retroceso a la EMA20 = continuación |
| `ruptura_donchian` | Clásico (Turtle) | Ruptura de canal N con salida en canal M |
| `senales_kaufman.breakout_er`, `mr_2dias` | Kaufman | Canal + filtro ER (largos) · reversión 2 días con SMA200 |
| `senales_raschke.holy_grail`, `ochenta_veinte` | Raschke | Holy Grail solo largos · 80-20 ambos lados |

## Reglas de la casa (resumen; el detalle está en CLAUDE.md y docs/)

1. **Nada se cree sin test, y todo test se registra** — también los que fallan (`estrategias/REGISTRO.md`).
2. **Una señal = una función ≤ 30 líneas, ≤ 4 parámetros.** Si necesita más, son dos hipótesis.
3. **El OOS se mira una vez.** Si se toca dos veces, ya es IS.
4. **Costes desde el prototipo.** Un edge que muere con costes ×2 no es un edge.
5. **Meseta, no pico.** Si los vecinos del parámetro no ganan, el parámetro tampoco.
6. **Los umbrales no se bajan para que pase una estrategia.** Se bajan (o suben) para todas, con motivo escrito.
7. **Lo que no pasa se descarta con motivo escrito.** El cementerio vale tanto como el podio.
