# CLAUDE.md — MINI FONDO

Repo de **desarrollo y validación de estrategias de trading con el método TIS**, ejecutado por
4 agentes encadenados en un harness sobre un motor de validación único (`codigo/quantlab/`).
Es el lead magnet de Trade It Simple: el que lo reciba tiene que poder clonarlo, correr el
ejemplo y meter su propia hipótesis sin preguntar nada. Escribe para esa persona.

## Los agentes (`.claude/agents/`)
| Agente | Pasos TIS | Entra | Sale | Veredicto |
|---|---|---|---|---|
| `investigador` | 01-02 | `hipotesis.md` | `informe_aed.md`, `codigo/exploratorio_<ID>.py` | `EDGE` / `NO_EDGE` |
| `protocolo` | 03 | hipótesis + AED | `reglas.md` | `OK` |
| `motor` | 04-07 | `reglas.md` | `codigo/estrategias/<carpeta>.py`, `reportes/<carpeta>/`, `informe_motor.md` | `OK` |
| `validador` | cierre + 08 | todo lo anterior | `informe_validacion.md`, `checklist_deploy.md` | `APROBADA` / `RECHAZADA` |
| `eficiencia` | transversal | estado, bitácora, entregables | `eficiencia.md` (notas para el siguiente agente) | `FLUIDO` / `AVISO` / `BLOQUEADO` |

`eficiencia` no está en el grafo: corre solo después de cada fase de agente (se apaga con
`--sin-eficiencia`) o a petición con `python -m harness.run eficiencia <ID>`. No mueve la fase, no toca
entregables, no decide criterio.

Los mismos ficheros sirven para dos cosas: el harness los usa como system prompt, y desde
Claude Code se invocan como subagentes (`@investigador`, etc.) para trabajo interactivo.

## El grafo (`harness/grafo.py`)
```
investigacion -EDGE-> [puerta_hipotesis] -ok-> protocolo -> motor -> validacion -APROBADA-> [puerta_deploy] -ok-> incubacion
      |NO_EDGE              |no                              ^         |RECHAZADA (<=3 vueltas)         |no
   archivada             archivada                           +---------+  4a vez -> archivada        archivada
```
Las `[puertas]` las cierra la persona (`ok`/`no`). Son los pasos verdes: criterio.
Todo lo demás lo cierra un agente con su línea `VEREDICTO:`.

## El motor (`codigo/quantlab/`)
Un solo motor para todas las estrategias. `backtest.py` ejecuta a la apertura siguiente con stop
ATR intrabarra y costes por lado; `validation.py` corre las 5 fases (IS/OOS, walk-forward, meseta,
Monte Carlo, stress); `report.py` escribe `reportes/<carpeta>/RESUMEN.md`. Una estrategia es
`codigo/estrategias/<ID>_<nombre>.py` con `senal(df, **params)` (≤30 líneas) y un dict `PLAN`.
`codigo/validar.py <ID> <datos>` lo corre todo. **No se escribe un motor por estrategia.**

## Origen
Fusión (2026-09-16) de tres sesiones en vivo del 2026-09-15: el laboratorio `quant_lab`
(motor, docs, Kaufman y Raschke → 001-004), el repo de agentes `CUEVA` (agentes, harness, dashboard,
pruebas → 005-007) y el agente de eficiencia. Este repo es la única copia viva.

## Cómo se usa
```
.venv\Scripts\activate
python -m pytest -q
python codigo/validar.py 001 --sintetico --rapido      # placebo
python codigo/validar.py 001 data/NDX_D1.csv           # ejemplo con datos
python -m harness.run nueva 002 nombre                 # carpeta + plantilla de hipótesis
python -m harness.run run 002                          # corre hasta la siguiente puerta
python -m harness.run ok 002 | no 002                  # cierras la puerta
python -m harness.run status
python -m harness.run eficiencia 002                 # revisión a petición
streamlit run harness/dashboard.py
```

## Dónde va cada cosa
| Qué | Dónde |
|---|---|
| Hipótesis, informes, reglas, estado de una estrategia | `estrategias/<ID>_<nombre>/` |
| Señal y plan de una estrategia | `codigo/estrategias/<ID>_<nombre>.py` |
| Exploratorios | `codigo/exploratorio_<ID>.py` |
| Salidas numéricas | `reportes/<ID>_<nombre>/` (los `*_placebo/` no se versionan) |
| Datos de mercado (no se versionan) | `data/` |
| Protocolo y plantillas | `docs/` · el proceso del laboratorio en `docs/laboratorio/` |
| Registro de todas las pruebas | `estrategias/REGISTRO.md` (también las que fallan) |
| Motor | `codigo/quantlab/` (cambios con test en `tests/`) |

**La raíz no recibe ficheros nuevos.**

## Reglas duras (para agentes y para sesiones interactivas)
1. Los criterios viven en `docs/PROTOCOLO.md`. **Ningún agente los baja.** Solo la persona, editando ese fichero.
2. **OOS se mira una vez.** Optimizar es cosa de IS. Un rechazo no autoriza a reoptimizar mirando OOS.
3. Costes dentro de cada métrica. No existen números brutos en los informes.
4. Cada agente escribe solo en sus carpetas (están en su `.md`). El validador no arregla; señala.
5. Cada turno de agente termina con `VEREDICTO: <X>` en la última línea, o el harness lo deja parado.
6. Los pasos verdes (hipótesis, criterio sobre el AED, sizing, deploy) no los decide ningún agente.
7. No leer `trades_oos.csv` ni `meseta.csv` al contexto: leer solo `RESUMEN.md`.
8. Sin push sin confirmación.
