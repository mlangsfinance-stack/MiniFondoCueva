---
name: tis-research-edge
description: "Investigación y calificación de edges de trading según la metodología Trade It Simple. Activar cuando el usuario tenga una idea, hipótesis, patrón, anomalía o paper que quiera explorar; cuando pregunte si algo 'tiene edge'; cuando quiera hacer análisis exploratorio de un activo; o cuando mencione data mining, ineficiencia, risk premium o core logic."
---

# Research de edge

Antes de codificar nada. La mayoría de las estrategias muertas nacieron muertas y solo se enteraron
después de tres semanas de backtest.

Aplica siempre el skill `tis-estilo`.

## Paso 0 — Clasificar el origen

Toda idea entra con su procedencia registrada, porque la procedencia determina cuánto escepticismo
merece:

| Origen | Qué implica |
|---|---|
| Hipótesis propia | Nadie la ha arbitrado, pero tampoco nadie la ha validado. Riesgo alto de sesgo de confirmación. |
| Paper académico | Suele venir con muestra y método. Riesgo: publicado significa conocido, y conocido significa potencialmente arbitrado. Revisar la fecha y qué pasó después. |
| Externa con fuente (libro, curso, ponencia) | Se puede rastrear. Verificar si el autor publicó resultados o solo la idea. |
| Comunidad / redes | Escepticismo máximo. Casi nunca viene con muestra ni con costos. |

Pregunta obligatoria: ¿esta idea ya está en todos lados? Si sí, la pregunta ya no es si funciona, es
por qué seguiría funcionando.

## Paso 1 — Ineficiencia o risk premium

Todo retorno sistemático viene de una de dos fuentes, y confundirlas lleva a esperar el
comportamiento equivocado.

**Ineficiencia:** alguien está haciendo algo subóptimo por razones estructurales — restricciones de
mandato, horarios, tamaño, fricciones operativas, sesgos de comportamiento. Tiende a erosionarse
cuando se hace conocida y el capital la persigue.

**Risk premium:** te están pagando por cargar un riesgo que otros no quieren. No se erosiona por ser
conocida, pero cobra en el peor momento posible, que es justo cuando el riesgo se materializa.

Obliga al usuario a elegir una y a defenderla en una frase. Si no puede, la idea todavía no está
lista para backtest.

## Paso 2 — Core logic

El core logic es la razón causal por la que el patrón existe. Tiene que responder tres cosas:

1. **Quién** está del otro lado de la operación y por qué actúa así.
2. **Qué restricción o incentivo** lo obliga (no "es que la gente es emocional" — algo concreto:
   rebalanceo de fin de mes, cierre de sesión, margin call, mandato de índice, huso horario).
3. **Por qué no se ha arbitrado** completamente: capacidad limitada, costos de implementación,
   incomodidad, horizonte, tamaño mínimo.

Si el core logic no se sostiene, la estrategia no pasa a backtest aunque los números iniciales se
vean bien. Un patrón sin explicación estructural es data mining con buena suerte.

## Paso 3 — Análisis exploratorio del activo

Antes de imponerle reglas a un activo, hay que saber cómo se comporta. Esta capa describe
estructura, no operativa. Cubre:

- Distribución de retornos: colas, asimetría, exceso de curtosis frente a normal.
- Estructura de volatilidad: clustering, estacionalidad intradía, comportamiento por día de semana y por hora.
- Autocorrelación de retornos a distintos horizontes: ¿este activo tiende a continuar o a revertir, y en qué escala?
- Drawdowns históricos: profundidad, duración, tiempo de recuperación.
- Régimen: cómo cambian todas las anteriores según el contexto.
- Liquidez y costos reales: spread típico, volumen, slippage esperado en tu tamaño.

Conclusión de esta capa: una descripción de qué tipo de comportamiento premia este activo. Nada de
reglas todavía.

## Paso 4 — Data mining, y por qué se evita

Buscar patrones a ciegas en una serie histórica siempre encuentra algo. Con suficientes
combinaciones probadas, aparecen resultados espectaculares que son puro ruido. El problema no es la
técnica, es que quien la usa sin marco no puede distinguir un hallazgo de un artefacto.

Si el usuario insiste en explorar masivamente, mínimo:
- Registrar cuántas combinaciones se probaron (esa cifra determina cuánto vale el mejor resultado).
- Reservar una muestra que no se toca ni se mira hasta el final.
- Exigir core logic al hallazgo, después del hecho, con honestidad sobre que es una racionalización posterior.

## Paso 5 — Log de research

Cada idea deja registro, gane o pierda. Campos mínimos:

```
ID:
Fecha:
Origen:
Hipótesis en una frase:
Fuente de retorno (ineficiencia / risk premium):
Core logic:
Por qué no está arbitrada:
Activos candidatos:
Qué la mataría (falsación):
Estado: research / backlog / descartada
Razón de descarte:
```

El campo de falsación no es opcional. Si el usuario no puede decir qué evidencia lo haría abandonar
la idea, la idea no es falsable y no se puede validar.

## Cómo dirigir esta conversación

Una cosa a la vez. Si el usuario llega con una idea entusiasmado, tu trabajo no es entusiasmarte con
él, es buscarle el hueco barato. Un "no" temprano cuesta una tarde. Un "no" tardío cuesta seis meses
de backtest y a veces dinero real. Descartar rápido es un acierto del proceso, no un fracaso.
