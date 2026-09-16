# Exxx — <nombre>

- **Hipótesis origen:** Hxxx (enlace a la ficha)
- **Familia de edge:** —
- **Estado:** la carpeta donde está este fichero. Historial de cambios de estado al final.
- **Señal:** `quantlab.senales.<funcion>` · parámetros fijados: `{...}`
- **RESUMEN de validación:** `reportes/<nombre>/RESUMEN.md` (fecha, veredicto)

## 1. Especificación operable
| Campo | Valor |
|---|---|
| Universo y sesión | activos, horario, zona horaria de la plataforma |
| Barra | diaria / 60m / … |
| Entrada | apertura de la barra siguiente a la señal, orden a mercado |
| Stop inicial | k = __ × ATR(14) |
| Salidas | por señal contraria / por tiempo (__ barras) / por stop |
| Gaps | fill en apertura si abre más allá del stop |
| Datos | fuente, ajuste, tratamiento de huecos |

## 2. Sizing y límites
| Campo | Valor |
|---|---|
| Método | fixed fractional: riesgo __ % del equity hasta el stop |
| Justificación | MaxDD p95 MC (__ %) × factor de sizing ≤ DD tolerable (__ %) |
| Posiciones simultáneas máx. | __ |
| Exposición máx. por activo / total | __ / __ |
| Parada por pérdida | diaria __ % · semanal __ % |

## 3. Encaje en cartera
| Estrategia existente | Correlación mensual | Mismo modo de fallo? |
|---|---|---|
| — | — | — |

MAR de la cartera sin / con esta estrategia: __ / __.

## 4. Incubación
- Inicio: AAAA-MM-DD · plataforma: __ · modo: paper / forward
- Trades: __ (objetivo ≥ 30) · meses: __ (objetivo ≥ 3)
- Equity real vs cono MC: dentro / fuera (p__)
- Paridad motor ↔ plataforma: nº trades __ vs __ · PnL __ % de diferencia
- Costes reales medidos: __ (modelados: __)
- Decisión: pasa a live / vuelve a validación / descartada

## 5. Live — monitor mensual
| Mes | Trades | PF rodante (30) | Equity vs cono MC | DD actual | Salud | Acción |
|---|---|---|---|---|---|---|
| — | — | — | — | — | 🟢/🟡/🔴 | — |

## 6. Regla de retirada (escrita antes de live, no se renegocia)
- 🟡 tamaño ½ si equity < p25 del cono dos meses seguidos.
- 🔴 parada si equity < p5 del cono **o** DD > p95 MC (__ %).
- Retirada → ficha a `x_descartadas/` con motivo y números; re-validar desde Fase 1 si se quiere volver.

## Historial de estado
| Fecha | De | A | Motivo |
|---|---|---|---|
| — | — | — | — |
