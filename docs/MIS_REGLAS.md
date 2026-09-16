# Mis reglas

Este fichero es tuyo. Es la autoridad máxima del repo: **ningún agente puede cambiarlo, discutirlo
ni saltárselo**. Si un agente te propone algo que contradice lo que hay aquí, está mal y tienes que
pararlo.

Viene relleno con los valores por defecto del método TIS. Cámbialos. Son tuyos.

Lo importante no es qué número pongas. Es que lo pongas **antes** de ver los resultados. Ese es el
punto donde casi todo el mundo hace trampa consigo mismo sin notarlo: si el umbral se decide
después, siempre queda justo debajo del resultado que salió.

---

## 1. Lo que no se negocia

Estos no son números, son la forma de trabajar. Están tomados de `tis-estilo`. Si quitas alguno,
escribe aquí por qué.

- **Core logic primero, datos después.** No pasa a backtest una idea que no puede responder quién
  está del otro lado, qué lo obliga y por qué no se ha arbitrado.
- **Edge estructural, no paramétrico.** Una correlación sin explicación causal es data mining hasta
  que se demuestre lo contrario.
- **El out-of-sample se mira una sola vez.** Si lo miras, ajustas y vuelves a mirar, ya no existe.
- **Meseta, no pico.** El mejor parámetro del backtest suele ser el más frágil.
- **Costos dentro de cada métrica.** No existen números brutos.
- **Riesgo medido en R**, con el stop definido antes de entrar.
- **El régimen no es un interruptor.** Los sistemas no se prenden y apagan según el mercado; los
  filtros ya responden al régimen.
- **Cero números inventados.** Si no se puede citar, se dice cualitativamente o se marca `PENDIENTE`.
- **Todo test se registra**, también los que fallan.

## 2. Mis umbrales

Los usa el agente `validador` para aprobar o rechazar. Un solo criterio fallido es RECHAZADA.

| Qué | Mi umbral | Por qué lo puse así |
|---|---|---|
| Operaciones OOS mínimas | 30 | Con menos, ninguna métrica se distingue del azar |
| Profit factor OOS | ≥ 1.3 | |
| Drawdown máximo OOS | < 20 % | |
| PF OOS sin la mejor operación | > 1.0 | |
| **Concentración: PF sin las 5 mejores operaciones** | **> 1.0** | Si se cae aquí, son cinco eventos afortunados, no un edge |
| Meseta | ≥ 3×3, ningún vecino cae > 30 % | |
| Walk-forward | eficiencia ≥ 0.5 · ≥ 60 % de ventanas positivas | |
| Monte Carlo | p5 de retorno > 0 · p95 de DD < 25 % · ruina < 5 % | |
| Stress: costes ×2 | PF OOS ≥ 1.1 | |
| Stress: sin los 2 mejores años | PF > 1.0 | |

## 3. Mi riesgo

Esto no lo decide ningún agente. Ni el más listo.

| Qué | Mi decisión |
|---|---|
| Riesgo máximo por operación | 1 % del capital (el techo TIS es 2 %) |
| Drawdown que me hace **reducir tamaño** | `PENDIENTE — escríbelo` |
| Drawdown que me hace **apagar para revisar** | `PENDIENTE — escríbelo` |
| Capital que voy a operar | `PENDIENTE` |
| ¿Ese capital tiene alguna obligación? (pagar algo, reemplazar un ingreso) | `PENDIENTE` |

> Sobre la última fila: si el dinero tiene un trabajo que hacer y un plazo, la urgencia te va a
> empujar a operar más grande justo después de una racha mala. La corrección no es controlar las
> emociones; es que el tamaño salga de una fórmula fijada de antemano y que ese capital no tenga
> obligaciones externas.

Antes de dimensionar nada, contesta esto por escrito: **qué pasaría en tu vida si tu drawdown máximo
ocurre mañana y dura ocho meses.** Si la respuesta incomoda, el tamaño está mal, no la estrategia.

## 4. Los pasos que decido yo

Ningún agente cierra estos. Se paran y te esperan.

1. **La hipótesis.** Qué crees que hace el mercado y por qué. Nadie la escribe por ti.
2. **El criterio sobre el análisis exploratorio.** El agente te dice qué encontró; si eso es
   suficiente para seguir, lo dices tú.
3. **El tamaño de posición.** El agente propone la aritmética. La tolerancia es tuya.
4. **Salir a operar.** Siempre en demo primero.

## 5. Registro de cambios

Cada vez que cambies un umbral de arriba, anótalo aquí con la fecha y el motivo. Cambiar un umbral
después de ver un resultado que no te gustó tiene nombre, y el registro es lo que te obliga a
mirarlo de frente.

| Fecha | Qué cambié | Por qué |
|---|---|---|
| | | |
