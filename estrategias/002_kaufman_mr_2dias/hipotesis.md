# H003 — Reversión de 2 días a favor de la tendencia de largo plazo (NDX, ambos lados)

- **Fecha:** 2026-09-15
- **Fuente:** literatura — Kaufman, *Trading Systems and Methods* (5ª ed., 2013): cap. 15 "Pattern
  Recognition" (secuencias de días consecutivos al alza/baja y su reversión) y cap. 16 "Day Trading"
  / mean reversion de corto plazo en índices; Kaufman, *Kaufman Constructs Trading Systems* (2020),
  sección de "mean reversion" en índices de acciones: comprar tras cierres consecutivos a la baja
  cuando el precio está por encima de la media de largo plazo, mantener pocos días. Emparenta con
  la evidencia académica de reversión a corto plazo en índices (autocorrelación negativa diaria
  desde los 90).
- **Familia de edge:** reversión (corto plazo) + filtro de régimen (SMA200 = tendencia de fondo)
- **Estado:** descartada(prototipo IS: PF 1.05, t 0.67; validación confirma: F1 Darwinex, F3, F5)
- **Tests acumulados sobre esta hipótesis:** 4 (tendencia IS con dos eventos · prototipo IS ·
  H003.1 prototipo IS solo largo, informativo · validación 5 fases)

## 1. Observación
En los índices de acciones desde los años 90, dos cierres consecutivos en contra de la tendencia de
fondo (dos bajadas seguidas en mercado alcista) tienden a ser seguidos de un rebote en 1–3 sesiones.
Lo simétrico (dos subidas en mercado bajista) da caídas, aunque con menos consistencia porque los
rebotes bajistas son violentos.

## 2. Mecanismo
Conductual (sobre-reacción de corto plazo) + estructural: en un mercado alcista, dos días de venta
suelen ser liquidación de corto plazo (rebalanceo, hedging, stops) que no cambia la tendencia y que
los compradores estructurales (flujos pasivos, "buy the dip") absorben rápido. El filtro SMA200
distingue "retroceso en tendencia" de "inicio de caída". Kaufman advierte que la reversión de índices
es un edge de retorno pequeño por trade: vive o muere por costes y por el stop.

## 3. Universo y timeframe
NDX diario (Norgate IS; Norgate y Darwinex OOS). Se espera en índices amplios de EEUU (SP500,
NDX) desde ~1990. NO se espera en materias primas ni divisas (allí domina la continuación) ni en
el propio NDX antes de 1990 (menor participación institucional). El lado corto se espera más débil.

## 4. Evento
```
sma = sma(close, 200)
baja2 = (close < close.shift(1)) & (close.shift(1) < close.shift(2))
sube2 = (close > close.shift(1)) & (close.shift(1) > close.shift(2))
evento_largo = baja2 & (close > sma)
evento_corto = sube2 & (close < sma)
```
Solo cierres; sin look-ahead.

## 5. Predicción falsable
Largo: tras el evento, el retorno a 1, 2 y 3 barras es mayor que el incondicional. Horizonte
principal: h = 2 (coincide con `hold`). Magnitud esperada: exceso ≥ +0.12 % a h=2 (≥ 3× el coste
de ida y vuelta de 0.04 %). Corto: retorno a h=2 menor que el incondicional (exceso ≤ −0.12 %).

## 6. Métrica que decide
`estudio_evento`: exceso y t-stat a h=2 (y a h=1, 3 como confirmación); `test_permutacion` a h=2
(n_sim=1000). Para el corto, el p-valor se calcula sobre el retorno con signo invertido.
`prob_rango` h=2 como apoyo.

## 7. Criterio de muerte (escrito ANTES de correr nada)
Por lado: n < 100 · exceso ≤ 0 (largo) / ≥ 0 (corto) a h=2 · no hay 2 horizontes consecutivos
con exceso del signo esperado · |t| < 2 · p-valor > 0.05. Si el corto muere y el largo vive, la
señal pasa a prototipo solo con el largo y se anota como variante (H003.1). No se toca sma_n ni
el número de días para que pase. Prototipo muere si PF ≤ 1.2, n < 100, expectancia ≤ 0.1 R o
t ≤ 2 en IS con costes.

## 8. Coste esperado
0.04 % ida y vuelta. Exceso esperado 0.12 % a h=2. Ratio 3×: es el mínimo admisible. Este edge es
sensible a costes por construcción; el stress de costes ×2 será la fase que más le cueste.

---

## Resultado del test de tendencia
2026-09-15 · datos: `data/ndx_norgate_d1.parquet` **solo IS** (1985-01-31 → 2015-12-31, 7.795 barras).

**Evento largo** `baja2 & close > SMA200` · n = 1.081

| h | n | media | mediana | %pos | media_base | %pos_base | exceso | t_stat |
|---|---|---|---|---|---|---|---|---|
| 1 | 1080 | 0.00053 | 0.00109 | 0.535 | 0.00060 | 0.542 | −0.00008 | 1.06 |
| 2 | 1080 | 0.00217 | 0.00255 | 0.556 | 0.00121 | 0.543 | +0.00096 | 3.18 |
| 3 | 1080 | 0.00273 | 0.00357 | 0.564 | 0.00179 | 0.558 | +0.00094 | 3.48 |
| 5 | 1079 | 0.00405 | 0.00567 | 0.585 | 0.00296 | 0.566 | +0.00110 | 4.05 |
| 10 | 1078 | 0.00724 | 0.00710 | 0.588 | 0.00583 | 0.577 | +0.00141 | 5.32 |

- `prob_rango` h=2: p_supera_alto 0.474 vs base 0.651 · p_rompe_bajo 0.698 vs base 0.562
  (el día siguiente sigue cayendo más veces de lo normal: la reversión no es inmediata).
- `test_permutacion` n_sim=1000: h=2 media 0.00217 vs azar 0.00122 → **p = 0.071**; h=5 → p = 0.127.

**Evento corto** `sube2 & close < SMA200` · n = 458

| h | n | media | mediana | %pos | media_base | %pos_base | exceso | t_stat |
|---|---|---|---|---|---|---|---|---|
| 1 | 458 | 0.00056 | 0.00080 | 0.524 | 0.00060 | 0.542 | −0.00005 | 0.61 |
| 2 | 458 | −0.00031 | 0.00121 | 0.526 | 0.00121 | 0.543 | −0.00151 | −0.23 |
| 3 | 458 | −0.00063 | 0.00420 | 0.563 | 0.00179 | 0.558 | −0.00242 | −0.39 |
| 5 | 458 | 0.00041 | 0.00404 | 0.531 | 0.00296 | 0.566 | −0.00255 | 0.19 |
| 10 | 458 | 0.00221 | 0.00800 | 0.581 | 0.00583 | 0.577 | −0.00362 | 0.79 |

- `prob_rango` h=2: p_supera_alto 0.742 vs base 0.651 · p_rompe_bajo 0.434 vs base 0.562.
- `test_permutacion` sobre el retorno con signo invertido, n_sim=1000: h=2 → **p = 0.052**; h=5 → p = 0.020.

Lectura: el largo tiene exceso positivo a h=2..10 (+0.10 % a h=2, justo debajo del +0.12 %
predicho) pero el t de `estudio_evento` es contra cero y el NDX lleva deriva; la permutación da
p=0.071, no significativo al 5 %. A h=1 el exceso es negativo: la caída continúa un día más. El
corto tiene exceso del signo correcto (−0.15 % a h=2) pero |t| < 1 y mediana positiva: unos
pocos días de caída fuerte lo explican todo; mecanismo asimétrico como se anticipó en §1.

## Decisión
**Puerta de tendencia: NO pasa** en ninguno de los dos lados (largo p=0.071, |t| ok pero por
deriva; corto |t|=0.23 < 2, p=0.052). Se lleva al prototipo con AMBOS lados tal como está definida
(sin quitar el corto: hacerlo sería variante H003.1 y no queremos buscar), marcada como
**tendencia débil**. Un solo test, dos eventos; ninguna variante.

## Prototipo IS (2026-09-15, Norgate < 2016, coste 2 pb/lado, riesgo 1 %, stop 2×ATR14)
n = 948 · PF 1.05 · expectancia 0.014 R · t = 0.67 · win 55 % · payoff 0.88 · 13.5 % stops ·
CAGR 0.4 % · MaxDD −17.9 % · años positivos 17/31 (55 %). Largos 690 trades (+20.4 k), cortos 258
(−7.9 k). Puerta de prototipo: **no pasa** (PF, expectancia y t).
H003.1 (informativo, solo largos, IS): n = 690 · PF 1.12 · exp 0.03 R · t = 1.26. Tampoco pasa.

## Validación (2026-09-15, `reportes/002_kaufman_mr_2dias/RESUMEN.md`, --rapido)
**DESCARTADA.** Fallan: `pf_oos_darwinex` 1.23 < 1.3 · `meseta_min_vecino` 0.86 < 1.2 (IS) ·
`stress_sin_2_mejores_anios_pf` 1.09 < 1.1 · `stress_peor_tercio_pf` 0.95 < 1.1.
Pasan: PF OOS Norgate 1.35 (justo fuera de la frontera 1.25–1.35), 282 trades OOS, MaxDD OOS −8.9 %,
WF 0.65 / 3 de 5 ventanas, costes ×2 PF 1.28. Curioso: OOS (2016+) mejor que IS (1985-2015).

## Decisión final
Descartada en prototipo (IS) y confirmada en validación. El edge de reversión de 2 días en el NDX
es del tamaño del coste (+0.10 % a 2 días vs 0.04 % de ida y vuelta) y no se sostiene en 1985-2015:
peor tercio (1985-1995) PF 0.95. El lado corto resta. El OOS 2016+ es mejor (PF 1.35) pero con IS
plano no es evidencia sino régimen. Aprendido: en índice cash diario, la reversión de corto plazo de
Kaufman necesita o bien un filtro de régimen distinto de la SMA200 (volatilidad, época) o un
timeframe intradía; no se refina aquí. Si se retoma será hipótesis nueva (H003.2) con test de
tendencia previo restringido a 1995+ y formulado antes de mirar nada más.
