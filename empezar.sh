#!/usr/bin/env bash
# MINI FONDO - puesta en marcha (Mac / Linux).
# Uso:  bash empezar.sh
set -u
cd "$(dirname "$0")"

echo
echo "================================================================"
echo "  MINI FONDO - Trade It Simple"
echo "  Esto prepara el repo y comprueba que todo funciona."
echo "  Solo hay que hacerlo una vez. Tarda un par de minutos."
echo "================================================================"
echo

fallo() { echo; echo "[!] Algo ha fallado: $1"; echo; exit 1; }

# --- 1. Buscar Python ---------------------------------------------------
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
if [ -z "$PY" ]; then
  echo "[!] No encuentro Python 3.10 o superior."
  echo
  echo "    Mac:    brew install python   (o descargalo en https://www.python.org/downloads/)"
  echo "    Ubuntu: sudo apt install python3 python3-venv"
  echo
  echo "    Cuando lo tengas, vuelve a ejecutar: bash empezar.sh"
  exit 1
fi
echo "[1/4] Python encontrado ($($PY --version 2>&1))."

# --- 2. Entorno aislado -------------------------------------------------
if [ ! -x ".venv/bin/python" ]; then
  echo "[2/4] Creando el entorno aislado (.venv)..."
  "$PY" -m venv .venv || fallo "no he podido crear el entorno (en Ubuntu puede faltar python3-venv)"
else
  echo "[2/4] El entorno ya existia."
fi

# --- 3. Dependencias ----------------------------------------------------
echo "[3/4] Instalando lo necesario (numpy, pandas, pytest)..."
.venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt \
  || fallo "la instalacion de dependencias no ha terminado"

# --- 4. Comprobacion ----------------------------------------------------
echo "[4/4] Comprobando que el motor funciona..."
echo
.venv/bin/python -m pytest -q || fallo "los tests no pasan"

cat <<'TXT'

================================================================
  LISTO. El motor funciona.
================================================================

Ahora la prueba importante: el PLACEBO.
Corremos la estrategia de ejemplo sobre datos INVENTADOS, sin
ninguna senal real. Tiene que SALIR RECHAZADA. Si pasara, el
motor estaria roto.

TXT
read -r -p "Pulsa Enter para correr el placebo... " _ || true
echo
.venv/bin/python codigo/validar.py 001 --sintetico --rapido

cat <<'TXT'

================================================================
  Has visto varias lineas FALLA. Eso es lo correcto.

  Siguiente paso: abre EMPIEZA_AQUI.md
  y, para ver las curvas sin instalar nada mas, abre
  reportes/ndx_charts.html en tu navegador.
================================================================

TXT
