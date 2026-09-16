# CLAUDE.md — MINI FONDO

Repo de **desarrollo y validación de estrategias de trading con el método TIS**, ejecutado por
4 agentes encadenados en un harness sobre un motor de validación único (`codigo/quantlab/`).
Es el lead magnet de Trade It Simple: el que lo reciba tiene que poder clonarlo, correr el
ejemplo y meter su propia hipótesis sin preguntar nada. Escribe para esa persona.

**La audiencia no es técnica.** La puerta de entrada es `EMPIEZA_AQUI.md` (guía por niveles, sin
jerga) y `EMPEZAR.bat` / `empezar.sh` (puesta en marcha con doble clic). El `README.md` es la
referencia técnica, no el primer contacto. Cualquier cosa que se añada tiene que caber en uno de
los tres niveles: **0** mirar sin instalar, **1** correr el motor, **2** los agentes.

## Los agentes (`.claude/agents/`)
| Agente | Pasos TIS | Entra | Sale | Veredicto |
|---|---|---|---|---|
| `investigador` | 01-02 | `hipotesis.md` | `informe_aed.md`, `codigo/exploratorio_<ID>.py` | `EDGE` / `NO_EDGE` |
| `protocolo` | 03 | hipótesis + AED | `reglas.md` | `OK` |
| `motor` | 04-07 | `reglas.md` | `codigo/estrategias/<carpeta>.py`, `reportes/<carpeta>/`, `informe_motor.md` | `OK` |
| `validador` | cierre + 08 | todo lo anterior | `informe_validacion.md`, `checklist_deploy.md` | `APROBADA` / `RECHAZADA` |
| `eficiencia` | transversal | estado, bitácora, entregables | `eficiencia.md` (notas para el siguiente agente) | `FLUIDO` / `AVISO` / `BLOQUEADO` |
| `mariel` | fuera del grafo | lo que le preguntes | una respuesta, no ficheros | — (no mueve fase) |

`mariel` es la mentora del método: revisa hipótesis, le busca el hueco a un resultado, traduce los
informes y avisa cuando alguien se está haciendo trampa. **Solo lee** (sin Write ni Bash) a
propósito: no produce entregables. No confundir con la autoría — quien opera el repo es la persona
que lo recibió, y los otros cinco agentes le hablan a ella, nunca a "Mariel".

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

## El método (`.claude/skills/` + `docs/`)
Los seis skills del método TIS están instalados en `.claude/skills/tis-*/SKILL.md`: `tis-estilo`
(gobierna a los otros cinco: voz, anti-slop y no negociables), `tis-research-edge`,
`tis-diseno-estrategia`, `tis-validacion`, `tis-riesgo-portafolio` y `tis-bitacora-estrategia`.
**Aplica `tis-estilo` a cualquier texto que escribas en este repo.** Lo explicado para humanos está
en `docs/METODO_TIS.md`.

Los seis agentes declaran `Skill` en su frontmatter `tools:`. Es obligatorio: `grafo.py` pasa
`allowed_tools=spec["tools"]` tal cual, así que un agente sin esa herramienta **no puede cargar los
skills** y la instrucción "aplica tis-estilo" se queda en papel mojado. Si añades un agente, no te
olvides de `Skill`.

La autoridad de criterio es **`docs/MIS_REGLAS.md`**, el fichero de la persona: sus umbrales mandan
sobre los defaults de `docs/PROTOCOLO.md` y sobre `quantlab.validation.Criterios`. Ningún agente lo
edita.

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
| Criterio de la persona (autoridad) | `docs/MIS_REGLAS.md` — **no lo toca ningún agente** |
| El método, para humanos | `docs/METODO_TIS.md` · los skills en `.claude/skills/` |
| Registro de todas las pruebas | `estrategias/REGISTRO.md` (también las que fallan) |
| Motor | `codigo/quantlab/` (cambios con test en `tests/`) |

**La raíz no recibe ficheros nuevos**, salvo los de entrada al repo, que ya están todos:
`README.md`, `EMPIEZA_AQUI.md`, `AVISO.md`, `LICENSE`, `CHANGELOG.md`, `EMPEZAR.bat`,
`VALIDAR.bat`, `empezar.sh`, `requirements*.txt`, `CLAUDE.md`, `.gitattributes`. No se añaden más.
`.vscode/extensions.json` solo recomienda Pixel Agents (`pablodelucca.pixel-agents`, MIT, de un
tercero): dibuja cada sesión de Claude Code como un personaje y los subagentes por separado. Es
opcional y el repo no depende de ella.

## Los .bat (trampas de cmd que ya costaron tiempo)
`EMPEZAR.bat` y `VALIDAR.bat` son la puerta de entrada de quien no programa. Tres cosas que hay que
respetar al tocarlos:
1. **`chcp 65001` rompe `set /p`.** Con la página de códigos UTF-8, `set /p` no lee nada. En
   `VALIDAR.bat` el `chcp` va justo antes de cada llamada a Python (que es donde hacen falta los
   acentos del RESUMEN), nunca arriba.
2. **Con `enabledelayedexpansion`, `echo [!]` se come el signo.** Por eso los errores se marcan
   `[ERROR]`.
3. **No basta con `where python`.** Windows trae un `python.exe` de 0 bytes en `WindowsApps` que
   solo abre la Microsoft Store y sale con 9009. La rutina `:probar` solo acepta un intérprete que
   imprima `42`; si no, el mensaje al usuario sería "tu Python es antiguo" cuando no hay Python.

Van con finales de línea CRLF (lo fija `.gitattributes`).

## Dependencias
`requirements.txt` es **solo el motor** (numpy, pandas, pyarrow, pytest): instala en ~40 s y con eso
corren los tests y `codigo/validar.py`. Streamlit, Plotly, matplotlib y `claude-agent-sdk` están en
`requirements-extra.txt` porque pesan y no hacen falta para validar. **Nada del núcleo puede
importar un paquete de los extra**; los módulos que sí lo hacen (`harness/grafo.py`,
`harness/dashboard.py`, `codigo/app/aed_ndx.py`, `codigo/scripts/05_charts_ndx.py`) son opcionales,
y sus tests usan `pytest.importorskip`.

## Reglas duras (para agentes y para sesiones interactivas)
1. Los criterios viven en `docs/MIS_REGLAS.md` (autoridad) y `docs/PROTOCOLO.md` (defaults).
   **Ningún agente los baja.** Solo la persona, en su fichero, anotando fecha y motivo.
2. **OOS se mira una vez.** Optimizar es cosa de IS. Un rechazo no autoriza a reoptimizar mirando OOS.
3. Costes dentro de cada métrica. No existen números brutos en los informes.
4. Cada agente escribe solo en sus carpetas (están en su `.md`). El validador no arregla; señala.
5. Cada turno de agente termina con `VEREDICTO: <X>` en la última línea, o el harness lo deja parado.
6. Los pasos verdes (hipótesis, criterio sobre el AED, sizing, deploy) no los decide ningún agente.
7. No leer `trades_oos.csv` ni `meseta.csv` al contexto: leer solo `RESUMEN.md`.
7b. **`trades_oos.csv` no se versiona nunca.** Lleva `precio_entrada` y `precio_salida`, o sea
   precios del proveedor de datos, y este repo es público. Está en `.gitignore`; el motor lo sigue
   escribiendo en local para quien corra sobre sus propias series. Lo que sí se versiona son las
   salidas agregadas sin precios: `meseta.csv`, `walk_forward.csv`, `metricas.csv`.
8. Sin push sin confirmación.
9. **Escribe para alguien que no programa.** La puerta de entrada es `EMPIEZA_AQUI.md`; el `README.md`
   es la referencia técnica. Cualquier cosa nueva cabe en un nivel: mirar sin instalar, correr el
   motor, o los agentes.
