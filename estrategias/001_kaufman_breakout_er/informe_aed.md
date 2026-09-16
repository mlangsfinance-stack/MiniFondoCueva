# 001 · kaufman_breakout_er — Informe AED (paso 02)

Datos: NDX cash **solo IS** (1985-01-31 → 2015-12-31, 7 795 barras). Evento:
`close > maximo_previo(high, 40) & ER(10) >= 0.3`. Todo calculado con datos hasta el cierre de la
barra; `maximo_previo` excluye la barra actual. **n = 687 eventos.**

## Qué se midió
Retorno tras el evento a h barras frente al retorno incondicional (base) del mismo tramo;
probabilidad de superar el alto / romper el bajo de la barra del evento en 3 barras; test de
permutación (1 000 simulaciones) sobre el exceso a h=5 y h=10.

## Estudio de evento

| h | n | media | mediana | %pos | media_base | %pos_base | exceso | t_stat |
|---|---|---|---|---|---|---|---|---|
| 1 | 687 | 0.00077 | 0.00145 | 0.574 | 0.00060 | 0.542 | +0.00016 | 1.83 |
| 2 | 687 | 0.00165 | 0.00257 | 0.575 | 0.00121 | 0.543 | +0.00044 | 2.63 |
| 3 | 687 | 0.00213 | 0.00297 | 0.575 | 0.00179 | 0.558 | +0.00034 | 2.80 |
| 5 | 687 | 0.00378 | 0.00574 | 0.611 | 0.00296 | 0.566 | +0.00083 | 3.83 |
| 10 | 687 | 0.00754 | 0.00911 | 0.606 | 0.00583 | 0.577 | +0.00171 | 5.16 |
| 20 | 687 | 0.01510 | 0.01281 | 0.616 | 0.01176 | 0.608 | +0.00333 | 7.15 |

- Rango a h=3: p(supera alto) **0.882** vs base 0.713 · p(rompe bajo) 0.445 vs base 0.619.
- Permutación (n_sim = 1 000): h=5 media 0.00378 vs azar 0.00297 → **p = 0.277**; h=10 → p = 0.176.

## Qué apoya la hipótesis
El exceso es positivo en todos los horizontes y crece con h, como toca a una continuación. El
evento sí "mueve" el rango: el 88 % de las veces se supera el alto de la barra en 3 días.

## Qué la contradice
El t-stat de la tabla es contra cero, no contra la base, y el NDX tiene una deriva de +0.30 % a 5
días: casi todo ese t es deriva. El contraste honesto es la permutación, y dice que un exceso de
+0.08 % a 5 días se obtiene eligiendo 687 días al azar el 28 % de las veces. Exceso 2× el coste de
ida y vuelta: por debajo del 3× exigido y del +0.15 % predicho en la hipótesis.

## Lectura
El filtro ER no añade un edge medible a 5-10 días sobre la base del propio índice. Lo que hay es la
deriva del NDX más una forma de entrar que no la estropea. Se cumplen n ≥ 100, exceso > 0 en
horizontes consecutivos y |t| ≥ 2, pero el criterio que manda (permutación, p ≤ 0.05) no pasa.
Se llevó a reglas y motor como **test inicial del pipeline**, marcado como tendencia débil, para
que la validación completa dijera la última palabra.

VEREDICTO: NO_EDGE
