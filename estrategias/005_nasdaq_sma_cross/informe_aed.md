# 005 · nasdaq_sma_cross — Informe AED (paso 02)

**Agente:** investigador · **Fecha:** 2026-09-15 · **Código:** `codigo/exploratorio_005.py`
**Datos:** `data/NDX_D1.csv`, 4 805 velas D1 (2008-08-06 → 2026-07-31). **Solo IS:** < 2021-01-01 → 3 362 velas.
OOS (2021-2026) **no se ha mirado**.

## 0. Qué dice la hipótesis y qué he medido

La hipótesis afirma que, en NDX diario, el retorno medio con SMA rápida > SMA lenta es **claramente superior**
al retorno con SMA rápida < SMA lenta y a la base incondicional, en la mayoría de años, y que el efecto vive en
un rango amplio de longitudes (rápida 20-100, lenta 100-300). Ella misma fija lo que la mataría: que sea solo la
deriva alcista o que dependa de 1-2 años.

He medido el fenómeno **crudo**, sin reglas: señal = estado de las SMAs al cierre de t-1, retorno = log(close_t/close_{t-1}).
Rejilla de 29 pares (rápida ∈ {10,20,30,50,75,100} × lenta ∈ {100,150,200,250,300}). Par de referencia para tablas
detalladas: 50/200. El periodo de calentamiento de la SMA lenta (hasta ~2009-05 para 200) se trata como "sin señal",
no como "abajo" — si se cuenta como "abajo" el crash de 2008 infla artificialmente lo malo que parece "abajo".

## 1. Base incondicional (IS)

| | valor |
|---|---|
| Retorno medio diario | **+5.7 bp** (t = 2.41) |
| Std diaria | 137 bp |
| Anualizado | +14.4 % · Sharpe 0.66 |
| Días positivos | 55.4 % |
| Peor día | −11.2 % |

Años negativos: 2008 (parcial, −45 %) y 2018 (−0.7 %). El resto positivos. La deriva alcista es fuerte.

## 2. Rejilla: arriba vs abajo vs base (retorno medio diario, bp)

| rápida/lenta | % tiempo arriba | arriba | abajo | base | spread (arriba−abajo) | t spread |
|---|---|---|---|---|---|---|
| 10/100 | 78 % | 5.0 | 15.6 | 5.7 | −10.6 | −1.55 |
| 20/100 | 79 % | 4.9 | 16.3 | 5.7 | −11.5 | −1.78 |
| 20/200 | 85 % | 4.8 | 20.6 | 5.7 | −15.8 | −2.19 |
| 30/200 | 86 % | 5.8 | 14.9 | 5.7 | −9.1 | −1.29 |
| 50/150 | 81 % | 6.1 | 13.7 | 5.7 | −7.6 | −1.24 |
| **50/200** | 86 % | 5.7 | 16.3 | 5.7 | **−10.6** | −1.49 |
| 75/150 | 82 % | 6.9 | 10.1 | 5.7 | −3.2 | −0.54 |
| 75/300 | 91 % | 6.2 | 10.6 | 5.7 | −4.4 | −0.65 |
| 100/200 | 85 % | 6.2 | 12.2 | 5.7 | −6.0 | −1.05 |
| 100/300 | 92 % | 6.2 | 10.6 | 5.7 | −4.4 | −0.62 |

**Resumen de los 29 pares:**
- Spread arriba−abajo **> 0 en 0 de 29 pares**. Mediana −10.6 bp, t mediano −1.44, mínimo −2.79.
- "Arriba" supera la base en 13/29 pares, y cuando lo hace es por **0.1-1.2 bp/día** (frente a una std de 115 bp): indistinguible de cero.
- "Abajo" tiene retorno medio **negativo en 0 de 29 pares**. Es siempre positivo y de hecho **2-5× mayor** que "arriba".

Lo que la hipótesis predice como "peores" son, en IS, los mejores días del índice. La razón es mecánica: en NDX
2009-2020 las correcciones fueron en V; la SMA rápida cruza abajo cuando la caída ya ha ocurrido y el estado
"abajo" coincide con el rebote. Los tramos "abajo" duran de media 48 días (mediana 41) frente a 304 arriba.

## 3. ¿Es solo la deriva alcista? Filtro vs largo siempre (mismo periodo, sin costes)

| rápida/lenta | acum. filtro | acum. largo | vol filtro | vol largo | Sharpe filtro | Sharpe largo | captura días + | captura días − |
|---|---|---|---|---|---|---|---|---|
| 20/100 | 1.25 | 2.39 | 15.6 % | 19.6 % | 0.62 | 0.94 | 69 % | 72 % |
| 50/200 | 1.55 | 2.25 | 17.0 % | 18.9 % | 0.73 | 0.95 | 82 % | 85 % |
| 75/150 | 1.82 | 2.41 | 16.8 % | 19.1 % | 0.85 | 0.99 | 79 % | 80 % |
| 100/300 | 1.74 | 2.01 | 18.2 % | 18.9 % | 0.79 | 0.88 | 91 % | 92 % |

- El filtro acumula **menos que largo siempre en 29/29 pares** y tiene **peor Sharpe en 29/29 pares**.
- Captura simétrica: el filtro se come la misma fracción de días negativos que de positivos (85 % vs 82 % en 50/200).
  No hay asimetría: **no evita las caídas más de lo que evita las subidas**.
- De los 20 peores días del periodo, el filtro 50/200 está **dentro en 17** (20/100: en 16). La protección frente a
  crashes que se le presupone al cruce de medias no aparece en este activo y periodo.

(Nota: si se compara desde 2008-08 contando el calentamiento como "fuera", el filtro parece ganar en Sharpe en 2/3 de los
pares. Es un artefacto: se le regala estar fuera del crash de 2008 antes de que existiera la señal. Con el mismo periodo
para ambos, desaparece.)

## 4. Estabilidad por año (50/200)

| año | % arriba | arriba bp | abajo bp | base bp | spread bp | filtro acum | largo acum |
|---|---|---|---|---|---|---|---|
| 2009* | 96 % | 15.9 | 127.3 | 20.1 | −111 | 0.24 | 0.32 |
| 2010 | 74 % | 1.2 | 17.6 | 5.5 | −16 | 0.03 | 0.17 |
| 2011 | 72 % | −1.7 | 7.9 | 1.0 | −10 | −0.04 | 0.03 |
| 2012 | 92 % | 5.7 | −8.9 | 4.5 | **+15** | 0.16 | 0.14 |
| 2013 | 94 % | 10.4 | 28.2 | 11.4 | −18 | 0.27 | 0.31 |
| 2014 | 100 % | 6.5 | — | 6.5 | — | 0.17 | 0.17 |
| 2015 | 86 % | −2.2 | 36.1 | 3.2 | −38 | −0.05 | 0.08 |
| 2016 | 70 % | −2.2 | 12.8 | 2.2 | −15 | −0.04 | 0.06 |
| 2017 | 100 % | 10.6 | — | 10.6 | — | 0.27 | 0.27 |
| 2018 | 92 % | 3.3 | −42.9 | −0.3 | **+46** | 0.08 | −0.01 |
| 2019 | 75 % | 8.1 | 25.7 | 12.6 | −18 | 0.16 | 0.32 |
| 2020 | 93 % | 12.8 | 44.1 | 15.0 | −31 | 0.31 | 0.39 |

\* 2009 empieza en mayo (calentamiento).

- Spread > 0 en **2 de 10 años** con ambos regímenes (2012 y 2018). "Arriba" > base en 2/12. Filtro ≥ largo en 4/12 (dos son empates por estar 100 % arriba).
- **En toda la rejilla**, por año: la mediana del spread es negativa en 10 de 11 años con datos; el único año donde la
  mayoría de pares tiene spread positivo es **2018** (91 % de pares). 2018 es el único año donde el cruce hizo lo que promete:
  salir antes de la caída de Q4. Un año de doce.

## 5. ¿Qué lo mata? (50/200)

| prueba | spread bp | t |
|---|---|---|
| Completo | −10.6 | −1.49 |
| Jackknife (quitando cada año, rango) | −8.1 … −13.3 | −1.07 … −1.91 |
| Sin los 2 años que más aportan (2012, 2018) | −15.1 | −2.05 |
| Sin 2008-2009 | −9.6 | −1.35 |
| Sin 2020 | −10.1 | −1.42 |
| Sin 2008, 2009 y 2020 | −9.1 | −1.28 |

No hay ningún año cuya eliminación cambie el signo. Lo que sí depende de 1-2 años es lo poco favorable que hay:
quitando 2012 y 2018 el spread se va a −15 bp con t = −2.05. El resultado no es frágil; es **robustamente contrario** a la hipótesis.

**Placebo** (2 000 rotaciones circulares de la señal sobre los retornos, que conservan la autocorrelación de ambas series):

| par | spread real | placebo p95 | p-valor | Sharpe filtro real | placebo media | p-valor |
|---|---|---|---|---|---|---|
| 50/200 | −10.6 bp | +11.3 bp | 0.99 | 0.73 | 0.88 | 0.94 |
| 20/100 | −11.5 bp | +7.9 bp | 0.999 | 0.62 | 0.84 | 0.98 |

Una señal colocada al azar con la misma exposición (86 % del tiempo dentro) captura **más** retorno y **más** Sharpe que el
cruce real en el 94-99 % de los casos. El cruce no está eligiendo días al azar: está eligiendo sistemáticamente
*peor* que el azar, porque sale justo cuando el rebote empieza.

## 6. Eventos de cruce (50/200: 9 cruces arriba, 8 abajo en 11.5 años)

| horizonte | fwd tras cruce ↑ (bp) | % pos | fwd tras cruce ↓ (bp) | % pos | base fwd % pos |
|---|---|---|---|---|---|
| 5 d | +44 | 78 % | +17 | 50 % | 60 % |
| 20 d | +274 | 89 % | +378 | 63 % | 67 % |
| 60 d | +516 | 89 % | +883 | 100 % | 76 % |
| 120 d | +1 104 | 89 % | +1 274 | 100 % | 81 % |

Tras el cruce a la baja, el índice sube a 60 y 120 días en **8 de 8** casos y más que tras el cruce al alza. Con n = 8-9
esto no es estadística, pero apunta en la misma dirección que todo lo anterior: en este activo y periodo el cruce bajista
fue una señal de compra, no de venta.

## 7. Régimen de volatilidad (terciles vol 20d, 50/200)

| vol | % arriba | arriba bp | abajo bp | base bp | spread |
|---|---|---|---|---|---|
| baja | 95 % | 3.9 | 7.6 | 4.1 | −3.6 |
| media | 92 % | 4.1 | 6.1 | 4.3 | −2.0 |
| alta | 72 % | 10.0 | 20.8 | 12.9 | −10.8 |

Spread negativo en los tres. Casi toda la varianza del filtro está en vol alta, donde "abajo" rinde 21 bp/día. El filtro
lo que hace es **estar fuera en vol alta** (28 % del tiempo), y en NDX 2009-2020 la vol alta pagó.

## 8. ¿Aporta la media rápida? Precio > SMA lenta (1 parámetro)

| regla | % arriba | arriba | abajo | spread | t | cruces |
|---|---|---|---|---|---|---|
| close > SMA100 | 78 % | 4.2 | 18.7 | −14.5 | −2.00 | 151 |
| close > SMA200 | 86 % | 5.6 | 16.1 | −10.5 | −1.14 | 88 |
| close > SMA300 | 91 % | 4.9 | 23.0 | −18.1 | −1.51 | 62 |

Mismo cuadro con un parámetro menos. La media rápida solo reduce el número de cruces (17 vs 88); no cambia el signo.

## 9. Costes

Precio mediano IS 3 799 → 5 puntos ida y vuelta = **13 bp por operación**. Con 0.6-3.8 cruces/año el coste total es el
0.4-3.2 % de lo acumulado: los costes **no** son lo que mata la hipótesis. El exceso frente a largo siempre es negativo
en 29/29 pares antes de costes (−0.10 a −0.84 en log-retorno acumulado sobre ~11.5 años).

## 10. Qué apoya la hipótesis / qué la contradice

**Apoya (poco):**
- El índice tiene deriva alcista fuerte y persistente (t = 2.4, 11/13 años positivos). Existe la tendencia plurianual.
- En 2018 el cruce hizo exactamente lo que promete. En 2012, marginalmente.
- Sharpe de los días "arriba" > Sharpe base en 22/29 pares — pero por una décima, y desaparece cuando se compara
  el filtro completo con largo siempre en el mismo periodo.

**Contradice (mucho):**
- Spread arriba−abajo negativo en **29/29 pares**, en **10/11 años** (mediana rejilla), en los **3 regímenes de vol**, con y sin 2008-09-20.
- "Abajo" nunca es negativo; es el estado con mejores retornos por día (rebotes en V).
- El filtro pierde frente a largo siempre en retorno **y** en Sharpe en 29/29 pares. No captura asimétricamente las caídas (está dentro en 17 de los 20 peores días).
- Placebo: una señal aleatoria con la misma exposición lo hace mejor el 94-99 % de las veces.
- Con un solo parámetro (precio vs SMA lenta) el resultado es idéntico: el fenómeno no está en el cruce.

**Lo que la propia hipótesis dijo que la mataría, ambas cosas ocurren:** el "edge" es la deriva alcista y largo siempre no
solo lo iguala, lo supera; y lo poco favorable (2 años de 12) es exactamente la dependencia de 1-2 años que se avisaba.

## 11. Lectura honesta

En NDX diario 2009-2020 el cruce de medias no separa días buenos de días malos: separa días normales de días de rebote,
y se queda con los normales. La razón estructural que da la hipótesis (momentum de flujos pasivos) sí existe como
deriva del índice, pero se la lleva entera quien está siempre largo; el cruce no la amplifica, la recorta. Lo que sí
hace el filtro es bajar la volatilidad (de 19 % a 16-17 %), pero a un coste en retorno que deja el Sharpe peor que el de
largo siempre y peor que el de una señal colocada al azar. Un solo año (2018) muestra el comportamiento buscado. No
descarto que en un periodo con mercados bajistas largos (2000-2002 estilo) el cruce proteja; pero ese periodo no está en
los datos y en el que sí está, doce años de IS con 29 combinaciones de parámetros, el signo es siempre el contrario al
predicho. Esto no es ambiguo ni es ruido con sesgo positivo: es ruido con sesgo negativo. Si Mariel quiere seguir con
la idea de tendencia en NDX, la premisa a reescribir sería otra (p. ej. "estar largo siempre y gestionar solo el tamaño
por vol", o cruces en horizontes mucho más largos con un objetivo de reducción de drawdown, no de retorno), pero no es
esta.

VEREDICTO: NO_EDGE
