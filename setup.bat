@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cd /d "%~dp0"
title ⚡ PIKACHU ASSISTANT - PREMIUM SETUP ⚡
color 0E

cls
echo.
echo.
echo      ██████╗ ██╗██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗   ██╗
echo      ██╔══██╗██║██║ ██╔╝██╔══██╗██╔════╝██║  ██║██║   ██║
echo      ██████╔╝██║█████╔╝ ███████║██║     ███████║██║   ██║
echo      ██╔═══╝ ██║██╔═██╗ ██╔══██║██║     ██╔══██║██║   ██║
echo      ██║     ██║██║  ██╗██║  ██║╚██████╗██║  ██║╚██████╔╝
echo      ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝
echo.
echo            ⚡  P I K A C H U   A S S I S T A N T  ⚡
echo.

color 06
echo   ⠀⢰⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀
echo   ⠀⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣾⣿
echo   ⠀⠘⢿⣿⣿⣿⣿⣦⣀⣀⣀⣄⣀⣀⣠⣀⣤⣶⣿⣿⣿⣿⣿⠇
echo   ⠀⠀⠈⠻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀
echo   ⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠋⠀⠀⠀
echo   ⠀⠀⠀⢠⣿⣿⡏⠆⢹⣿⣿⣿⣿⣿⣿⠒⠈⣿⣿⣿⣇⠀⠀⠀
echo   ⠀⠀⠀⣼⣿⣿⣷⣶⣿⣿⣛⣻⣿⣿⣿⣶⣾⣿⣿⣿⣿⡀⠀⠀
echo   ⠀⠀⠀⡁⠀⠈⣿⣿⣿⣿⢟⣛⡻⣿⣿⣿⣟⠀⠀⠈⣿⡇⠀⠀
echo   ⠀⠀⠀⢿⣶⣿⣿⣿⣿⣿⡻⣿⡿⣿⣿⣿⣿⣶⣶⣾⣿⣿⠀⠀
echo   ⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀
echo   ⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
echo.

color 0E
echo   ═══════════════════════════════════════════════════════════════════════
echo            ⚡  SYSTEM INITIALIZATION SEQUENCE ENGAGED  ⚡
echo   ═══════════════════════════════════════════════════════════════════════
echo.

:: ===================== STEP 1 =====================
echo   [1/5] Selecting Python Version...

py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py -3.11"
    echo   [✓] Found Python 3.11 (via Launcher)
    goto :FoundPython
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>nul') do set CUR_VER=%%v
if "!CUR_VER:~0,4!"=="3.11" (
    set "PYTHON_CMD=python"
    echo   [✓] Default Python is 3.11
    goto :FoundPython
)

if "!CUR_VER:~0,4!"=="3.10" set "PYTHON_CMD=python" & goto :FoundPython
if "!CUR_VER:~0,4!"=="3.12" set "PYTHON_CMD=python" & goto :FoundPython

color 0C
echo.
echo   [X] CRITICAL ERROR: Python 3.11 not found!
echo.
pause
exit /b 1

:FoundPython
echo.

:: ===================== STEP 2 =====================
echo   [2/5] configuring Environment...

if exist venv (
    echo   [i] Removing old environment to prevent conflicts...
    rmdir /s /q venv
)

echo   [+] Creating new environment using Python 3.11...
%PYTHON_CMD% -m venv venv

if errorlevel 1 (
    color 0C
    echo   [X] Failed to create environment.
    pause
    exit /b 1
)
echo   [✓] Environment created.
echo.

:: ===================== STEP 3 =====================
echo   [3/5] Installing Libraries...
call venv\Scripts\activate
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

if errorlevel 1 (
    color 0C
    echo   [X] Install Failed. Check internet.
    pause
    exit /b 1
)
echo   [✓] Libraries installed.
echo.

:: ===================== STEP 4 =====================
echo   [4/5] Checking AI Brain...
ollama list | findstr /i "qwen2.5-coder:7b" >nul
if errorlevel 1 (
    echo   [!] Downloading Model (This might take time)...
    ollama pull qwen2.5-coder:7b
) else (
    echo   [✓] AI Model ready.
)
echo.

:: ===================== STEP 5 =====================
echo   [5/5] Finalizing...

if not exist .env (
    (
        echo TELEGRAM_TOKEN=PASTE_TOKEN_HERE
        echo MODEL_NAME=qwen2.5-coder:7b
    ) > .env
    echo   [!] Created .env file. PLEASE ADD YOUR TOKEN!
)

(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo WshShell.Run chr^(34^) ^& "%~dp0start_pikachu.bat" ^& chr^(34^), 0
    echo Set WshShell = Nothing
) > run_silent.vbs

echo.
echo   ██████████████████████████████████████████████████████████████████████
echo                   ✅  SETUP COMPLETE — PIKACHU IS READY
echo   ██████████████████████████████████████████████████████████████████████
echo.
pause
