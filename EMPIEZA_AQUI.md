# Empieza aquí

Esto es el MINI FONDO: el proceso con el que un fondo decide si una idea de trading merece dinero,
empaquetado para que lo corras en tu ordenador.

No hace falta que programes. La guía va en cinco pasos y el segundo ya te enseña lo importante sin
instalar nada. Si en algún momento te pierdes, salta al final: hay una sección de qué hacer cuando
algo se rompe.

Una cosa antes de empezar. Aquí no vas a encontrar una estrategia para copiar. Las siete que trae de
ejemplo están las siete descartadas, y ese es el contenido. Lo que se enseña es a descartar rápido y
con motivo escrito, que es la parte del trabajo que más dinero ahorra aunque sea la que menos se
siente como progreso.

Lee también [AVISO.md](AVISO.md). Son dos minutos y aclara qué es esto y qué no.

---

## Paso 1 — Descargar la carpeta

Vas a bajar el repositorio como un archivo comprimido. No necesitas cuenta de GitHub ni saber usar
git.

1. Abre la página del repositorio en tu navegador.
2. Busca el botón verde que dice **Code**, arriba a la derecha de la lista de archivos.
3. Púlsalo. Se abre un menú pequeño.
4. Abajo del menú, pulsa **Download ZIP**. Empieza la descarga.
5. Ve a tu carpeta de Descargas y busca `MiniFondoCueva-main.zip`.
6. Clic derecho sobre él → **Extraer todo** (en Mac, doble clic).
7. Te queda una carpeta llamada `MiniFondoCueva-main`. Muévela a un sitio que encuentres fácil: el
   Escritorio sirve.

Abre esa carpeta. Deberías ver archivos con nombres como `EMPEZAR.bat`, `README.md` y carpetas como
`codigo` y `estrategias`. Si los ves, ya lo tienes.

> Un aviso para Windows: si extraes la carpeta dentro del propio ZIP sin descomprimirlo, nada va a
> funcionar. Asegúrate de haber usado **Extraer todo** y de estar trabajando sobre la carpeta
> resultante.

---

## Paso 2 — Mirar, sin instalar nada

Tres archivos, en este orden. Quince minutos. Aquí está el 80 % de lo que vine a enseñarte.

### Las curvas

Entra en la carpeta `reportes` y haz doble clic en **`ndx_charts.html`**. Se abre en tu navegador.
No necesita internet.

Son las cuatro estrategias sobre el Nasdaq. De cada una vas a ver cinco cosas:

**La curva de capital.** La zona gris es el tramo de historia con el que se construyó la regla. La
zona blanca es el tramo que la regla nunca vio. Si la curva sube bonito en gris y se aplana en
blanco, la regla estaba memorizando el pasado.

**El drawdown.** Cuánto se llegó a perder desde el punto más alto. Este es el número que decide si
habrías aguantado sin cerrar la posición a las tres de la mañana, y por eso importa más que la
rentabilidad.

**El mapa de colores.** Cada casilla es la misma regla con parámetros distintos. Lo que buscas es
una zona ancha de casillas buenas, lo que aquí llamamos meseta. Si solo una casilla está oscura y
las de al lado claras, ese resultado salió por suerte y no va a repetirse.

**Las barras.** La regla reajustada varias veces a lo largo de los años, como la reajustarías tú.
Verde ganó en ese tramo, rojo perdió.

**El cono.** Las mismas operaciones, barajadas mil veces en otro orden. Si tu resultado real está
pegado al borde de arriba, tuviste suerte con el orden en que salieron.

### El acta de las siete

Abre [estrategias/REGISTRO.md](estrategias/REGISTRO.md). Siete filas y, en cada una, por qué murió.
Fíjate en que ninguna dice "perdía dinero". Dicen cosas como "pocas operaciones para poder saberlo"
o "solo funcionaba con un parámetro exacto".

### El caso que más enseña

Abre [estrategias/001_kaufman_breakout_er/informe_validacion.md](estrategias/001_kaufman_breakout_er/informe_validacion.md).

Esa estrategia ganaba 5,70 por cada euro perdido, y está rechazada. Hizo 24 operaciones en diez
años. Con esa muestra, el resultado no se puede distinguir de haber estado comprado durante la mejor
década del Nasdaq. Una sola operación distinta mueve el número de 5,70 a 4,90.

Si entiendes por qué eso se rechaza en lugar de celebrarse, ya tienes el método.

---

## Paso 3 — Hacer que corra en tu ordenador

### Windows

Doble clic en **`EMPEZAR.bat`**.

Se abre una ventana negra con texto corriendo. Es normal. El programa busca Python, prepara lo que
necesita y comprueba que todo funciona. Tarda menos de un minuto con conexión normal.

Si no tienes Python, te abre la página de descarga. Al instalarlo, **marca la casilla "Add Python to
PATH"** en la primera pantalla del instalador. Es lo único de todo el proceso donde te puedes
equivocar de forma que luego cueste arreglar.

Cuando termine verás `26 passed`. Eso significa que el motor funciona.

### Mac o Linux

Abre la Terminal en esa carpeta y escribe `bash empezar.sh`.

### La prueba del placebo

Después de los tests, el programa corre una estrategia sobre **precios inventados por ordenador**.
Ruido puro, sin ninguna señal dentro. Como no hay nada que encontrar, el resultado correcto es que
la rechace, y vas a ver varias líneas que dicen `FALLA`.

Ver `FALLA` ahí es la buena noticia. Un motor que aprueba el ruido te va a aprobar cualquier cosa, y
esos son los que arruinan cuentas. Antes de fiarte de un resultado, comprueba que el aparato que lo
mide sabe decir que no.

---

## Paso 4 — Probar con tus propios datos

Necesitas un archivo de precios. Un CSV con una fila por día y estas columnas en la primera fila:

```
fecha, open, high, low, close
```

Lo puedes exportar de TradingView, de tu bróker o de donde ya tengas tu histórico. Guárdalo dentro
de la carpeta `data`. El nombre da igual.

Después, **doble clic en `VALIDAR.bat`**. Te va a preguntar dos cosas, en este orden:

1. Qué estrategia quieres correr, de las cuatro. Escribes el número y pulsas Enter.
2. Qué archivo de precios usar. Te lista lo que encuentre dentro de `data` y eliges por número.
   Si escribes `0`, corre el placebo sobre precios inventados.

Tarda un rato, según cuántos años tenga tu archivo. Cuando termine te dice dónde quedó el acta:
dentro de `reportes`, en un `RESUMEN.md` que puedes abrir con el Bloc de notas.

Cada corrida tuya va a su propia carpeta, con el nombre de tu archivo pegado al final. Las actas
del ejemplo que vienen en el repo no se tocan nunca: se hicieron con datos que no se pueden
redistribuir, así que si se borraran no habría forma de recuperarlas.

Si todavía no tienes datos, ábrelo igual. Al no encontrar nada en `data` corre el placebo, y así ves
cómo es el informe completo antes de traer los tuyos.

> En Mac o Linux no hay `VALIDAR.bat`. Desde la Terminal, en esa carpeta:
> `.venv/bin/python codigo/validar.py 001 data/TU_ARCHIVO.csv` (cambia el `001` por `002`, `003` o
> `004` para las otras tres).

Los datos del Nasdaq que se usaron en los ejemplos vienen de Norgate y Darwinex, y su licencia no
permite regalarlos. Por eso hay que poner los tuyos y por eso tus números van a salir distintos de
los de la tabla.

---

## Paso 5 — Los agentes

Hasta aquí el repo es una calculadora muy exigente. Con [Claude Code](https://claude.com/claude-code)
instalado se convierte en un equipo: cinco agentes que hacen el trabajo y una mentora con la que
hablas.

| Agente | Qué hace |
|---|---|
| `@investigador` | Mira si tu idea tiene algo, antes de escribir una sola regla |
| `@protocolo` | Convierte tu idea en reglas sin ambigüedad |
| `@motor` | Backtest, optimización, robustez, tamaño de posición |
| `@validador` | Rehace los números desde cero. No se fía del motor |
| `@eficiencia` | Vigila a los otros cuatro: qué se atasca, qué se repite |
| `@mariel` | La mentora. Le preguntas cuando no sabes si algo vale la pena |

`@mariel` es a quien acudes cuando tienes una idea y no sabes si merece el tiempo, cuando un
resultado te salió sospechosamente bien, o cuando no entiendes un número de un informe. Te busca el
hueco en vez de darte la razón.

Las piezas opcionales se instalan con `pip install -r requirements-extra.txt`. Luego:

```
python -m harness.run nueva 008 mi_idea   # crea la carpeta de tu estrategia
# rellenas estrategias/008_mi_idea/hipotesis.md
python -m harness.run run 008             # arranca y se para a preguntarte
python -m harness.run ok 008              # sigues, o "no 008" para cortar
```

El proceso se detiene en dos momentos y ningún agente continúa sin ti: después del análisis inicial
y antes de salir a operar. Esos dos son tuyos.

### Verlos trabajar

Los agentes trabajan en la terminal, que para casi todo el mundo es una pared de texto. Hay una
forma de verlos.

**Pixel Agents** dibuja cada sesión de Claude Code como un personaje en una oficina de pixel art.
Camina, se sienta en su escritorio y hace una cosa u otra según lo que esté haciendo de verdad:
teclear cuando escribe código, leer cuando busca en los ficheros, quedarse parado cuando espera que
le des permiso. Cada agente sale como un personaje distinto, así que cuando lances una estrategia
vas a ver al investigador, al protocolo, al motor y al validador pasarse el trabajo.

Sirve para dos cosas concretas, más allá de que resulte entretenido. La primera es saber **si algo
está pasando o se ha quedado esperándote**, que en la terminal cuesta distinguir. La segunda es
entender **qué hace cada agente**, porque lo ves ocupado en cosas distintas.

Si abres la carpeta con [Visual Studio Code](https://code.visualstudio.com/), te va a salir solo un
aviso abajo a la derecha ofreciéndote instalarla. Acepta, abre el panel de Pixel Agents al lado de
la terminal y pulsa **+ Agent**.

También puedes instalarla a mano desde el
[Marketplace](https://marketplace.visualstudio.com/items?itemName=pablodelucca.pixel-agents), y hay
versión para JetBrains y una web que funciona sin VS Code.

Es opcional y es de un tercero, con licencia MIT. El repo corre exactamente igual sin ella.

---

## Qué te queda al terminar

Cada paso deja un archivo. Cuando cierras una estrategia, gane o pierda, tienes una carpeta
`estrategias/<ID>_<nombre>/` con esto dentro:

| Archivo | Qué es | Quién lo escribe |
|---|---|---|
| `hipotesis.md` | Tu idea: origen, fuente de retorno, core logic y qué la mataría | Tú |
| `informe_aed.md` | Si el comportamiento aparece en los datos, con tablas y números | `@investigador` |
| `reglas.md` | Tu idea traducida a instrucciones sin ambigüedad | `@protocolo` |
| `informe_motor.md` | Backtest, optimización, robustez y la propuesta de tamaño | `@motor` |
| `informe_validacion.md` | La auditoría, rehecha desde cero, y el veredicto | `@validador` |
| `bitacora.md` | Qué se probó, qué salió y qué se decidió, con fecha | Todos |
| `estado.json` | En qué fase está | El harness |

Fuera de esa carpeta se te quedan dos cosas más. En `reportes/<ID>_<nombre>/RESUMEN.md`, el acta
numérica: una página con las métricas de IS y OOS, la lista de criterios y cuáles pasaron. Y una
fila nueva en `estrategias/REGISTRO.md`, que es el registro de todo lo que has probado.

Ese registro es lo que más valor acumula. Dentro de un año, cuando se te ocurra otra vez la misma
idea, ahí va a estar escrito por qué la descartaste.

---

## El método, en cinco minutos

El repo trabaja con el método TIS. La versión larga está en [docs/METODO_TIS.md](docs/METODO_TIS.md)
y los criterios numéricos en [docs/MIS_REGLAS.md](docs/MIS_REGLAS.md), que es tu fichero: los
agentes lo obedecen y no lo pueden cambiar.

El orden importa y no se saltan pasos.

**Primero la explicación, después los datos.** Antes de tocar un backtest tienes que poder responder
quién está del otro lado de tu operación, qué lo obliga a actuar así y por qué nadie se ha comido ya
esa ventaja. Eso se llama core logic. Sin core logic tienes una correlación con suerte, y los datos
sirven para validar una hipótesis, nunca para generarla.

**Los umbrales se escriben antes de ver los resultados.** Aquí es donde casi todo el mundo se hace
trampa sin darse cuenta: si decides el mínimo después de ver el número, siempre queda justo debajo.

**El tramo reciente se aparta y se mira una sola vez.** Si lo miras, ajustas y vuelves a mirarlo, ya
no te sirve para nada.

**Buscas una zona, no un número mágico.** El parámetro que mejor luce en la tabla suele ser el más
frágil de todos.

**Después intentas romperlo.** Doblas los costes, quitas los mejores años, barajas el orden de las
operaciones. Lo que sobrevive a eso, sobrevive.

**El riesgo se mide en R**, que es lo que pierdes si salta el stop. En dólares el tamaño te lo
acaba moviendo el estado de ánimo; en R sale de una fórmula.

---

## Diccionario

| Lo que verás | Lo que significa |
|---|---|
| IS | El tramo de historia con el que se construyó la regla |
| OOS | El tramo que la regla nunca vio. El único que cuenta |
| core logic | Por qué existe tu ventaja: quién pierde y qué lo obliga |
| profit factor | Euros ganados por cada euro perdido. 1,0 es empate |
| n_trades | Cuántas operaciones. Por debajo de 30 no significa nada |
| max_dd | La peor caída desde un máximo |
| win_rate | Porcentaje de operaciones ganadoras. Por sí solo no dice si ganas dinero |
| R | Lo que pierdes si salta el stop. La unidad en la que se mide todo |
| meseta | Zona ancha de parámetros que funciona, en vez de un pico aislado |
| walk-forward | Reajustar la regla por tramos, como harías en la vida real |
| Monte Carlo | Barajar el orden de las operaciones para ver cuánto fue suerte |
| placebo | Correr sobre datos inventados. Tiene que fallar |
| DESCARTADA | No pasó el examen, con el motivo escrito al lado |

---

## Si algo se rompe

**"Windows protegió tu PC"** — Sale una pantalla azul con un botón de "No ejecutar". Es el aviso
normal de Windows para cualquier archivo descargado de internet. Pulsa **Más información** y luego
**Ejecutar de todas formas**. Si prefieres no hacerlo, cierra esa pantalla: el nivel 2 de esta guía
no necesita ejecutar nada.

**Nada funciona y las carpetas se ven raras** — Comprueba que **descomprimiste** el ZIP y no lo
abriste sin más. Windows deja mirar dentro de un archivo comprimido como si fuera una carpeta
normal, pero ahí dentro no se puede ejecutar nada ni se crea nada. Clic derecho sobre el ZIP →
Extraer todo, y trabaja sobre la carpeta que aparece.

**"En este ordenador no hay Python instalado"** — Te va a abrir la página de descarga.
Al instalarlo, **marca la casilla "Add python.exe to PATH"** en la primera pantalla, abajo. Es el
paso que más gente se salta. Después cierra la ventana negra y vuelve a hacer doble clic en
`EMPEZAR.bat`.

**La ventana negra se abre y se cierra de golpe** — Clic derecho en `EMPEZAR.bat` → Editar, para ver
qué dice. O mándame una captura.

**Terminó `EMPEZAR.bat` y ya no puedo escribir nada** — Es lo normal, esa ventana se cierra al
acabar. Para validar con tus datos no hace falta escribir: doble clic en `VALIDAR.bat`.

**`Faltan columnas [...]`** — Tu CSV no trae los nombres esperados. Ábrelo en Excel y deja la
primera fila exactamente como `fecha, open, high, low, close`. Sobran las demás columnas, pero esas
cinco tienen que estar y llamarse así.

**`ModuleNotFoundError: No module named 'streamlit'`** — Esa pieza es opcional, solo para los
paneles. Instálala con `.venv\Scripts\python -m pip install -r requirements-extra.txt`.

**Tarda muchísimo en instalar** — Está descargando. Déjalo trabajar y no cierres la ventana.

---

## Qué hacer ahora

Coge una idea tuya, esa que llevas tiempo queriendo probar, y pásala por el paso 4. Lo más probable
es que la descarte.

Eso es una tarde bien invertida. Cada idea que descartas con un motivo escrito es dinero que no vas
a perder averiguándolo con la cuenta abierta.

Cuando la descartes, cuéntamelo. Me interesa más eso que un backtest bonito.

— Mariel Lang · Trade It Simple
