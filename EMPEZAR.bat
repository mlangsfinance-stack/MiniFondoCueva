@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
cd /d "%~dp0"
title MINI FONDO - puesta en marcha

echo.
echo ================================================================
echo   MINI FONDO - Trade It Simple
echo   Esto prepara el repo y comprueba que todo funciona.
echo   Solo hay que hacerlo una vez. Tarda cosa de un minuto.
echo ================================================================
echo.

rem --- 1. Buscar un Python que de verdad funcione -----------------------
rem  Windows suele traer un "python.exe" de 0 bytes en WindowsApps que solo abre
rem  la Microsoft Store y sale con codigo 9009. Por eso no basta con "where python":
rem  probamos que el interprete sepa imprimir algo antes de darlo por bueno.
set "PY="
call :probar py -3
call :probar python
call :probar python3

if not defined PY (
  echo   [ERROR] En este ordenador no hay Python instalado.
  echo.
  echo       Te abro la pagina de descarga. Baja el boton amarillo grande.
  echo.
  echo       MUY IMPORTANTE: en la PRIMERA pantalla del instalador, abajo,
  echo       marca la casilla  "Add python.exe to PATH"  antes de pulsar
  echo       Install Now. Es el unico paso donde te puedes equivocar.
  echo.
  echo       Cuando termine, cierra esta ventana y vuelve a hacer doble clic
  echo       en EMPEZAR.bat.
  echo.
  start "" "https://www.python.org/downloads/"
  pause
  exit /b 1
)

%PY% -c "import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>&1
if errorlevel 1 (
  for /f "delims=" %%v in ('%PY% -c "import sys;print(sys.version.split()[0])" 2^>nul') do set "VER=%%v"
  echo   [ERROR] Tu Python es la version !VER! y hace falta 3.10 o mas nueva.
  echo.
  echo       Instala la ultima desde https://www.python.org/downloads/
  echo       ^(marca "Add python.exe to PATH"^) y vuelve a ejecutar esto.
  echo.
  start "" "https://www.python.org/downloads/"
  pause
  exit /b 1
)
echo   [1/4] Python encontrado.

rem --- 2. Entorno aislado ----------------------------------------------
if not exist ".venv\Scripts\python.exe" (
  echo   [2/4] Creando el entorno aislado ^(carpeta .venv^)...
  %PY% -m venv .venv
  if errorlevel 1 goto :error
) else (
  echo   [2/4] El entorno ya existia.
)

rem --- 3. Dependencias --------------------------------------------------
echo   [3/4] Instalando lo necesario ^(numpy, pandas, pytest^)...
".venv\Scripts\python.exe" -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto :error

rem --- 4. Comprobacion --------------------------------------------------
echo   [4/4] Comprobando que el motor funciona...
echo.
".venv\Scripts\python.exe" -m pytest -q
if errorlevel 1 goto :error

echo.
echo ================================================================
echo   LISTO. El motor funciona.
echo ================================================================
echo.
echo   Ahora la prueba importante: el PLACEBO.
echo.
echo   Vamos a correr la estrategia de ejemplo sobre precios INVENTADOS
echo   por ordenador. Ruido puro, sin nada dentro. Como no hay nada que
echo   encontrar, tiene que salir RECHAZADA.
echo.
echo   Vas a ver varias lineas que dicen FALLA. Esa es la buena noticia.
echo.
pause
echo.
".venv\Scripts\python.exe" codigo\validar.py 001 --sintetico --rapido

echo.
echo ================================================================
echo   Has visto lineas FALLA y el veredicto DESCARTADA. Correcto.
echo.
echo   Siguiente paso, en este orden:
echo.
echo     1. Abre  EMPIEZA_AQUI.md   (la guia, se lee con el Bloc de notas)
echo     2. Abre  reportes\ndx_charts.html  con doble clic: las curvas
echo     3. Cuando tengas tus datos, doble clic en  VALIDAR.bat
echo ================================================================
echo.
pause
exit /b 0

rem ----------------------------------------------------------------------
:probar
rem  Da por bueno "%*" como interprete solo si imprime 42. Asi descartamos
rem  el alias vacio de la Microsoft Store, que sale con 9009 sin imprimir nada.
if defined PY goto :eof
for /f "delims=" %%v in ('%* -c "print(42)" 2^>nul') do (
  if "%%v"=="42" set "PY=%*"
)
goto :eof

:error
echo.
echo   [ERROR] Algo ha fallado. Copia el texto de arriba y mandamelo.
echo.
pause
exit /b 1
