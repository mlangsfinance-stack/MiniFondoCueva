# 00 — Filosofía: tres escuelas, un proceso

No son tres estilos a elegir. Cada uno cubre una parte del camino donde los otros dos son
débiles: Raschke sabe **mirar** el mercado, Kaufman sabe **construir** algo que no se rompa,
Simons sabe **demostrar** que no es casualidad y **agregar** muchos edges pequeños.

## 1. Linda Raschke — observar antes de programar

- **Tendencias, no sistemas.** Antes de reglas, la pregunta es: *"después de X, ¿el mercado
  hace Y más veces de lo normal?"* Se mide con estadística de instituto: n, media, % de
  aciertos, comparado con la base incondicional. Si no hay tendencia, no hay nada que optimizar.
- **Playbook de setups.** Cada setup tiene nombre, contexto (régimen), disparo, stop y
  gestión de la salida definidos **antes** de la entrada. El Holy Grail (ADX + retroceso a
  EMA20), Turtle Soup (falso breakout), 80-20, NR7… son ejemplos: patrones simples con
  mecanismo claro.
- **El mercado alterna.** Rango → expansión → tendencia → contracción. Un setup sirve en un
  régimen; saber en cuál estás vale más que afinar el setup.
- **Los mejores trades funcionan enseguida.** Si una operación no hace lo que debe en
  poco tiempo, la hipótesis de ese trade ya está rota: salida por tiempo.
- **Proceso diario y diario.** Preparación pre-mercado, plan, ejecución, revisión. El diario
  no es terapia: es la fuente de hipótesis nuevas.
- **Riesgo primero.** Se define cuánto se pierde si falla antes de pensar cuánto se gana.

## 2. Perry Kaufman — robustez antes que rendimiento

- **Simplicidad.** Cada parámetro añadido es una oportunidad más de ajustarse al pasado.
  Sistema bueno = pocas reglas que se explican en una frase.
- **Meseta, no pico.** Un parámetro es válido si sus vecinos también ganan. La optimización
  no busca *el* mejor valor: busca la *zona* donde da igual el valor exacto.
- **Adaptación al ruido.** El Efficiency Ratio mide señal/ruido del precio; la KAMA acelera
  cuando hay tendencia limpia y se frena cuando hay ruido. Es la alternativa honesta a elegir
  a mano "la media de 37 periodos".
- **Probar en varios mercados y periodos.** Un edge que solo funciona en un activo y en una
  década es una anécdota.
- **Costes y ejecución son parte del sistema**, no un ajuste al final.
- **Entender por qué pierde.** Un sistema cuyo drawdown se explica (régimen, whipsaw, coste)
  se puede operar; uno que pierde sin motivo conocido, no.
- **Expectativa matemática.** Todo se reduce a: (% acierto × ganancia media) − (% fallo ×
  pérdida media), con costes. El resto es narrativa.

## 3. Jim Simons / Renaissance — demostrar, agregar, no creer

- **Los datos primero.** No hace falta que la explicación sea bonita; hace falta que el
  efecto sea estadísticamente real, repetible y ejecutable.
- **Contraste contra el azar.** Toda anomalía se compara con lo que daría el azar (permutación,
  placebo con datos sin estructura). Un t-stat de 2 con 30 trades no es nada.
- **Corrección por múltiples tests.** Si probaste 100 ideas, 5 pasarán por casualidad al 5 %.
  Por eso **todo test se registra** y el umbral sube con el número de intentos.
- **Muchos edges pequeños y poco correlacionados.** Un PF de 1.2 sostenido en 20 mercados
  independientes es un negocio; un PF de 2.5 en uno solo es una moneda al aire.
- **La ejecución es el edge o lo mata.** Slippage, impacto, horarios, calidad de datos.
- **Revisión por pares y ciencia reproducible.** Código versionado, datos fechados, resultados
  reproducibles con una orden. Si no se puede reproducir, no existe.
- **Sin ego.** El proceso decide, no la persona. Lo que no pasa, se descarta sin drama.

## 4. Síntesis — los 10 principios del laboratorio

1. **Observar → hipótesis → test.** Nunca al revés (buscar un test que confirme lo que quiero).
2. **Una hipótesis, un mecanismo, una predicción falsable.** Con criterio de muerte escrito antes.
3. **Tendencia antes que sistema.** Si el retorno condicional no supera la base, se para ahí.
4. **Simple: ≤ 4 parámetros, ≤ 30 líneas.** Lo que no cabe son dos hipótesis.
5. **Costes desde el primer backtest.** Y ×2 en stress.
6. **OOS intocable.** Se mira una vez; el walk-forward es la única re-optimización permitida.
7. **Meseta o nada.** Vecinos 3×3 ganando, sin caídas > 30 %.
8. **Contraste con el azar y con el placebo.** Permutación, Monte Carlo, datos sintéticos sin estructura.
9. **Registro total.** Cada test cuenta para la corrección por múltiples comparaciones.
10. **Cartera, no estrategia.** El objetivo final es agregar edges poco correlacionados con riesgo controlado; una estrategia sola es un paso intermedio.
