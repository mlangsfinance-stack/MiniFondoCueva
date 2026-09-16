# Hxxx — <nombre corto>

- **Fecha:** AAAA-MM-DD
- **Fuente:** observación propia / literatura (cita) / barrido de datos / fallo de sistema Exxx
- **Familia de edge:** continuación · reversión · volatilidad · estacional · relativo
- **Estado:** idea → tendencia → prototipo → validación → descartada (con tramo y motivo)
- **Tests acumulados sobre esta hipótesis:** 0 (se actualiza; cada variante cuenta)

## 1. Observación
Qué se ha visto, dónde, en qué timeframe, cuántas veces. Sin interpretar todavía.

## 2. Mecanismo
Por qué debería existir. Familia: estructural / conductual / riesgo / fricción. Una o dos frases.
Si no hay mecanismo, decirlo: la evidencia exigida sube.

## 3. Universo y timeframe
Dónde se espera que funcione y dónde NO. Activos concretos, barra, sesión.

## 4. Evento
Condición observable al cierre de la barra, sin look-ahead. Escrita como pseudocódigo:
```
evento = (adx14 > 30) & (+DI > -DI) & (low <= ema20) & (close > ema20)
```

## 5. Predicción falsable
"Tras el evento, el retorno a h barras es mayor que el incondicional en al menos X."
Horizonte principal: h = __. Magnitud esperada: __ (≥ 3× el coste de ida y vuelta).

## 6. Métrica que decide
Cuál de `tendencies` responde: exceso de retorno / % positivo / p_supera_alto / expansión de rango.

## 7. Criterio de muerte (escrito ANTES de correr nada)
Se descarta si: n < 100 · exceso ≤ 0 en el horizonte principal · |t| < 2 · p-valor > 0.05
(o > 0.01 si viene de barrido). Tres variantes fallidas del evento = muerta.

## 8. Coste esperado
Coste de ida y vuelta del activo: __ %. Exceso esperado: __ %. Ratio: __.

---

## Resultado del test de tendencia
(pegar la tabla de `codigo/scripts/01_tendencia.py`, fecha, datos usados, seed si sintético)

## Decisión
Pasa a prototipo / descartada en tramo __ por __. Qué se aprendió.
