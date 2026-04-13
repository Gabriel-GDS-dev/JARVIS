@echo off
REM Inicia o backend FastAPI e a interface Streamlit em janelas separadas.
REM Execute este arquivo dando duplo clique no Windows.

SET SCRIPT_DIR=%~dp0
CD /d "%SCRIPT_DIR%"

REM Verifica se existe ambiente virtual local em .venv ou venv dentro do projeto
SET VENV_PATH=
IF EXIST ".venv\Scripts\activate.bat" SET VENV_PATH=.venv
IF NOT DEFINED VENV_PATH IF EXIST "venv\Scripts\activate.bat" SET VENV_PATH=venv

REM Verifica se existe ambiente virtual no diretório pai do workspace (c:\Res)
IF NOT DEFINED VENV_PATH (
    pushd "..\.."
    IF EXIST ".venv\Scripts\activate.bat" SET VENV_PATH=..\..\.venv
    IF NOT DEFINED VENV_PATH IF EXIST "venv\Scripts\activate.bat" SET VENV_PATH=..\..\venv
    popd
)

IF NOT DEFINED VENV_PATH (
    echo Nao foi possivel encontrar o ambiente virtual em ".venv\Scripts\activate.bat", "venv\Scripts\activate.bat", "..\..\.venv\Scripts\activate.bat" ou "..\..\venv\Scripts\activate.bat".
    echo Certifique-se de instalar o ambiente e execute novamente.
    pause
    EXIT /b 1
)

SET "PYTHON_EXE=%VENV_PATH%\Scripts\python.exe"
IF NOT EXIST "%PYTHON_EXE%" (
    echo Nao foi possivel encontrar o Python em %PYTHON_EXE%.
    pause
    EXIT /b 1
)

start "Jarvis API" cmd /k "cd /d "%SCRIPT_DIR%" && "%PYTHON_EXE%" -m uvicorn app.main:app --app-dir "%SCRIPT_DIR%" --reload --port 8000"
timeout /t 2 /nobreak >nul
start "Jarvis Streamlit" cmd /k "cd /d "%SCRIPT_DIR%" && "%PYTHON_EXE%" -m streamlit run "%SCRIPT_DIR%interface\streamlit_app.py""
