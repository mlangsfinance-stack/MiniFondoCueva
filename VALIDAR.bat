@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title MINI FONDO - validar una estrategia

echo.
echo ================================================================
echo   VALIDAR UNA ESTRATEGIA
echo ================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo   [ERROR] Todavia no has preparado el repo.
  echo.
  echo       Haz doble clic primero en  EMPEZAR.bat  y cuando termine
  echo       vuelve aqui.
  echo.
  pause
  exit /b 1
)

rem --- 1. Elegir estrategia ---------------------------------------------
echo   Que estrategia quieres correr:
echo.
echo     1  Kaufman - ruptura de canal con filtro de ruido
echo     2  Kaufman - reversion de 2 dias a favor de la tendencia
echo     3  Raschke - Holy Grail
echo     4  Raschke - patron 80-20
echo.
set "ID="
set /p "OPC=  Escribe 1, 2, 3 o 4 y pulsa Enter: "
set "OPC=%OPC: =%"
if "%OPC%"=="1" set "ID=001"
if "%OPC%"=="2" set "ID=002"
if "%OPC%"=="3" set "ID=003"
if "%OPC%"=="4" set "ID=004"
if not defined ID (
  echo.
  echo   [ERROR] Eso no era 1, 2, 3 ni 4. Vuelve a abrir el archivo.
  pause
  exit /b 1
)

rem --- 2. Elegir datos ---------------------------------------------------
echo.
set "N=0"
for %%f in (data\*.csv data\*.parquet) do (
  set /a N+=1
  set "F!N!=%%f"
  echo     !N!  %%~nxf
)

if "%N%"=="0" (
  echo   En la carpeta  data  no hay ningun archivo de precios.
  echo.
  echo   Para usar los tuyos: guarda ahi un CSV con una fila por dia y estas
  echo   columnas en la primera fila:   fecha, open, high, low, close
  echo.
  echo   Mientras tanto corremos el PLACEBO, sobre precios inventados.
  echo   Tiene que salir DESCARTADA: es la prueba de que el examen funciona.
  echo.
  pause
  echo.
  chcp 65001 >nul 2>&1
  ".venv\Scripts\python.exe" codigo\validar.py %ID% --sintetico --rapido
  goto :fin
)

echo     0  ninguno, correr el placebo sobre precios inventados
echo.
set /p "OPD=  Escribe el numero del archivo que quieres usar: "
set "OPD=%OPD: =%"

if "%OPD%"=="0" (
  echo.
  chcp 65001 >nul 2>&1
  ".venv\Scripts\python.exe" codigo\validar.py %ID% --sintetico --rapido
  goto :fin
)

set "DATOS=!F%OPD%!"
if not defined DATOS (
  echo.
  echo   [ERROR] Ese numero no estaba en la lista. Vuelve a abrir el archivo.
  pause
  exit /b 1
)

echo.
echo   Corriendo la estrategia %ID% sobre !DATOS!
echo   Esto tarda un rato. No cierres la ventana.
echo.
chcp 65001 >nul 2>&1
".venv\Scripts\python.exe" codigo\validar.py %ID% "!DATOS!"

:fin
echo.
echo ================================================================
echo   El acta completa te ha quedado guardada dentro de la carpeta
echo   reportes, en un archivo llamado RESUMEN.md
echo.
echo   Si no entiendes algun numero, el diccionario esta al final de
echo   EMPIEZA_AQUI.md
echo ================================================================
echo.
pause
exit /b 0
