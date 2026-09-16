# Registro de cambios

## 2026-09-16 — Preparación para entrega

El repo nació el mismo día de la fusión de tres sesiones en vivo. Esa fusión dejó cosas rotas y
cosas a medias. Esto es lo que se arregló y lo que se añadió antes de entregarlo.

### El método TIS, dentro del repo

Antes se citaba en ocho ficheros ("Paso 03 del método TIS") sin que hubiera ningún sitio donde se
explicara qué es.

- Instalados los seis skills del método en `.claude/skills/tis-*/SKILL.md`: `tis-estilo`,
  `tis-research-edge`, `tis-diseno-estrategia`, `tis-validacion`, `tis-riesgo-portafolio` y
  `tis-bitacora-estrategia`. Vienen cableados: quien reciba el repo no tiene que montarlos.
- Nuevo `docs/METODO_TIS.md`: el método explicado, con las tres escuelas de las que sale, los
  pilares que no se negocian y el recorrido completo de idea a live.
- Nuevo `docs/MIS_REGLAS.md`: el fichero de la persona. Es la autoridad del repo y ningún agente lo
  toca. Trae los umbrales por defecto y los sitios donde hay que escribir el riesgo propio.
  `docs/PROTOCOLO.md` pasa a ser los defaults y cede la autoridad a ese fichero.
- `docs/PLANTILLA_HIPOTESIS.md` ahora pide lo que `tis-research-edge` exige: origen de la idea,
  fuente de retorno (ineficiencia o risk premium), core logic con sus tres preguntas y qué la
  mataría.

### El agente mentor

- Nuevo `@mariel` (`.claude/agents/mariel.md`): revisa una hipótesis antes de que cueste tiempo, le
  busca el hueco a un resultado que gustó demasiado, traduce los informes y avisa cuando alguien se
  está haciendo trampa. Solo tiene permisos de lectura a propósito: no produce entregables.
- Los otros cinco agentes ya no tratan a Mariel como la operadora. Decía cosas como "Mariel decide
  el sizing" o abría una sección "Para Mariel" en el informe de quien usara el repo. Ahora se
  dirigen a la persona que lo tiene delante, que es quien decide.
- Los cinco leen `docs/MIS_REGLAS.md` y aplican `tis-estilo` antes de trabajar.

### El test de concentración

`tis-validacion` pide quitar las cinco mejores operaciones y ver qué queda. El motor solo quitaba
una.

- Nuevo `quantlab.metrics.pf_sin_top(pnl, k)` y métrica `pf_sin_top5`. Devuelve `nan` cuando la
  muestra no da para evaluarlo, en vez de un 0 que se leería como fallo.
- Nuevo criterio `pf_sin_top5_min` en `quantlab.validation.Criterios`, aplicado al OOS y a la serie
  extra. Tres tests nuevos.

### Reproducibilidad

- `codigo/validar.py 002`, `003` y `004` no funcionaban: solo existía la señal de la 001. Las otras
  tres se habían quedado en la convención del laboratorio. Portadas a
  `codigo/estrategias/<ID>_<nombre>.py`, verificando que la señal y el plan son idénticos a los del
  laboratorio, así que los números de `estrategias/REGISTRO.md` siguen siendo los mismos.
- Nuevo `tests/test_estrategias_coinciden.py`: impide que las dos copias se separen en silencio.
- `estrategias/REGISTRO.md` explica ahora cómo rehacer los números.

### Arreglos de la fusión

- Las carpetas `reportes/ndx_*` se habían renombrado a `reportes/<ID>_*` sin actualizar a quien las
  leía. Eso tenía roto `codigo/scripts/05_charts_ndx.py` y dejaba **siempre vacía** la pestaña
  "Resultados" del AED (`codigo/app/aed_ndx.py` buscaba `ndx_*`). Ahora lista cualquier carpeta con
  `RESUMEN.md`.
- Unas cuarenta referencias muertas a `hipotesis/`, `src/` y `scripts/` del laboratorio anterior,
  repartidas en diecinueve ficheros.
- Los enlaces del índice de `docs/laboratorio/README.md` no abrían: apuntaban a `docs/00_…` desde
  dentro de `docs/laboratorio/`. Su sección "Estructura" describía además el repo anterior.
- `codigo/validar.py` no reconfiguraba la salida a UTF-8 y corrompía los acentos en consola de
  Windows. Mismo arreglo que ya tenía `harness/run.py`.

### Puesta en marcha para quien no programa

- Nuevo `EMPIEZA_AQUI.md`: guía en cinco pasos que empieza por descargar el ZIP desde GitHub, sin
  dar por supuesto git ni línea de comandos.
- Nuevos `EMPEZAR.bat` (doble clic en Windows) y `empezar.sh` (Mac y Linux): preparan el entorno,
  corren los tests y lanzan el placebo. Medido en 40 segundos desde cero.
- `requirements.txt` se parte en dos. Antes la instalación mínima arrastraba Streamlit, Plotly,
  matplotlib y el SDK de agentes, y podía tardar veinte minutos o más. Ahora trae solo el motor
  (numpy, pandas, pyarrow, pytest) y lo demás vive en `requirements-extra.txt`.
- `tests/test_aed_ndx.py` importaba Streamlit y rompía la colección entera de tests cuando no
  estaba instalado. Ahora se salta con `pytest.importorskip`.
- Nuevos `LICENSE` (MIT) y `AVISO.md` con el descargo de riesgo.
- Nuevo `.gitattributes`: sin él, Git convertía `empezar.sh` a CRLF y lo dejaba inservible en Mac.

### Auditoría de los agentes contra los skills

- **Los seis agentes no podían cargar ningún skill.** Todos decían "aplica `tis-estilo`" y ninguno
  declaraba la herramienta `Skill` en su frontmatter. `harness/grafo.py` pasa
  `allowed_tools=spec["tools"]` sin añadir nada, así que la instrucción no se podía cumplir.
  Añadida `Skill` a los seis.
- `@mariel` reescrita. Antes repetía de memoria el contenido de `tis-research-edge` y de
  `tis-validacion`, lo que la dejaba desfasada en cuanto se tocara un skill. Ahora tiene una tabla
  de qué skill cargar según la pregunta y los lee. Cubre también `tis-riesgo-portafolio` y
  `tis-bitacora-estrategia`, que antes no tocaba.
- Añadidas a `@mariel` dos reglas del método que le faltaban: ofrecer dos opciones A y B ante una
  decisión de diseño y parar ahí, y sugerir la segunda lectura (auditar en una sesión nueva sin
  decir de dónde salió).
- Guardarraíl nuevo: `@mariel` habla con la voz del método y con lo que está escrito en los skills.
  No pone opiniones en boca de Mariel Lang sobre cosas que no estén ahí.

### Ver a los agentes trabajar

- `.vscode/extensions.json` recomienda **Pixel Agents** (`pablodelucca.pixel-agents`, MIT, de un
  tercero): dibuja cada sesión de Claude Code como un personaje de pixel art y los subagentes como
  personajes separados, así que se ve a los cinco agentes pasarse el trabajo. Al abrir la carpeta en
  VS Code sale el aviso para instalarla. No requiere nada del repo y el repo no depende de ella.
- Documentada en `EMPIEZA_AQUI.md` dentro del paso de los agentes, con para qué sirve de verdad:
  distinguir si algo está corriendo o te está esperando, y entender qué hace cada agente.

### Repaso con ojos de principiante

- **`EMPEZAR.bat` mentía cuando no había Python.** Windows trae un `python.exe` de 0 bytes en
  `WindowsApps` que solo abre la Microsoft Store y sale con código 9009. El script lo tomaba por un
  intérprete y respondía "tu Python es demasiado antiguo". Ahora solo acepta un intérprete que
  responda de verdad, y si no hay ninguno lo dice con las instrucciones correctas.
- **No había forma de correr nada después de `EMPEZAR.bat`.** La guía decía "escribe esto en la
  ventana negra" y esa ventana ya se había cerrado. Nuevo `VALIDAR.bat`: pregunta qué estrategia
  quieres, lista los archivos de `data/` para que elijas por número, corre las cinco fases y te dice
  dónde quedó el acta. Sin teclear rutas.
- **`chcp 65001` dejaba a `set /p` sin leer nada.** Movido a justo antes de cada llamada a Python,
  que es donde hace falta para que los acentos del RESUMEN no salgan corruptos.
- Con `enabledelayedexpansion`, `echo [!]` se comía el signo de admiración. Los errores se marcan
  ahora `[ERROR]`.
- `VALIDAR.bat` tolera espacios en lo que teclee la persona.
- Ampliada la sección de problemas de `EMPIEZA_AQUI.md` con los dos que más van a aparecer:
  la pantalla azul de "Windows protegió tu PC" y trabajar dentro del ZIP sin haberlo descomprimido.

- **Validar con datos propios borraba las actas del ejemplo.** `codigo/validar.py` escribía en
  `reportes/<ID>_<nombre>/`, la misma carpeta que trae el repo. La primera corrida de cualquiera se
  llevaba por delante unos informes hechos con series de Norgate y Darwinex que no se
  redistribuyen, o sea irrecuperables. Ahora cada corrida va a `reportes/<ID>_<nombre>__<archivo>/`
  y las del ejemplo quedan intactas. Añadido el patrón al `.gitignore`.

### Textos

- Pasados por el anti-slop de `tis-estilo`. El `README.md` decía "Spoiler: se rechaza", que es
  justo uno de los patrones que el skill prohíbe.
