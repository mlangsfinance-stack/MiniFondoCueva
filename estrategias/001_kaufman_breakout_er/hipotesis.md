# 001 · kaufman_breakout_er — Hipótesis

> Paso 01. La escribe la persona, no la IA. Sin esto el investigador no arranca.

## Activo(s) y timeframe
NDX (Nasdaq 100), velas diarias (D1). Índice cash como serie principal; CFD del broker como
segunda serie para comprobar que el resultado sobrevive a los precios reales que se operan.

## Comportamiento que explotas
Un cierre por encima del máximo de las últimas 40 sesiones tiende a continuar al alza **cuando el
tramo que ha llevado hasta ahí ha sido limpio** (pocos retrocesos). Si la ruptura llega tras un
tramo ruidoso, la tasa de fallo (whipsaw) sube mucho. Solo largos.

## Por qué existe (la razón estructural)
Infra-reacción a noticias y flujos que se incorporan despacio (momentum), reforzada por stops de
cortos y por gestores tendenciales que entran en máximos de N días. El Efficiency Ratio de Kaufman
mide si el tramo previo tiene dirección neta (señal) frente a oscilación (ruido): en ese régimen el
precio "cuesta menos" de mover y la continuación es más probable. Solo largos porque el NDX tiene
deriva positiva estructural y las rupturas bajistas de índices son de otra naturaleza (pánico,
reversión rápida): mezclar lados sería mezclar dos hipótesis.

Fuente: Kaufman, *Trading Systems and Methods* (5ª ed.), cap. 5 (N-day breakout) y cap. 17
(Efficiency Ratio); *Smarter Trading*, capítulo sobre ruido de mercado.

## Cómo se vería si es verdad
- Tras el evento `close > máx(high, 40 previas) & ER(10) ≥ 0.3`, el retorno a 5 y 10 barras es
  mayor que el incondicional. Exceso esperado a h=5: ≥ +0.15 % (≥ 3× el coste de ida y vuelta).
- La probabilidad de superar el alto de la barra del evento en 3 barras supera la base.
- **Lo mataría:** exceso ≤ 0 a h=5, p-valor de permutación > 0.05, o que el exceso sea solo la
  deriva alcista del índice (la base sin condición lo iguala).

## Datos
- `data/ndx_norgate_d1.parquet` — NDX cash 1985-2026 (no se versiona: licencia Norgate).
- `data/ndx_darwinex_d1.parquet` — CFD NDX 2008-2026 (no se versiona).
- Fecha de corte IS/OOS: **2016-01-01**. IS = 1985-2015. OOS = 2016-2026, en ambas series.

## Límites
- Solo largos. Una posición como máximo. Sin apalancamiento sobre el riesgo declarado.
- Parámetros de Kaufman (40 / 20 / ER 10 / 0.3): **no salen de buscar** y no se acortan para
  fabricar trades.
- Riesgo 1 % del equity por trade. Costes 2 pb por lado (spread/2 + slippage sobre NDX ~8 000).
- El OOS se mira una vez.
