# El método TIS

TIS es la forma de trabajar de Trade It Simple: un proceso para llevar una idea de trading desde la
frase suelta hasta dinero real, o hasta el archivo de descartadas con el motivo escrito. La mayoría
acaba en el archivo, y ese es el funcionamiento correcto.

Este documento explica el método. Los umbrales concretos viven en [MIS_REGLAS.md](MIS_REGLAS.md),
que es tuyo, y la mecánica del pipeline de agentes en [PROTOCOLO.md](PROTOCOLO.md).

---

## De dónde sale

El método junta tres escuelas que responden a preguntas distintas. La síntesis larga está en
[laboratorio/00_FILOSOFIA.md](laboratorio/00_FILOSOFIA.md).

**Jim Simons y Renaissance** aportan la exigencia estadística: un edge es una anomalía que sobrevive
al contraste contra el azar y a los costes reales. Muchos edges pequeños y poco correlacionados
valen más que uno grande. Nada se cree sin test y todo test se registra.

**Perry Kaufman** aporta la robustez por delante del rendimiento: pocos parámetros, mesetas en vez
de picos, adaptación al ruido del mercado, y entender por qué pierde un sistema antes de ponerlo a
ganar.

**Linda Raschke** aporta el orden de trabajo: observar primero, medir el comportamiento del mercado
con estadística simple, y solo después escribir reglas con disparo, stop y salida definidos antes
de entrar.

---

## Lo que el método asume

Estos pilares gobiernan todo lo demás. Si algo de lo que vas a hacer los contradice, el problema
está en lo que vas a hacer.

**El edge es estructural, no paramétrico.** Una ventaja vive en una razón causal del comportamiento
del mercado. Si solo vive en una combinación de parámetros, es un hallazgo de data mining hasta que
demuestres lo contrario.

**Core logic primero, datos después.** Los datos validan una hipótesis; no la generan. Empezar por
los datos es exactamente el error que produce estrategias que mueren al ponerles dinero.

**El régimen no es un interruptor.** Los sistemas no se prenden y apagan según cómo veas el mercado
por la mañana. Los filtros del sistema ya responden al régimen. Saber en qué régimen estás te da
contexto y tranquilidad, no permiso para activar y desactivar.

**El activo se filtra solo.** Un sistema bien construido no necesita que decidas cada día si opera.

**In-sample y out-of-sample, siempre.** No es opcional ni es "cuando haya tiempo".

**Meseta, no pico.** El mejor parámetro del backtest suele ser el más frágil.

**Riesgo en R, con stop duro en el bróker.** Nunca más del 2 % del capital por operación, y ese 2 %
es techo, no objetivo.

**Cero números inventados.** Ni tuyos ni de tu IA. Lo que no se puede citar se dice de forma
cualitativa o se marca como pendiente.

---

## El recorrido

```
idea → research de edge → diseño → validación → riesgo → bitácora → live
```

La mayoría de las ideas se caen en el primer tramo. Ese es el punto. Un "no" en la primera tarde
cuesta una tarde; un "no" después de seis meses de backtest cuesta seis meses y a veces cuesta
dinero real.

### Research de edge

Antes de codificar nada. Cada idea entra con su **origen** registrado, porque la procedencia decide
cuánto escepticismo merece: una hipótesis propia arrastra sesgo de confirmación, un paper publicado
puede estar ya arbitrado, y algo que viene de redes casi nunca trae muestra ni costes.

Después eliges **fuente de retorno** y la defiendes en una frase. Solo hay dos. Una **ineficiencia**
es alguien haciendo algo subóptimo por una restricción estructural — un mandato, un horario, un
tamaño — y se erosiona cuando se hace conocida. Un **risk premium** es que te paguen por cargar un
riesgo que otros no quieren; no se erosiona por ser conocido, pero cobra en el peor momento posible.

Y llegas al **core logic**, que responde tres cosas: quién está del otro lado, qué restricción o
incentivo concreto lo obliga, y por qué nadie se ha comido ya esa ventaja. Si el core logic no se
sostiene, la idea no pasa a backtest aunque los primeros números se vean bien.

Se cierra con **qué la mataría**. Si no puedes decir qué evidencia te haría abandonar la idea, la
idea no es falsable y no se puede validar.

### Diseño

Una regla que necesita interpretación humana no funciona como regla. Si dos personas leen tu
especificación y ejecutan distinto, está mal escrita. "Cuando el mercado se vea fuerte" no es una
regla; un umbral exacto sí.

Cada parámetro se justifica **antes** de probarlo. Si el lookback es 21, que sea porque son las
sesiones de un mes, y no porque dio mejor que 20 y que 22. Los parámetros se pre-comprometen y el
backtest confirma o desmiente; el backtest no elige.

Los filtros se añaden de uno en uno, cada uno con su propia validación. Apilarlos a ciegas es la
forma más elegante de sobreajustar sin enterarte.

### Validación

Diez pasos, en orden, sin saltárselos. Si uno falla, no se pasa al siguiente ajustando el anterior:
eso es sobreajuste con pasos extra.

1. Backtest in-sample — ¿existe algo?
2. Criterios duros — ¿pasa el mínimo que fijaste antes de mirar?
3. Out-of-sample — ¿existe fuera de donde lo construiste?
4. Robustez — ¿existe alrededor, o solo en el pico?
5. Walk-forward — ¿sobrevive re-estimándose en el tiempo?
6. Monte Carlo — ¿qué tan mala pudo haber sido la suerte?
7. Stress — ¿cuánto duele en los peores tramos?
8. Costes y paridad — ¿sobrevive a la fricción real?
9. Forward en demo — ¿se comporta igual en vivo, sin dinero?
10. Real con tamaño mínimo — documentado desde el primer día.

Dos detalles que deciden más de lo que parece. El primero: **la concentración**. Quita las cinco
mejores operaciones y mira qué queda. Si se vuelve plano o negativo, tienes cinco eventos
afortunados. El segundo: **el percentil malo del Monte Carlo**. Tu sistema tiene que ser operable en
el percentil 5, no en el promedio, porque el promedio no es lo que te va a tocar vivir.

### Riesgo

R es lo que pierdes si salta el stop, y en R se mide todo: la expectancia, el drawdown, el mes.
Pensar en dólares hace que el tamaño se mueva por razones emocionales; pensar en R lo convierte en
aritmética.

Hay un patrón que arruina cuentas y que no tiene nada de psicológico: **capital con un trabajo que
hacer**. Cuando el dinero tiene que rendir cierta cantidad en cierto plazo, la urgencia empuja a
operar más grande justo después de una racha perdedora. La corrección es que el tamaño salga de una
fórmula fijada de antemano y que ese capital no tenga obligaciones externas.

En cartera, la descorrelación que importa es **entre sistemas**, no entre activos. Dos seguidores de
tendencia en instrumentos distintos suelen perder las mismas semanas: son el mismo sistema con dos
nombres.

### Bitácora

Lo que no está documentado no existe. Dentro de seis meses no vas a recordar por qué elegiste 21 en
vez de 20, y sin esa razón no puedes distinguir una degradación real de una mala racha.

Cada estrategia vive en un estado y se mueve con motivo escrito: `research`, `backlog`,
`en_validacion`, `validada`, `forward`, `live`, `retirada`, `descartada`. Las descartadas no se
borran nunca. Ese archivo es lo que evita que repitas el mismo trabajo dentro de un año.

---

## Cómo lo implementa este repo

| Tramo del método | Dónde vive aquí |
|---|---|
| Research de edge | `@investigador` · `docs/PLANTILLA_HIPOTESIS.md` · `informe_aed.md` |
| Diseño | `@protocolo` → `reglas.md` |
| Validación | `@motor` + `codigo/quantlab/validation.py` → `reportes/<carpeta>/RESUMEN.md` |
| Auditoría independiente | `@validador`, que rehace los números sin fiarse del motor |
| Riesgo | `@motor` propone, tú decides en `docs/MIS_REGLAS.md` |
| Bitácora | `estrategias/<ID>/bitacora.md` · `estrategias/REGISTRO.md` |
| Mentoría | `@mariel` |

Los seis skills del método están instalados en `.claude/skills/`. Se activan solos cuando la
conversación toca su tema y también los puedes llamar por nombre. `tis-estilo` gobierna a los otros
cinco y es el que contiene las reglas de "cero números inventados" y "el régimen no es un
interruptor", que es justo donde una IA sin frenos hace más daño.

---

## Lo que el método no hace

No genera estrategias rentables. Genera un proceso que descarta las malas más rápido y documenta las
que sobreviven.

No sustituye a entender lo que estás haciendo. Un backtest que no sabes leer es igual de peligroso
venga de donde venga.

No es asesoría financiera y no promete resultados. Es metodología.

— Trade It Simple · tradeitsimplesolutions.com
