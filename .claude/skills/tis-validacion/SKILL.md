---
name: tis-validacion
description: "Protocolo de validación de estrategias Trade It Simple: in-sample / out-of-sample, walk-forward, zonas robustas, Monte Carlo, stress test, costos y criterio de paso a real. Activar cuando el usuario tenga resultados de backtest, pregunte si su estrategia está lista, hable de optimización, overfitting, curve fitting, walk forward, Monte Carlo, o quiera saber si puede pasar a dinero real."
---

# Protocolo de validación

Aplica siempre `tis-estilo`. Este es el skill donde el asistente tiene que ser más incómodo. Un
backtest bonito no es evidencia. Es una hipótesis con gráfico.

## Orden del protocolo — no se saltan pasos

```
1. Backtest in-sample      → ¿existe algo?
2. Criterios duros         → ¿pasa el mínimo?
3. Validación out-of-sample→ ¿existe fuera de donde lo construí?
4. Robustez (meseta)       → ¿existe alrededor, o solo en el pico?
5. Walk-forward            → ¿sobrevive re-estimándose en el tiempo?
6. Monte Carlo             → ¿qué tan mala pudo ser la suerte?
7. Stress test             → ¿qué pasa en los peores regímenes?
8. Costos y paridad        → ¿sobrevive a la fricción real?
9. Forward / paper         → ¿se comporta igual en vivo, sin dinero?
10. Real con tamaño mínimo → documentado desde el primer día
```

Si un paso falla, no se pasa al siguiente ajustando el paso anterior. Eso es sobreajuste con extra
pasos.

## 1. In-sample

- Muestra amplia, que incluya más de un régimen. Una serie de 17 meses es un régimen y medio: eso da
  **pase exploratorio**, no validación.
- Serie de datos de fuente confiable y verificable. Data scrapeada de origen dudoso no se usa, punto.
- Universo construido con la lista histórica, no con la lista de hoy.
- Costos incluidos desde la primera corrida.

## 2. Criterios duros

El usuario define sus umbrales **antes** de ver los resultados y los escribe. Este es el punto donde
casi todo el mundo hace trampa consigo mismo sin notarlo: si el umbral se decide después, siempre
queda justo debajo del resultado obtenido.

Dimensiones mínimas a fijar:

| Dimensión | Qué mide |
|---|---|
| Número de operaciones | Si son pocas, ninguna métrica significa nada |
| Expectancia en R | Cuánto gana en promedio cada operación, en unidades de riesgo |
| Profit factor | Bruto ganado sobre bruto perdido |
| Drawdown máximo | Profundidad y también duración |
| Sharpe o Sortino | Retorno ajustado por variabilidad |
| Calmar / MAR | Retorno contra el peor hueco |
| Concentración | Qué pasa si quitas las 5 mejores operaciones |

Ese último es el más revelador y el que menos se hace. Si al quitar las cinco mejores operaciones la
estrategia se vuelve plana o negativa, no tienes un edge: tienes cinco eventos afortunados.

No inventes umbrales "estándar de la industria". Si el usuario pide referencias, dale rangos como
puntos de partida a discutir y déjale claro que la cifra correcta depende de su frecuencia, su
horizonte y su tolerancia, y que lo importante es que se fije antes.

## 3. Out-of-sample

- La muestra OOS se aparta al inicio y **no se mira** hasta que la construcción está cerrada.
- Se usa una sola vez. Si la miras, ajustas y vuelves a mirar, ya no es out-of-sample: es in-sample
  con retraso.
- Degradación esperable entre IS y OOS: siempre hay. La pregunta no es si degrada, es cuánto y si el
  orden de magnitud se mantiene. Una caída que convierte una buena estrategia en una mediocre es
  información, no ruido.
- Si el usuario ya quemó su OOS, no hay atajo: hay que esperar datos nuevos o pasar a forward.

## 4. Robustez — meseta, no pico

Se barre cada parámetro alrededor de su valor elegido y se grafica el desempeño. Lo que buscas es
una **meseta**: una zona ancha donde los valores vecinos se comportan parecido.

- Un pico aislado rodeado de resultados malos es un artefacto. No importa lo alto que sea.
- Si el valor óptimo está en el borde del rango probado, amplía el rango: puede que el óptimo real
  esté afuera, o puede que el parámetro no esté haciendo nada.
- Preferir siempre el centro de la meseta al pico, aunque el pico luzca mejor en la tabla.

Lo mismo aplica a variar el instrumento, la ventana de fechas y el horario: si la estrategia solo
vive en una combinación exacta, no vive.

## 5. Walk-forward

Se re-estima periódicamente con datos anteriores y se opera el tramo siguiente sin volver a mirar.
Sirve para responder si el proceso de selección de parámetros —no un juego específico de
parámetros— sobrevive en el tiempo.

Reporta la eficiencia walk-forward y, sobre todo, la **estabilidad de los parámetros seleccionados**
en cada ventana. Si en cada re-estimación el óptimo salta de un extremo al otro, el parámetro es
ruido y probablemente no debería existir.

## 6. Monte Carlo

Reordenar las operaciones y remuestrear sirve para ver qué tan diferente pudo verse la curva con las
mismas operaciones en otro orden. Entrega:

- Distribución de drawdown máximo, no solo el observado.
- Probabilidad de alcanzar un drawdown que te haría abandonar.
- Rango de resultados finales en los percentiles bajos.

El número que importa no es la mediana: es el percentil malo. Tu sistema tiene que ser operable en
el percentil 5, no en el promedio.

## 7. Stress test

Correr el sistema, o su lógica equivalente, sobre los peores tramos históricos disponibles del
activo o de su clase. Crisis, cambios de estructura de mercado, épocas de volatilidad extrema y
épocas de volatilidad muerta. El objetivo no es que gane ahí: es saber cuánto duele, para no
descubrirlo con dinero puesto.

## 8. Costos y paridad

- Comisión, spread y slippage realistas. Para intradía y para estrategias de muchas operaciones,
  esta línea decide sola si hay edge o no.
- Si vas a operar en una plataforma concreta, reconcilia el backtest contra esa plataforma antes de
  ir a real. Diferencias de zona horaria, de horario de sesión, de precios de cierre o de manejo de
  órdenes cambian resultados de forma material.
- La zona horaria se verifica contra el servidor de datos, no se asume. Tratar la hora local como si
  fuera la del feed es un error clásico y silencioso.

## 9. Forward / paper

Para muestras cortas o mercados donde no hay historia suficiente, el forward en demo es la
validación real. Sin dinero, con ejecución real, durante un período definido de antemano y con
criterios de aprobación escritos antes de empezar.

## 10. Paso a real

Checklist de aprobación:

- [ ] Core logic escrito y defendible
- [ ] Spec sin ambigüedades, congelada
- [ ] IS y OOS completados, OOS usado una sola vez
- [ ] Meseta identificada, parámetro elegido dentro de ella
- [ ] Monte Carlo revisado en percentiles bajos
- [ ] Drawdown máximo esperado escrito y aceptado emocional y financieramente
- [ ] Costos realistas incorporados
- [ ] Paridad con la plataforma de ejecución verificada
- [ ] Reglas de reducción de tamaño y de revisión definidas de antemano
- [ ] Tamaño inicial conservador definido
- [ ] Bitácora abierta

Se entra con tamaño mínimo. El objetivo de los primeros meses en real no es ganar dinero, es
confirmar que la ejecución real se parece a lo simulado.

## Degradación del edge

Después de real, el trabajo no termina.

- Cierta degradación es esperable y no es señal de muerte.
- **El régimen nunca es trigger de apagado.** Los filtros del sistema ya responden al régimen.
- **Drawdown moderado → se reduce tamaño.** El sistema sigue corriendo.
- **Drawdown que alcanza el máximo histórico documentado del sistema → se apaga para revisión de
  edge decay.** Es un diagnóstico estructurado, no un abandono. Se revisa si la distribución de
  disparos cambió, si el payoff se salió de sus bandas, si el core logic sigue siendo cierto.
- Lo que se monitorea son los componentes del edge, no solo la curva de capital. Para cuando la
  curva te avisa, ya perdiste mucho.

## Cómo se comporta el asistente aquí

Tu trabajo no es aprobar. Es buscar por dónde se rompe. Antes de validar cualquier resultado,
pregúntate qué explicación aburrida podría producir esos mismos números: sesgo de supervivencia,
lookahead, costos ausentes, muestra corta, suerte concentrada en pocas operaciones.

Cuando el resultado sea demasiado bueno, dilo. Un Sharpe altísimo en un backtest casero casi siempre
es un bug, no un descubrimiento. Encontrar el bug es el resultado valioso.
