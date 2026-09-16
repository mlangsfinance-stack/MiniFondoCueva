# 007 · oro_nasdaq — Informe AED

> Paso 02. Turno del investigador, 2026-09-15.

## Resultado: no se ha hecho AED

`hipotesis.md` está sin rellenar. Es la plantilla `PLANTILLA_HIPOTESIS.md` tal cual: las
seis secciones (activo y timeframe, comportamiento que explotas, razón estructural, cómo
se vería si es verdad, datos y fecha de corte IS/OOS, límites) solo contienen el comentario
HTML de ejemplo.

Sin premisa no hay fenómeno que medir. El investigador no inventa la hipótesis: eso es el
paso 01, verde, y lo cierra Mariel.

## Qué hay y qué falta

| Pieza | Estado |
|---|---|
| Comportamiento a testear | **Falta** |
| Razón estructural | **Falta** |
| Activo(s) y timeframe | **Falta** (el nombre de la carpeta sugiere oro + Nasdaq, pero no está declarado) |
| Fecha de corte IS/OOS | **Falta** — sin ella no se puede separar lo que se mira de lo que no |
| Zona horaria de las velas | **Falta** |
| Datos en `data/` | `NDX_D1.csv` (Nasdaq-100, diario). No hay fichero de oro (XAUUSD) ni datos intradía |

Nota sobre los datos: `data/NDX_D1.csv` ya existe (las notas de `eficiencia.md` decían que
`data/` estaba vacío; ya no). Si la hipótesis va de oro **y** Nasdaq, falta el CSV de oro.
Si va de velas intradía, `NDX_D1.csv` (diario) no sirve.

## Qué necesita el siguiente turno

Para que el AED sea real, `hipotesis.md` tiene que decir al menos:
1. Qué hace el precio que se cree repetible (una frase).
2. Por qué existe: quién pierde dinero para que esto pague.
3. Qué tendría que mostrar el AED para decir "hay edge" y qué lo mataría.
4. Activos, timeframe, ruta de los datos en `data/`, zona horaria y fecha de corte IS/OOS.

No se ha escrito `codigo/exploratorio_007.py`: no hay nada que explorar todavía.

## Lectura

No es un rechazo de la idea; es que no hay idea escrita. El veredicto es `NO_EDGE` por
falta de premisa, como manda la regla 1 del investigador. En cuanto Mariel rellene la
hipótesis (y suba el dato de oro si hace falta), se reabre y se hace el AED completo.

VEREDICTO: NO_EDGE
