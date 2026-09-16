# 05 — Métricas: una definición, un sitio

Todas se calculan en `quantlab.metrics.metricas` a partir de la lista de trades y la curva de
equity del motor. No hay otra implementación. Si una métrica no está aquí, no se usa en una puerta.

| Métrica | Definición | Para qué sirve | Ojo |
|---|---|---|---|
| `n_trades` | nº de operaciones cerradas | significación; < 30 no dice nada, < 100 poco | contar por activo si es multi-mercado |
| `profit_factor` | Σ ganancias / Σ pérdidas | resumen de expectativa robusto a escala | inflado por 1–2 trades; ver `pf_sin_mejor` |
| `pf_sin_mejor` | PF quitando el mejor trade | detectar dependencia de un outlier | si cae < 1, el edge era un trade |
| `win_rate` | % trades con PnL > 0 | describir el perfil (no juzga) | 35 % con payoff 2.5 es mejor que 60 % con 0.6 |
| `payoff` | ganancia media / pérdida media | describir el perfil | — |
| `expectancia_R` | media de PnL / riesgo inicial | edge por unidad de riesgo, comparable entre estrategias | > 0.1 R es aceptable; > 0.3 R sospechoso |
| `t_stat` | media PnL / desv PnL × √n | ¿el PnL medio es distinto de 0? | > 2 mínimo; con muchos tests, > 3 |
| `retorno_total`, `cagr` | sobre el equity compuesto | escala del resultado | depende del sizing; no compara estrategias |
| `max_dd` | mínima caída desde máximo de equity | dolor; base de sizing y retirada | un solo camino; el MC da la distribución |
| `mar` | CAGR / \|MaxDD\| | rentabilidad por unidad de dolor | > 0.5 razonable, > 1 bueno |
| `sharpe` | media / desv de retornos diarios × √252 | comparar con otras estrategias y activos | penaliza volatilidad buena; útil, no sagrado |
| `trades_anio` | n_trades / años | ritmo; informa del tiempo de incubación necesario | — |
| `media_barras` | duración media | coherencia con la hipótesis (horizonte) | si difiere del horizonte de la tendencia, algo no cuadra |
| `pct_stop` | % de salidas por stop | ¿el stop trabaja o estorba? | > 50 % suele indicar stop demasiado ceñido |

## Validación (`quantlab.validation`)

| Métrica | Definición |
|---|---|
| eficiencia WF | media de CAGR OOS por ventana / media de CAGR IS por ventana |
| % ventanas positivas | ventanas WF con CAGR OOS > 0 / total |
| meseta: caída | 1 − mín(vecinos 3×3) / centro, sobre PF |
| MC p5 retorno | percentil 5 del retorno final tras permutar el orden de los trades |
| MC p95 DD | percentil 95 del MaxDD tras permutar |
| MC ruina | % de simulaciones con DD ≥ `mc_ruina_dd` (35 %) |

## Tendencia (`quantlab.tendencies`)

| Métrica | Definición |
|---|---|
| exceso | retorno medio fwd tras el evento − retorno medio fwd incondicional |
| t_stat (evento) | media / desv × √n del retorno fwd condicional |
| p_supera_alto | % de eventos en que el alto previo se supera en h barras (vs base) |
| p_valor permutación | % de muestras aleatorias de n barras con media ≥ la observada |
