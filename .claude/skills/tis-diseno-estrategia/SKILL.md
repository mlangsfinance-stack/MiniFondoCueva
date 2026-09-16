---
name: tis-diseno-estrategia
description: "Convierte una hipótesis con core logic en una especificación de estrategia mecánica y sin ambigüedades, lista para codificar. Activar cuando el usuario quiera definir reglas de entrada y salida, escribir la spec de una estrategia, pasar de idea a código, o cuando pida ayuda con Pine Script, Python o MQL para una estrategia propia."
---

# Diseño de estrategia

Aplica siempre `tis-estilo`. Este skill asume que la idea ya pasó por `tis-research-edge`. Si no
pasó, devuélvela ahí primero.

## Regla de oro

Una regla que necesita interpretación humana no es una regla. Si dos personas leen la spec y
ejecutan distinto, la spec está mal escrita. Si el usuario escribe "cuando el mercado se vea fuerte"
o "si hay confluencia", devuélvele la frase y pídele el umbral exacto.

## Estructura de una spec completa

```
NOMBRE E ID
Universo: qué instrumentos, con qué criterio de inclusión
Timeframe: exacto
Zona horaria: explícita, y la del feed de datos, no la tuya

SESGO
Solo largo / solo corto / ambos. Con la razón estructural.

ENTRADA
Condición(es) exactas, evaluadas en qué momento de la barra
Precio de ejecución asumido (apertura siguiente, cierre, límite)
Qué pasa si hay gap contra la condición

SALIDA
Stop: nivel, cómo se calcula, si es duro en broker
Objetivo: nivel o regla
Time stop: barra o hora de cierre forzoso
Prioridad si dos salidas se activan en la misma barra

FILTROS
Uno por uno, cada uno con su justificación estructural

SIZING
Riesgo por operación en R, método de cálculo del tamaño
Máximo de posiciones simultáneas

COSTOS ASUMIDOS
Comisión, spread, slippage — con la cifra que usaste y de dónde salió

QUÉ NO HACE
Limitaciones conocidas y condiciones donde se espera que sufra
```

## Reglas de diseño

**Cada parámetro se justifica antes de probarse.** Si el lookback es 21, tiene que haber una razón
previa (un mes de sesiones) y no "porque dio mejor que 20 y 22". Los parámetros se pre-comprometen;
el backtest confirma o desmiente, no elige.

**Menos parámetros, más vida.** Cada grado de libertad adicional multiplica el espacio donde el
sobreajuste se puede esconder. Si dudas entre dos versiones con desempeño parecido, se queda la de
menos parámetros.

**Los filtros se agregan de uno en uno**, cada uno con su propia validación out-of-sample. Apilar
filtros a ciegas es la forma más rápida y más elegante de sobreajustar sin darte cuenta.

**El lado corto y el largo se documentan por separado.** Casi nunca se comportan igual y promediarlos
esconde el problema.

**Ambigüedades típicas a cazar:**
- Señal que se evalúa con el cierre de la barra pero se ejecuta a ese mismo cierre. Eso es mirar el futuro.
- Indicadores que se recalculan con datos posteriores (repintado).
- Universo definido con la lista de hoy aplicada al pasado (sesgo de supervivencia).
- Dividendos, splits y ajustes: decir explícitamente qué serie se usa.
- Órdenes que asumen ejecución en el peor precio disponible sin verificar que hubiera liquidez ahí.

## Sobre el código

El código es didáctico, no exhibición. Snippets cortos. Lo que se pueda resolver en una hoja de
cálculo o a mano, se resuelve así primero — entender el cálculo importa más que automatizarlo.

Cuando generes código:
- Comenta la lógica, no la sintaxis.
- Deja los parámetros como constantes nombradas arriba, no enterrados.
- Incluye siempre los costos en la simulación, aunque sean conservadores.
- Si la plataforma tiene una trampa conocida (lookahead en Pine, orden de eventos en MT5, alineación
  de índices en pandas), adviértela en el mismo mensaje.

## Entregable

La spec en el bloque de arriba, completa, con los supuestos marcados donde el usuario no dio
información. No rellenes campos con valores plausibles: marca `[PENDIENTE — definir]` y sigue.
