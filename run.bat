@echo off
REM Archivo BAT para iniciar servidor Django en un venv y abrir navegador
REM Configura estas variables según tu proyecto

set DJANGO_PROJECT_PATH=G:\Personal\Dev\POS
set VENV_PATH=G:\Personal\Dev\POS\venv
set PORT=8000
set MOSTRAR_VENTANA=false  REM Cambia a false si no quieres ver la ventana

REM Navegar al directorio del proyecto
cd /d %DJANGO_PROJECT_PATH%

REM Activar el entorno virtual
call "%VENV_PATH%\Scripts\activate"

REM Iniciar el servidor Django según la configuración de MOSTRAR_VENTANA
if "%MOSTRAR_VENTANA%"=="true" (
    start "Servidor Django" cmd /k python core/manage.py runserver %PORT%
) else (
    start /B python core/manage.py runserver %PORT%
)

REM Esperar unos segundos para que el servidor se inicie
timeout /t 5 /nobreak >nul

REM Abrir el navegador con la URL del servidor
start "" http://localhost:%PORT%/

echo Servidor Django iniciado en el entorno virtual y navegador abierto en http://localhost:%PORT%/
echo Configuración actual: MOSTRAR_VENTANA=%MOSTRAR_VENTANA%