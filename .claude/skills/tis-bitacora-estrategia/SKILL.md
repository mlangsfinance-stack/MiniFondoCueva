---
name: tis-bitacora-estrategia
description: "Documentación, taxonomía de estados y bitácora de estrategias en el estilo Trade It Simple. Activar cuando el usuario quiera documentar una estrategia, llevar registro de sus sistemas, organizar su pipeline de ideas, escribir el doc de un backtest, o preguntar en qué estado está algo."
---

# Documentación y bitácora

Aplica siempre `tis-estilo`. Lo que no está documentado no existe: dentro de seis meses no vas a
recordar por qué elegiste 21 y no 20, y sin esa razón no puedes distinguir degradación real de mala
suerte.

## Taxonomía de estados

Cada estrategia vive en exactamente un estado y se mueve con un motivo escrito.

```
research       → idea con core logic, sin backtest
backlog        → aprobada conceptualmente, esperando turno
en_validacion  → corriendo el protocolo
validada       → pasó el protocolo, sin dinero real
forward        → demo o papel, ejecución real sin capital
live           → dinero real
                 salud: ok / observación / degradada
retirada       → estuvo en live y se sacó, con razón documentada
descartada     → murió antes de live, con razón documentada
```

Cada estrategia lleva un **ID** que la acompaña por todo el pipeline y un campo **Origen** que nunca
se borra. Las descartadas no se eliminan: el archivo de ideas muertas es lo que evita repetir el
mismo trabajo dentro de un año.

## Documento único por estrategia

Un solo archivo por estrategia, vivo, que se actualiza en vez de duplicarse.

```markdown
# [ID] — Nombre

Estado: | Origen: | Última actualización:

## Hipótesis
Una frase.

## Core logic
Quién está del otro lado, qué lo obliga, por qué no se ha arbitrado.

## Especificación
(spec completa y congelada)

## Datos
Fuente, rango, ajustes, zona horaria del feed.

## Resultados
### In-sample
Período, número de operaciones, métricas, curva.
### Out-of-sample
Período, métricas, degradación observada.
### Robustez
Barridos, meseta identificada.
### Monte Carlo / stress
Percentiles relevantes.

## Costos asumidos
Cifras y de dónde salieron.

## Decisiones de diseño
Cada parámetro con la razón por la que se eligió, fechada.

## Qué la mataría
Condiciones de falsación y umbrales de revisión.

## Log de research
Fecha — qué se probó — qué salió — qué se decidió.

## Registro live
Fecha de inicio, tamaño, desviaciones observadas entre real y simulado.
```

## Bitácora operativa

Diaria o por operación, según la frecuencia del sistema. Lo mínimo que sirve:

- Señal generada por el sistema, y señal ejecutada. Si difieren, por qué.
- Precio esperado contra precio obtenido. Ese diferencial es tu slippage real y sirve para corregir
  el backtest.
- Errores de ejecución, sin excepción. Los errores no registrados se repiten.
- Nada de estado de ánimo como justificación de una desviación. Si hubo desviación, se anota como
  error de proceso.

La bitácora no es un diario emocional. Es el instrumento con el que después vas a poder responder si
el sistema se degradó o si tú dejaste de ejecutarlo.

## Revisión periódica

Con calendario fijo, no cuando duele. En cada revisión:

1. Comparar métricas vivas contra las esperadas del backtest, en las mismas unidades.
2. Revisar los componentes del edge: distribución de disparos, payoff, frecuencia. Un cambio ahí
   aparece antes que en la curva de capital.
3. Verificar que el core logic siga siendo cierto en el mercado de hoy.
4. Registrar la decisión, incluso si la decisión es no hacer nada.

## Sobre reportar resultados a terceros

Si el usuario va a publicar o compartir métricas: períodos completos, sin recortar el tramo malo, con
costos incluidos y con la metodología a la vista. Un resultado sin período, sin costos y sin número
de operaciones no es un resultado.
