---
name: tis-riesgo-portafolio
description: "Gestión de riesgo, position sizing y construcción de portafolio de sistemas según Trade It Simple. Activar cuando el usuario pregunte cuánto arriesgar, cómo calcular el tamaño de posición, hable de Kelly, R, apalancamiento, correlación entre estrategias, asignación de capital, rebalanceo, o cuando combine varios sistemas."
---

# Riesgo, sizing y portafolio

Aplica siempre `tis-estilo`. Este skill se apoya en los anteriores: sin validación previa,
dimensionar es dimensionar humo.

## 1. La unidad es R

R es la cantidad que pierdes si el stop se ejecuta. Todo se mide en R: la expectancia, el drawdown,
el resultado del mes. Pensar en dólares hace que el tamaño cambie por razones emocionales; pensar en
R hace que el tamaño sea una consecuencia aritmética.

**Nunca más de 2% del capital por operación.** Y el 2% es techo, no objetivo.

Cálculo básico:

```
Tamaño = (Capital × Riesgo%) / (Distancia al stop en precio × valor del punto)
```

Si el resultado da una fracción imposible de operar en tu instrumento, el problema es el instrumento
o el capital, no la regla. No se redondea hacia arriba.

## 2. Métodos de sizing

| Método | Qué hace | Cuándo tiene sentido |
|---|---|---|
| Fixed fractional | Porcentaje constante del capital por operación | Punto de partida por defecto, simple y robusto |
| Ajustado por volatilidad | Normaliza el riesgo según la volatilidad del activo | Cuando operas varios instrumentos con volatilidades distintas |
| Kelly fraccionado | Optimiza crecimiento geométrico, se usa a una fracción del completo | Solo con expectancia estimada de forma confiable y muchas operaciones |

Sobre Kelly: existe como opción legítima, no se descarta por dogma. Pero Kelly completo asume que
conoces tu ventaja con precisión, y nadie la conoce con precisión. Si tu estimación de expectancia
está inflada, Kelly amplifica el error hasta la ruina. Fracciones conservadoras, siempre.

## 3. Riesgo de ruina y la trampa del capital con presión

Hay un patrón que arruina cuentas y que no es psicológico, es metodológico: **capital que tiene un
trabajo que hacer**. Cuando el dinero tiene que rendir cierta cantidad en cierto plazo — pagar algo,
reemplazar un ingreso, demostrarle algo a alguien — la urgencia empuja a operar más grande justo en
el peor momento, que es después de una racha perdedora.

La corrección no es "controla tus emociones". Es que el tamaño lo determine una fórmula fijada de
antemano y que el capital operado no tenga obligaciones externas.

Antes de dimensionar, revisa con el usuario:
- Cuál es el drawdown máximo que puede tolerar sin cambiar de comportamiento.
- Qué pasaría con su vida si ese drawdown ocurre mañana y dura ocho meses.
- Si la respuesta incomoda, el tamaño está mal, no la estrategia.

## 4. Portafolio de sistemas

La descorrelación que importa es **entre sistemas**, no entre activos. Dos estrategias de
seguimiento de tendencia en instrumentos distintos suelen perder en las mismas semanas: son el mismo
sistema con dos nombres.

Para combinar:

- Mide la correlación entre las **curvas de retornos diarios de cada sistema**, no entre los precios
  de los activos.
- Asigna por contribución al riesgo, no por peso igual. Un sistema con el doble de volatilidad y el
  mismo peso nominal está aportando el doble de riesgo.
- Revisa la correlación en los tramos malos por separado. Las correlaciones tienden a subir
  precisamente cuando necesitas que bajen.
- Métricas a nivel portafolio, no solo a nivel sistema: el drawdown del conjunto no es el promedio
  de los drawdowns individuales.

Regla de incorporación: un sistema nuevo entra si mejora el perfil de riesgo del conjunto, no si
tiene buenas métricas por sí solo.

## 5. Rebalanceo

Se define de antemano: frecuencia, umbral de desvío y qué se hace con un sistema en revisión.
Rebalancear por sensación es reintroducir discrecionalidad por la puerta de atrás.

## 6. Reglas de reducción y apagado

- **Drawdown moderado del sistema** → se reduce tamaño. El sistema sigue corriendo.
- **Drawdown máximo histórico documentado** → se apaga para revisión de edge decay, con protocolo
  escrito.
- **El régimen de mercado nunca apaga nada.** Si un régimen te preocupa, eso pertenece al diseño de
  los filtros del sistema, no a una decisión discrecional de la mañana.

Todos estos umbrales se escriben antes de necesitarlos. Una regla de riesgo decidida en medio de un
drawdown no es una regla, es una reacción.
