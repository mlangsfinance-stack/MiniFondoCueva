# 02 — Hipótesis: de la observación al test de tendencia

## 1. De dónde salen las ideas

| Fuente | Escuela | Ejemplo |
|---|---|---|
| Observar el precio y anotar lo que se repite | Raschke | "Cuando el día abre con gap y no lo cierra en la primera hora, tiende a extenderse" |
| Anomalías conocidas de la literatura | Kaufman / académica | Momentum 12-1, reversión a corto plazo, estacionalidad, efecto fin de mes |
| Barridos de datos sin narrativa previa | Simons | Retornos condicionales a cualquier feature medible, filtrados por significación y luego por costes |
| Estructura del mercado | todas | Rebalanceos de índices, vencimientos, horarios de liquidez, flujos de opciones |
| Fallos de sistemas propios | Kaufman | "El breakout falla cuando el ER es bajo" → hipótesis de filtro |

Regla: la fuente se anota. Una idea de barrido de datos necesita **más** evidencia que una
con mecanismo conocido, porque viene de un espacio de búsqueda mayor.

## 2. Anatomía de una hipótesis

Una hipótesis está completa cuando puede rellenar los 8 campos. Si falta uno, no es hipótesis: es idea.

1. **Observación** — qué se ha visto, en qué activo, en qué timeframe, cuántas veces.
2. **Mecanismo** — *por qué* debería existir. Cuatro familias válidas:
   - *Estructural*: alguien está obligado a operar (rebalanceos, vencimientos, hedging de dealers).
   - *Conductual*: sesgo humano persistente (infra-reacción → momentum; sobre-reacción → reversión).
   - *Riesgo*: se cobra por asumir un riesgo que otros no quieren (carry, vender volatilidad).
   - *Fricción/informacional*: la información se incorpora despacio (post-earnings drift).
   "Porque funciona en el backtest" no es un mecanismo.
3. **Universo y timeframe** — dónde se espera y dónde NO. Si se espera en todo, sospechar.
4. **Evento** — la condición observable al cierre de una barra, sin look-ahead, que activa la hipótesis.
5. **Predicción falsable** — qué hace el precio después, en qué horizonte, en qué magnitud.
   "Tras el evento, el retorno a 5 barras es mayor que el incondicional" es falsable.
   "El mercado tiende a subir" no lo es.
6. **Métrica que decide** — cuál de las medidas de `tendencies` responde a la predicción
   (retorno medio, % positivo, probabilidad de superar el alto, expansión de rango…).
7. **Criterio de muerte** — con qué número se descarta, **escrito antes de correr nada**.
8. **Coste esperado** — cuánto coste por trade admite el edge antes de morir (si el exceso
   esperado es 0.1 % y el coste es 0.1 %, no hay nada).

## 3. Taxonomía de edges (para no confundir dos en una)

| Familia | Predicción típica | Métrica | Ejemplos de setup |
|---|---|---|---|
| Continuación / momentum | tras fuerza, más fuerza | retorno fwd, % positivo | Holy Grail, breakout con ER alto, momentum 12-1 |
| Reversión | tras extremo, vuelta | retorno fwd de signo contrario | RSI(2), Turtle Soup, cierre en extremo del rango |
| Volatilidad | tras contracción, expansión | rango fwd / rango previo | NR7, squeeze de Bollinger |
| Estacional / calendario | fecha → sesgo | retorno medio por fecha | fin de mes, vencimientos, hora del día |
| Relativo / cross-seccional | ranking → dispersión | retorno top − bottom | momentum cross-seccional, pares |

Una señal mezcla como mucho **un edge de dirección + un filtro de régimen**. Más que eso son
dos hipótesis y se prueban por separado.

## 4. Test de tendencia (tramo 25–40)

Sin reglas de salida, sin stops, sin optimizar. Solo: evento → qué pasa después.

```python
from quantlab import data, indicators, tendencies
df = data.cargar("data/activo.parquet")
evento = ...                                   # Series booleana, calculada solo con datos hasta el cierre
tendencies.estudio_evento(df, evento)          # retorno fwd condicional vs base, por horizonte, t-stat
tendencies.prob_rango(df, evento, h=3)         # ¿se supera el alto? ¿se rompe el bajo?
tendencies.test_permutacion(df, evento, h=5)   # p-valor contra n eventos al azar
```

**Puerta (todas a la vez):**
- n ≥ 100 eventos (menos, y el t-stat no significa nada).
- exceso sobre la base > 0 en al menos 2 horizontes consecutivos.
- |t-stat| ≥ 2 en el horizonte principal.
- p-valor de permutación ≤ 0.05 (≤ 0.01 si la idea viene de un barrido de datos).
- Si la hipótesis dice "en todos los índices", se cumple en ≥ 2 de ellos.
- El exceso esperado es ≥ 3× el coste de ida y vuelta del activo.

**Lo que NO se hace aquí:** cambiar el evento hasta que salga. Cada variante del evento es un
test nuevo en `REGISTRO.md`. Tres variantes fallidas → la hipótesis se descarta, no se refina.

## 5. Registro y corrección por múltiples tests

`hipotesis/REGISTRO.md` tiene una fila por test. Con N tests registrados, el p-valor exigido para
creer un resultado es aproximadamente 0.05 / N (Bonferroni, conservador) — con 20 tests, 0.0025.
No hace falta ser exacto: hace falta **saber cuántas cosas se han probado** y desconfiar más
cuanto más se ha buscado. El registro también evita repetir tests ya muertos con otro nombre.
