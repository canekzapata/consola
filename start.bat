@echo off
echo ============================================================
echo    📝 Editor de Escritura Avanzado
echo    Procesador de texto + Markov + IA + Web Search
echo ============================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verificar dependencias
echo Verificando dependencias...
echo.

python -c "import markovify" 2>nul
if errorlevel 1 (
    echo ⚠️  markovify no está instalado
    echo Instalando dependencias...
    pip install markovify flask flask-cors
    echo.
)

python -c "import flask" 2>nul
if errorlevel 1 (
    echo ⚠️  flask no está instalado
    echo Instalando dependencias...
    pip install markovify flask flask-cors
    echo.
)

python -c "import flask_cors" 2>nul
if errorlevel 1 (
    echo ⚠️  flask-cors no está instalado
    echo Instalando dependencias...
    pip install markovify flask flask-cors requests
    echo.
)

python -c "import requests" 2>nul
if errorlevel 1 (
    echo ⚠️  requests no está instalado
    echo Instalando dependencias...
    pip install requests
    echo.
)

echo ✓ Todas las dependencias están instaladas
echo.

REM Iniciar el servidor
echo 🚀 Iniciando servidor...
echo    URL: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python server-windows.py

pause
