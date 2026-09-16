# MINI FONDO — 4 agentes que validan estrategias como lo haría un fondo

Un repo que convierte una idea de trading en una estrategia validada (o en una descartada con
motivo escrito) usando **cuatro agentes de IA encadenados** y un motor de validación de cinco
fases. Tú pones la hipótesis y el criterio; ellos ponen el trabajo. Es el método **TIS
(Trade It Simple)** en 8 pasos, empaquetado para que lo corras en tu ordenador con Claude Code.

Incluye un ejemplo completo: la ruptura de canal con filtro de ruido de **Perry Kaufman** sobre
el Nasdaq, llevada de la hipótesis al veredicto. Spoiler: **se rechaza**, con un profit factor
OOS de 5.7. Si quieres entender por qué eso es lo correcto, este repo es para ti.

## Qué hay dentro

| Pieza | Qué hace |
|---|---|
| `.claude/agents/investigador.md` | Paso 02. Análisis exploratorio: ¿hay edge estructural o es ruido? |
| `.claude/agents/protocolo.md` | Paso 03. Convierte la hipótesis en reglas blanco o negro. |
| `.claude/agents/motor.md` | Pasos 04-07. Implementa, backtest IS/OOS, optimiza por meseta, robustez, sizing. |
| `.claude/agents/validador.md` | Cierre. Rehace los números, no se fía del motor. APROBADA o RECHAZADA. |
| `harness/` | Encadena los 4 agentes y se para en las dos puertas que solo cierra una persona. |
| `codigo/quantlab/` | El motor: ejecución realista, costes, métricas y las 5 fases de validación. |
| `codigo/validar.py` | Valida cualquier estrategia del repo sobre tus datos con un comando. |
| `docs/PROTOCOLO.md` | Los 8 pasos y los criterios numéricos. Solo los cambia la persona. |
| `estrategias/001_kaufman_breakout_er/` | El ejemplo: hipótesis, AED, reglas, informes, veredicto y bitácora. |

## Los 8 pasos

```
01 Hipótesis ──► 02 AED ──► [tu criterio] ──► 03 Reglas ──► 04 Backtest ──► 05 Optimización ──► 06 Robustez ──► 07 Sizing ──► [tu decisión] ──► 08 Deploy
   tú             IA           puerta            IA            IA               IA                 IA              IA propone      puerta            tú
```

Los pasos naranjas los hace la IA. Los verdes (hipótesis, criterio sobre el AED, sizing, deploy)
son tuyos y **ningún agente los decide**. Si la validación rechaza, el motor corrige lo señalado
y vuelve a intentarlo; como mucho tres veces. El OOS se mira una sola vez.

## Arranque en 5 minutos

```
git clone <este repo> && cd mini_fondo
python -m venv .venv && .venv\Scripts\activate        # Windows; en Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                                   # 11 tests, < 2 s: el motor funciona
python codigo/validar.py 001 --sintetico --rapido     # placebo: sobre ruido la regla NO debe pasar
```

Para el ejemplo con datos reales necesitas velas diarias del NDX (`fecha, open, high, low, close`)
en `data/` — no se incluyen por licencia. Después:

```
python codigo/validar.py 001 data/NDX_D1.csv --corte 2016-01-01
```

Para correr los agentes hace falta [Claude Code](https://claude.com/claude-code) con sesión iniciada:

```
python -m harness.run nueva 002 mi_idea      # crea la carpeta y la ficha de hipótesis
# rellena estrategias/002_mi_idea/hipotesis.md y deja tus datos en data/
python -m harness.run run 002                # investigador → se para en tu puerta
python -m harness.run ok 002                 # protocolo → motor → validador → se para en deploy
python -m harness.run status
```

Desde una sesión de Claude Code también puedes llamarlos a mano: `@investigador`, `@protocolo`,
`@motor`, `@validador`.

## El ejemplo: Kaufman sobre el Nasdaq

Ruptura del máximo de 40 días, solo si el tramo previo es limpio (Efficiency Ratio ≥ 0.3), salida
al perder el mínimo de 20 días, stop 3×ATR. Parámetros de Kaufman, sin optimizar. 2 pb por lado,
1 % de riesgo. IS 1985-2015, OOS 2016-2026 en índice cash **y** en CFD del broker.

| | IS | OOS cash | OOS CFD |
|---|---|---|---|
| trades | 93 | 24 | 23 |
| profit factor | 2.22 | 5.70 | 4.86 |
| MaxDD | −7.3 % | −4.8 % | −3.8 % |

Pasa la meseta, el walk-forward, Monte Carlo, costes ×2 y sin los dos mejores años. **Falla un
criterio: 24 trades OOS son menos de 30.** Y un solo criterio fallido es RECHAZADA. Un PF de 5.7 con
24 trades en la década más alcista del Nasdaq no es evidencia; es una década alcista. El AED ya lo
había avisado (permutación p = 0.28: el exceso sobre la base es deriva del índice).

Lo que **no** se hace: acortar el canal para fabricar trades ni bajar el umbral a 20. Lo que sí:
la misma regla sobre más índices, como hipótesis nueva. Está escrito en
`estrategias/001_kaufman_breakout_er/informe_validacion.md`.

## Reglas duras

1. Los criterios viven en `docs/PROTOCOLO.md`. Ningún agente los baja.
2. El OOS se mira una vez. Optimizar es cosa del IS.
3. Costes dentro de cada métrica. No existen números brutos.
4. Cada agente escribe solo en sus carpetas. El validador no arregla: señala.
5. Los pasos verdes no los decide ningún agente.

## Estructura

```
.claude/agents/     los 4 agentes (system prompt del harness y subagentes de Claude Code)
harness/            run.py (CLI) · grafo.py (fases y veredictos) · estado.py
docs/               PROTOCOLO.md · PLANTILLA_HIPOTESIS.md
codigo/quantlab/    motor de backtest, métricas, validación, informe
codigo/estrategias/ una señal por estrategia (≤30 líneas + PLAN)
codigo/validar.py   las 5 fases sobre tus datos
estrategias/<ID>/   hipótesis, informes, reglas, estado.json, bitácora
reportes/<ID>/      RESUMEN.md, meseta.csv, walk_forward.csv, trades_oos.csv
data/               tus velas (no se versionan)
tests/              humo + placebo
```

---
Mariel Lang · Trade It Simple. Método TIS. Este repo es un regalo: úsalo, rómpelo, cuéntame qué
descartaste y por qué.
