# 006 · nasdaq_overnight — Informe AED (paso 02)

**Agente:** investigador · **Fecha:** 2026-09-15
**Datos:** `data/NDX_D1.csv`, solo IS (2008-08-06 → 2020-12-31, 3 362 velas). OOS (≥ 2021-01-01) no se ha mirado.
**Código:** `codigo/exploratorio_006.py` (ejecutar con `.venv/Scripts/python`).
**Costes de la hipótesis:** 1.5 pts spread + 1 pt slippage por lado = **5 puntos ida y vuelta**.

## Qué medí

Sin reglas de trading. Tres tramos por vela, en retorno simple y en puntos:

| Tramo | Definición |
|---|---|
| overnight | `open[t+1] / close[t] − 1` (lo que la hipótesis quiere capturar) |
| intradía | `close[t] / open[t] − 1` (la base contra la que se compara) |
| close-close | `close[t+1] / close[t] − 1` (deriva total del índice) |

Y sobre el overnight: media, mediana, t-stat, % de noches positivas, comparación con costes, estabilidad por año, ventanas rodantes de 2 años, mitades del IS, recorte de mejores noches/años, día de la semana, régimen (SMA200, terciles de volatilidad), autocorrelación y anatomía del gap en puntos.

## Hallazgo previo que condiciona todo: qué es «open» y «close» en esta vela

Antes de medir el efecto miré si el gap `close[t] → open[t+1]` es un gap de mercado real. No lo es:

| Medida | Valor |
|---|---|
| Mediana de \|gap overnight\| | **1.0 pts** |
| Mediana del rango high-low de la vela | 46.5 pts |
| Mediana \|gap\| / rango | **0.029** |
| Std overnight vs std intradía | 0.41 % vs 1.30 % |
| Varianza overnight / varianza close-close | **0.09** |
| Velas en domingo | 211 |

El CFD de Darwinex cotiza prácticamente 24 h. El «open» y el «close» de la vela D1 son el primer y el último tick alrededor de la medianoche del servidor, separados por el descanso de rollover (~1 h), **no** la subasta de apertura (9:30 ET) ni la de cierre (16:00 ET) del Nasdaq cash. El overnight real del índice US (16:00 → 9:30 ET del día siguiente) queda **dentro** del tramo que aquí llamamos «intradía». Con estos datos no se puede medir el fenómeno que describe la hipótesis; lo que se mide es el gap de rollover del CFD.

## Lo que sale con la definición de la hipótesis (aun así, medido)

### Retorno por tramo — IS completo

| Tramo | n | media | mediana | std | t | % pos | suma |
|---|---|---|---|---|---|---|---|
| **overnight** | 3 361 | **−0.0275 %** | −0.0074 % | 0.41 % | **−3.87** | **35.0 %** | **−92.3 %** |
| intradía | 3 362 | +0.0943 % | +0.1135 % | 1.30 % | +4.21 | 56.5 % | +317.0 % |
| close-close | 3 361 | +0.0665 % | +0.1061 % | 1.37 % | +2.81 | 55.4 % | +223.5 % |

Diferencia pareada overnight − intradía: −0.122 % por día, t = −5.16. Es **lo contrario** de lo que la hipótesis predice, y con significación.

### Frente a costes (el punto crítico según la propia hipótesis)

| Medida | Valor |
|---|---|
| Gap overnight medio | **−1.28 pts** (bruto, ya negativo) |
| Coste ida y vuelta | 5.0 pts |
| Gap medio neto | −6.28 pts (t = −25.5) |
| % noches con gap > 5 pts | 6.7 % |
| Suma IS bruto / coste total / neto | −4 292 / 16 805 / **−21 097 pts** |
| Suma IS en % (overnight neto) | **−629 %** frente a +317 % del intradía |

No hay año en que el overnight neto de costes sea positivo (0/13). Ni siquiera el bruto lo es en la mayoría (4/13 años con suma > 0, y esos cuatro suman entre +0.1 % y +3.4 %).

### Estabilidad por año

| Año | n | over media | intra media | over suma | intra suma | % noches pos | t over |
|---|---|---|---|---|---|---|---|
| 2008 | 103 | −0.180 % | −0.175 % | −18.6 % | −18.0 % | 42.7 | −1.05 |
| 2009 | 255 | −0.034 % | +0.216 % | −8.5 % | +55.2 % | 7.8 | −1.09 |
| 2010 | 307 | −0.007 % | +0.070 % | −2.2 % | +21.6 % | 46.6 | −0.37 |
| 2011 | 307 | +0.000 % | +0.024 % | +0.1 % | +7.2 % | 55.4 | +0.02 |
| 2012 | 311 | +0.005 % | +0.047 % | +1.7 % | +14.7 % | 42.4 | +0.42 |
| 2013 | 273 | −0.006 % | +0.111 % | −1.5 % | +30.3 % | 44.7 | −1.09 |
| 2014 | 259 | +0.002 % | +0.069 % | +0.4 % | +17.9 % | 50.2 | +0.31 |
| 2015 | 259 | −0.026 % | +0.062 % | −6.6 % | +16.1 % | 47.5 | −2.68 |
| 2016 | 258 | −0.073 % | +0.101 % | −18.7 % | +26.1 % | 16.7 | −9.98 |
| 2017 | 256 | −0.058 % | +0.165 % | −14.8 % | +42.4 % | 9.0 | −9.46 |
| 2018 | 258 | +0.013 % | −0.008 % | +3.4 % | −1.9 % | 20.9 | +0.47 |
| 2019 | 257 | −0.052 % | +0.183 % | −13.3 % | +47.1 % | 20.6 | −3.89 |
| 2020 | 258 | −0.052 % | +0.226 % | −13.5 % | +58.4 % | 46.7 | −2.15 |

Overnight > intradía en **1 de 13** años (2018, y por −1.9 % vs +3.4 %: los dos casi planos).

### Pruebas de muerte

| Prueba | Resultado |
|---|---|
| Sin los 2 mejores años overnight (2018, 2012) | media −0.035 %, t = −4.36, suma −97 % |
| Sin 2 mejores ni 2 peores años | media −0.025 %, suma −60 % (intradía mismo subset +296 %) |
| Sin las 20 mejores noches | media −0.044 %, t = −7.5 |
| Winsorizado 1 %/99 % | media −0.028 %, t = −5.8 |
| 1ª mitad IS (2008-08 → 2014-06) | over media −0.017 %, t = −1.36 |
| 2ª mitad IS (2014-06 → 2020-12) | over media −0.038 %, t = −5.87 |
| Ventanas rodantes de 2 años | 12 ventanas: 10 negativas, 2 con media ≈ 0 (2011-12, 2012-13). Ninguna con overnight neto > 0 |
| Régimen alcista (close > SMA200) | over media −0.021 %, t = −5.8 (intradía +0.136 %) |
| Régimen bajista | over media −0.018 %, t = −0.83 |
| Terciles de volatilidad | −0.024 % / −0.018 % / −0.039 % (baja / media / alta): negativo en los tres |
| Día de la semana | lunes +0.016 % (t = 0.95, no significativo); martes a viernes −0.03 a −0.05 % (t entre −2.2 y −2.8). Ningún día supera los costes |
| Autocorrelación overnight lag 1-5 | −0.06, −0.01, −0.02, −0.04, +0.03: nada explotable |
| Overnight condicionado al signo del intradía | ambos negativos (−0.016 % / −0.032 %) |

No hay filtro simple (régimen, día, volatilidad, signo del día) que ponga el overnight en positivo neto de costes. El único subconjunto con media positiva (lunes) tiene t = 0.95 y un gap neto de −5.0 pts.

### Anatomía del gap: por qué es negativo

| Año | mediana gap (pts) | % gap > 0 | % gap = 0 | % gap < 0 |
|---|---|---|---|---|
| 2009 | 0.0 | 7.8 | 83.5 | 8.6 |
| 2011-2014 | ±0.2 a ±1.0 | 42-55 | 0-2 | 45-57 |
| 2016 | **−4.15** | 16.7 | 0.4 | **82.9** |
| 2017 | **−3.20** | 9.0 | 0.8 | **90.2** |
| 2019 | −3.20 | 20.6 | 1.2 | 78.2 |
| 2020 | −0.90 | 46.7 | 0.4 | 52.5 |

En 2016-2017-2019 el gap es negativo entre el 78 % y el 90 % de las noches, con valores repetidos (−3.0, −3.5, −6.0 pts). Eso no es mercado: es un sesgo mecánico del rollover del CFD (ajuste de financiación/dividendos aplicado en el precio al cambio de día, o el open del nuevo día marcado en el lado ask con spread de madrugada). En 2009 el 83 % de los gaps son exactamente 0 (precio sin ticks en el descanso). Es decir, el «overnight» de este dataset es un artefacto de cómo el bróker construye la vela, no un fenómeno de mercado.

## Qué apoya la hipótesis

- Nada en estos datos. El único apoyo es externo: la literatura sobre el efecto overnight en el cash US, que estos datos no pueden confirmar ni refutar porque no contienen la apertura ni el cierre del cash.

## Qué la contradice

1. El overnight medido es **negativo bruto** (−0.0275 %/día, t = −3.9, 35 % de noches positivas) y la deriva vive en el tramo open→close (+0.094 %/día, t = +4.2). Es el signo opuesto al predicho.
2. Los costes (5 pts) son 4× el tamaño del efecto en valor absoluto y el neto es −6.3 pts/noche con t = −25. Ningún año, ninguna ventana, ningún filtro lo supera. La propia hipótesis fija esta condición de muerte y se cumple.
3. El gap es un artefacto de rollover del CFD, no la subasta de apertura/cierre del Nasdaq. La razón estructural (noticias fuera de hora, prima por gap, subasta) no aplica a un intervalo de ~1 h a medianoche hora servidor.
4. No sobrevive a quitar los 2 mejores años (sigue en −0.035 %), ni a winsorizar, ni a partir el IS por la mitad.

## Lectura honesta

La hipótesis no se ha refutado en su versión de mercado (el overnight del Nasdaq cash), se ha refutado en la única versión que estos datos permiten medir: comprar el close D1 del CFD y vender el open D1 siguiente. Ese tramo es el descanso de rollover del bróker, pesa el 9 % de la varianza diaria, tiene un sesgo negativo mecánico y pierde 6 puntos por noche neto de costes, de forma estable en 13 años. No hay nada que optimizar ni filtrar: el efecto va al revés y el coste es cuatro veces mayor que su magnitud. Si Mariel quiere probar el efecto overnight de verdad, hace falta otro dato: velas intradía (M15 o H1) del CFD en las que se pueda marcar 16:00 ET y 9:30 ET, y ahí sí medir `open_9:30 / close_16:00 − 1` frente a la sesión regular, con el coste de 5 pts por RT como filtro duro. Con `NDX_D1.csv` la estrategia 003 no tiene base.

VEREDICTO: NO_EDGE
