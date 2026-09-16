# 06 — Antipatrones: cómo se engaña uno mismo

Cada uno tiene su antídoto en el proceso. Si aparece uno nuevo, se añade aquí y se añade su puerta.

| Antipatrón | Cómo se ve | Antídoto en el proceso |
|---|---|---|
| **Look-ahead** | Un indicador usa el cierre de hoy para decidir hoy; un máximo "de n barras" incluye la actual; datos ajustados con información futura | Señal al cierre, ejecución en apertura siguiente; `maximo_previo`; test `sin_lookahead` |
| **Sesgo de supervivencia** | Universo de acciones = las que existen hoy | Universo histórico con delistings; si no hay, decir explícitamente que el resultado es optimista |
| **Minería de datos** | Probar 200 variantes y presentar la que pasó | `estrategias/REGISTRO.md` con todas; p-valor exigido ≈ 0.05/N; tres variantes fallidas = hipótesis muerta |
| **OOS reutilizado** | "Solo lo miré para ver si iba bien" y luego cambiar algo | El OOS se mira una vez; tocar la regla = hipótesis nueva desde prototipo |
| **Pico de parámetros** | PF 2.1 en n=14 y 1.1 en n=13 y n=15 | Fase 3: meseta 3×3, caída < 30 % |
| **Un trade lo es todo** | PF 1.6 que pasa a 0.95 sin el mejor trade | `pf_sin_mejor` en Fase 1 |
| **Un año lo es todo** | 2020 hace el 80 % del PnL | Stress: sin los 2 mejores años; PnL por año en prototipo |
| **Costes al final** | "Luego le meto costes" — y muere | Costes desde prototipo; ×2 en stress |
| **Complejidad creciente** | Filtro sobre filtro para arreglar el último drawdown | ≤ 4 parámetros, ≤ 30 líneas; cada filtro es una hipótesis con su tendencia |
| **Mecanismo inventado a posteriori** | Narrativa bonita después del backtest | Mecanismo escrito en la ficha **antes** del test de tendencia |
| **Confundir escala con edge** | CAGR alto por apalancamiento, no por expectativa | Puertas sobre PF, expectancia R, t-stat; CAGR solo informa |
| **Motor a medida** | "Esta estrategia necesita su propio backtester" | Un motor; lo que falte se añade al motor con test |
| **Régimen único** | Solo se probó en tendencia alcista | Peor tercio en stress; multi-mercado cuando aplica; placebo sintético |
| **Umbral a medida** | Bajar PF mínimo a 1.25 "porque esta es especial" | Umbrales del laboratorio, no de la estrategia; historial de cambios en `03_VALIDACION.md §5` |
| **Retirada renegociada** | "Un mes más, seguro que vuelve" | Regla de retirada escrita antes de live; 🔴 = parada mecánica |

## Checklist antes de dar por validado cualquier número

- [ ] La señal usa solo datos ≤ cierre de la barra en que se calcula.
- [ ] La ejecución es en la barra siguiente, con coste.
- [ ] Los datos cubren al menos dos regímenes distintos (alcista, bajista, lateral).
- [ ] Cuento cuántos tests he hecho para llegar aquí, y están en el registro.
- [ ] El OOS no se ha mirado antes de fijar los parámetros.
- [ ] Sin el mejor trade y sin el mejor año, sigue en positivo.
- [ ] Los parámetros vecinos también ganan.
- [ ] El resultado se reproduce con una sola orden desde el repo limpio.
- [ ] Podría explicar el mecanismo a alguien en dos frases sin usar la palabra "backtest".
