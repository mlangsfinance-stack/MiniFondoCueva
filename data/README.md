# Carga tus datos aquí

Este repo **no trae precios de mercado**, y es a propósito. Las series que se usaron en los
ejemplos son de proveedores con licencia (Norgate para el índice, Darwinex para el CFD) y no se
pueden regalar. Los tuyos los pones tú, en esta carpeta.

Nada de lo que dejes aquí se sube a ningún sitio: la carpeta está excluida del control de versiones.

## Qué formato tiene que tener

Un CSV con una fila por vela y estas columnas en la primera fila:

```
fecha,open,high,low,close
```

Así de simple. Un ejemplo de las tres primeras líneas:

```
fecha,open,high,low,close
2016-01-04,4304.75,4324.50,4192.25,4197.00
2016-01-05,4200.50,4243.75,4185.00,4202.75
```

Detalles que importan:

- **Los nombres de las columnas tienen que ser esos.** Si tu archivo trae `Date`, `Open`, `High`…
  también vale: se reconocen en inglés y sin distinguir mayúsculas. Lo que no vale es `Apertura`
  o `Precio de cierre`.
- **`volume` es opcional.** Si lo tienes, déjalo; si no, no pasa nada.
- **Las fechas, en orden y sin repetir.** Si hay duplicados se queda el último.
- **Formato `.parquet` también sirve**, si ya trabajas con él.
- El nombre del archivo da igual. `NDX_D1.csv`, `mi_nasdaq.csv`, lo que quieras.

## De dónde sacarlos

**TradingView.** Abre el gráfico en temporalidad diaria, menú de exportación (los tres puntos
arriba a la derecha del panel de datos) → Exportar datos del gráfico. Te baja un CSV listo.

**MetaTrader 5.** Herramientas → Copiar datos históricos, elige el símbolo y D1, y exporta a CSV.
Ojo con la zona horaria del servidor de tu bróker, que casi nunca es la tuya.

**Tu bróker.** Casi todos tienen una opción de exportar histórico en la plataforma web.

**Yahoo Finance.** Gratis y suficiente para practicar, aunque con huecos y sin ajustar bien los
dividendos en algunos casos. Para aprender el proceso sirve; para decidir con dinero, no.

## Un aviso sobre la calidad del dato

El método TIS dice que la serie tiene que ser de fuente fiable y verificable. Con datos gratuitos
vas a encontrar huecos, precios de apertura inventados y ajustes raros en fechas antiguas. Eso no
te impide aprender a validar, pero sí te impide sacar conclusiones sobre si algo es operable.

Hay una trampa concreta que conviene conocer, y está documentada en el repo: en la serie del índice
que se usó para los ejemplos, antes del año 2000 el precio de apertura es igual al cierre del día
anterior, porque el índice cash no tiene apertura real. Cualquier regla que mire el `open` —como el
patrón 80-20— da resultados falsos en ese tramo. Mira tus datos antes de fiarte de ellos.

## Cuando ya lo tengas

En Windows, doble clic en `VALIDAR.bat`: te lista lo que haya aquí y eliges por número.

En Mac o Linux, desde la Terminal en la carpeta del repo:

```
.venv/bin/python codigo/validar.py 001 data/TU_ARCHIVO.csv
```

Si algo falla con las columnas, el mensaje te dice exactamente cuáles faltan y cuáles encontró.
