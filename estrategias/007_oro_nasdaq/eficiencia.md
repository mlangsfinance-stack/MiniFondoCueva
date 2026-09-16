# Eficiencia — 007_oro_nasdaq

## Estado
Fase `investigacion`, vuelta_motor 0. `historial` en `estado.json` está vacío: ningún
agente ha corrido todavía sobre esta estrategia. Coste acumulado: 0. Tiempo acumulado: 0.
`bitacora.md` solo tiene el título, sin entradas.

| Turno | Fase | Coste | Duración | Veredicto |
|---|---|---|---|---|
| — | — | — | — | (sin turnos registrados) |

## Bloqueos
- **`estrategias/007_oro_nasdaq/hipotesis.md` está en blanco.** Es la plantilla tal cual
  (`PLANTILLA_HIPOTESIS.md`), sin rellenar: "Activo(s) y timeframe", "Comportamiento que
  explotas", "Por qué existe", "Cómo se vería si es verdad", "Datos" y "Límites" están
  todos vacíos (solo el comentario HTML de ejemplo). El propio `investigador.md` dice en
  su regla 1: si la hipótesis está vacía, para y cierra `VEREDICTO: NO_EDGE` sin AED. Si se
  invoca al investigador ahora, gasta un turno solo para constatar esto.
- **`data/` no tiene ningún CSV/parquet**, solo `data/README.md` con el formato esperado.
  Aunque se rellenase la hipótesis, el investigador no tiene con qué correr el AED para
  XAUUSD/NAS100 (paso 2 de su `.md` también corta en seco si no hay datos).

Ambos bloqueos son de **paso verde / entrada de Mariel** (paso 01 del protocolo), no algo
que un agente pueda resolver escribiendo código.

## Despilfarro
Ninguno todavía — no ha corrido ningún turno, no hay coste ni tiempo que revisar.

## Notas para `investigador`
- No arranques el AED todavía: `hipotesis.md` no tiene ni el activo ni el comportamiento
  a testear. Ejecutar ahora solo produce un `VEREDICTO: NO_EDGE` por falta de premisa,
  gastando un turno sin AED real.
- Cuando Mariel rellene la hipótesis, comprueba también que `data/` tenga el CSV/parquet
  del activo declarado (nombre sugerido `<SIMBOLO>_<TF>.csv`) antes de escribir
  `codigo/exploratorio_007.py`.
- Confirma en la hipótesis rellenada la fecha de corte IS/OOS y la zona horaria de las
  velas antes de medir nada: son datos que el protocolo exige y que ahora mismo no existen
  en ningún sitio del repo.

## Para Mariel
Faltan dos cosas que ningún agente puede resolver: rellenar `hipotesis.md` (paso 01,
criterio tuyo) y subir el/los CSV o parquet de mercado a `data/` (XAUUSD y/o NAS100, según
lo que decidas en la hipótesis). Hasta que estén las dos, la estrategia no puede moverse
de fase.

La estrategia está recién creada (sin turnos) y no puede avanzar hasta que se complete la hipótesis y se carguen los datos.

VEREDICTO: BLOQUEADO
