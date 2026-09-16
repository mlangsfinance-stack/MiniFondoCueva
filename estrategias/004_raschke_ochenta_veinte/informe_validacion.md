# E004 — ochenta_veinte (80-20 de Street Smarts, ambas direcciones, NDX diario)

- **Hipótesis origen:** H004 (`hipotesis/H004_ochenta_veinte.md`)
- **Familia de edge:** reversión a corto plazo
- **Estado:** `x_descartadas/` — muerta en **prototipo IS** (PF 0.74, t=−3.8) y confirmada en
  **Fase 1 (IS/OOS)** de la validación; además falla F2, F3 y F5. El lado corto ya había muerto
  en tendencia (exceso con el signo contrario).
- **Señal:** `quantlab.senales_raschke.ochenta_veinte` · parámetros fijados:
  `{pct: 0.2, hold: 1, atr_mult_rango: 1.0}` · config `{stop_atr: 1.5, max_barras: 1}`
- **RESUMEN de validación:** `reportes/ndx_ochenta_veinte/RESUMEN.md` (2026-09-15, **DESCARTADA**)

## 1. Especificación operable
| Campo | Valor |
|---|---|
| Universo y sesión | NDX cash (Norgate) para IS/OOS; CFD NDX Darwinex como OOS real (2016+) |
| Barra | diaria |
| Entrada | apertura del Día 2 (barra siguiente a la señal). Señal Día 1: abre en el 20 % superior del rango y cierra en el 20 % inferior (largo) o el espejo (corto), con rango ≥ 1.0 × ATR(10) previo |
| Stop inicial | k = 1.5 × ATR(14) |
| Salidas | por señal: apertura del Día 3 (el motor ejecuta en apertura; Street Smarts cierra el mismo día) / por stop |
| Gaps | fill en apertura si abre más allá del stop |
| Datos | Norgate NDX 1985–2026 (antes de ~2000 el open es el cierre previo: el evento en ese tramo es un artefacto); Darwinex 2008–2026 |

Simplificaciones respecto a Street Smarts: sin esperar al nuevo extremo en Día 2 ni stop en ese
extremo; salida en apertura de Día 3 en vez de al cierre de Día 2.

## 2. Motivo del descarte (acta)
Tendencia IS: largo PASA (n=570, exceso h=1 +0.14 %, t=2.21, p=0.018; en 2000–2015 +0.27 %, p=0.002);
corto MUERE (n=630, exceso h=1 **+0.12 %** — continuación, no reversión; 2000–2015: −0.04 %, p=0.61).
Prototipo IS (ambas direcciones): n=1153, PF 0.74, exp −0.044 R, t=−3.77, 35 % años positivos.
Por lado: corto PF 0.57 (t=−5.0), largo PF 0.95 (t=−0.45). Por tramo: pre-2000 (open artificial)
corto 0.43 / largo 0.82; 2000–2015 (open real) corto 1.00 / largo 1.12.
Validación (una sola pasada, `--rapido`):

| fase | check | valor | umbral |
|---|---|---|---|
| 1 | pf_oos (Norgate 2016+, 276 trades) | 1.153 | ≥ 1.30 |
| 1 | pf_oos_darwinex (361 trades) | 1.161 | ≥ 1.30 |
| 2 | wf_eficiencia | 0.000 | ≥ 0.50 |
| 3 | meseta_min_vecino | 0.651 | ≥ 1.20 |
| 5 | stress_costes_x2_pf_oos | 1.049 | ≥ 1.10 |
| 5 | stress_sin_2_mejores_anios_pf | 0.769 | ≥ 1.10 |
| 5 | stress_peor_tercio_pf | 0.548 | ≥ 1.10 |

PF por tercios: 0.55 / 1.13 / 1.07. El OOS (PF 1.15 en las dos series, coherente entre índice y
CFD) es mejor que el IS porque el IS arrastra 15 años con open = cierre previo, donde el patrón
no significa lo que Street Smarts describe.

## 3. Lección
1. El 80-20 en el NDX es **asimétrico**: solo el lado largo (tras día de venta) tiene exceso; el
   corto opera contra el momentum del índice y lo destruye todo.
2. Un edge de +0.14–0.27 % a un día con stop intradía y 4 pb de coste queda en PF ≈ 1.1: demasiado
   fino para sobrevivir a costes ×2.
3. Con índice cash sin apertura real antes de 2000 el patrón no se puede testear; hay que
   restringir a datos con open real o usar futuros.
Siguiente iteración (hipótesis nueva, no ajuste): **H004.1** — solo largos, datos con open real
(2000+ o futuros NQ), salida al cierre de Día 2 (añadir al motor con test), sin stop intradía o
stop en el extremo de Día 1 como dice el libro. Tendencia primero.

## Historial de estado
| Fecha | De | A | Motivo |
|---|---|---|---|
| 2026-09-15 | idea | tendencia | ficha H004 escrita; evento largo pasa, corto muere |
| 2026-09-15 | tendencia | prototipo | se mantiene la definición original (ambas direcciones) |
| 2026-09-15 | prototipo | validación | no pasa puerta (PF 0.74, t=−3.8); se valida igualmente para ver el pipeline entero |
| 2026-09-15 | validación | x_descartadas | DESCARTADA en Fase 1: PF OOS 1.15 Norgate / 1.16 Darwinex; F2, F3, F5 también fallan |
