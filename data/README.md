# data/

Aquí van los CSV/parquet de mercado. No se versionan.

Formato esperado por los agentes: una fila por vela, columnas
`fecha, open, high, low, close, volume` (fecha en UTC o con la zona declarada en `hipotesis.md`).

Nombre sugerido: `<SIMBOLO>_<TF>.csv`, p. ej. `XAUUSD_1H.csv`, `NAS100_1H.csv`.
