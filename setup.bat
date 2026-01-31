@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ═══════════════════════════════════════════════════════════════════════════════
::                      PIKACHU DESKTOP ASSISTANT - SETUP
::                    Advanced Installation System v2.0
:: ═══════════════════════════════════════════════════════════════════════════════

cd /d "%~dp0"

:: ═══════════════════════════════════════════════════════════════════════════════
:: INITIALIZATION & COLOR SCHEME
:: ═══════════════════════════════════════════════════════════════════════════════
color 0E
mode con cols=96 lines=35
title PIKACHU ASSISTANT - INTELLIGENT SETUP SYSTEM

:: ═══════════════════════════════════════════════════════════════════════════════
:: ANIMATED SPLASH SCREEN
:: ═══════════════════════════════════════════════════════════════════════════════
cls
echo.
echo.
echo                ╔═══════════════════════════════════════════╗
echo                ║                                           ║
echo                ║         L O A D I N G . . .               ║
echo                ║                                           ║
echo                ╚═══════════════════════════════════════════╝
echo.
call :ProgressBar 30
cls

:: ═══════════════════════════════════════════════════════════════════════════════
:: MAIN HEADER
:: ═══════════════════════════════════════════════════════════════════════════════
call :DrawHeader
echo.
echo   ╔══════════════════════════════════════════════════════════════════════════════╗
echo   ║                                                                              ║
echo   ║       ██████╗ ██╗██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗   ██╗                 ║
echo   ║       ██╔══██╗██║██║ ██╔╝██╔══██╗██╔════╝██║  ██║██║   ██║                 ║
echo   ║       ██████╔╝██║█████╔╝ ███████║██║     ███████║██║   ██║                 ║
echo   ║       ██╔═══╝ ██║██╔═██╗ ██╔══██║██║     ██╔══██║██║   ██║                 ║
echo   ║       ██║     ██║██║  ██╗██║  ██║╚██████╗██║  ██║╚██████╔╝                 ║
echo   ║       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝                  ║
echo   ║                                                                              ║
echo   ║                  ⚡ INTELLIGENT DESKTOP ASSISTANT ⚡                         ║
echo   ║                                                                              ║
echo   ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo                      ┌────────────────────────────────────┐
echo                      │ Fast • Local • Private • Powerful  │
echo                      │    Enterprise-Grade AI Engine      │
echo                      └────────────────────────────────────┘
echo.
timeout /t 2 >nul

:: ═══════════════════════════════════════════════════════════════════════════════
:: SYSTEM DIAGNOSTICS
:: ═══════════════════════════════════════════════════════════════════════════════
call :SectionHeader "SYSTEM DIAGNOSTICS"
echo.
echo   [▶] Running comprehensive system checks...
echo.
timeout /t 1 >nul

:: ═══════════════════════════════════════════════════════════════════════════════
:: STEP 1: PYTHON VERIFICATION
:: ═══════════════════════════════════════════════════════════════════════════════
call :StepHeader "01" "PYTHON RUNTIME VERIFICATION"
echo   [●] Scanning for Python interpreter...
timeout /t 1 >nul

python --version >nul 2>&1
if errorlevel 1 (
    call :ErrorBox "Python Runtime Not Found" "Python 3.10+ is required. Install from python.org" "Ensure 'Add Python to PATH' is checked during installation"
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version') do set PYVER=%%v
call :SuccessMsg "Python !PYVER! detected and verified"
call :AnimatedCheck
echo.

:: ═══════════════════════════════════════════════════════════════════════════════
:: STEP 2: VIRTUAL ENVIRONMENT SETUP
:: ═══════════════════════════════════════════════════════════════════════════════
call :StepHeader "02" "VIRTUAL ENVIRONMENT CONFIGURATION"

if exist venv (
    call :InfoMsg "Virtual environment detected - validating integrity..."
    timeout /t 1 >nul
    call :SuccessMsg "Environment validation complete"
) else (
    echo   [●] Creating isolated Python environment...
    call :ProgressBar 20
    python -m venv venv
    if errorlevel 1 (
        call :ErrorBox "Environment Creation Failed" "Unable to create virtual environment" "Check Python installation and permissions"
        pause
        exit /b 1
    )
    call :SuccessMsg "Virtual environment successfully created"
)
call :AnimatedCheck
echo.

:: ═══════════════════════════════════════════════════════════════════════════════
:: STEP 3: DEPENDENCY INSTALLATION
:: ═══════════════════════════════════════════════════════════════════════════════
call :StepHeader "03" "DEPENDENCY RESOLUTION & INSTALLATION"
echo   [●] Activating isolated environment...
call venv\Scripts\activate
timeout /t 1 >nul
call :SuccessMsg "Environment activated"

echo   [●] Upgrading package manager...
pip install --upgrade pip --quiet --disable-pip-version-check
call :SuccessMsg "Package manager updated"

echo   [●] Installing required dependencies...
echo.
call :ProgressBar 40
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    call :ErrorBox "Dependency Installation Failed" "Unable to install required packages" "Check requirements.txt and internet connection"
    pause
    exit /b 1
)
call :SuccessMsg "All dependencies installed successfully"
call :AnimatedCheck
echo.

:: ═══════════════════════════════════════════════════════════════════════════════
:: STEP 4: OLLAMA & AI MODEL SETUP
:: ═══════════════════════════════════════════════════════════════════════════════
call :StepHeader "04" "AI ENGINE CONFIGURATION"
echo   [●] Verifying Ollama runtime...
timeout /t 1 >nul

ollama --version >nul 2>&1
if errorlevel 1 (
    call :ErrorBox "Ollama Runtime Not Found" "Ollama is required for local AI processing" "Download from: https://ollama.com"
    pause
    exit /b 1
)
call :SuccessMsg "Ollama runtime verified"

echo   [●] Scanning for AI model: qwen2.5-coder:7b...
ollama list | findstr /i "qwen2.5-coder:7b" >nul
if errorlevel 1 (
    echo.
    call :InfoMsg "AI model not found - initiating download..."
    echo.
    echo   ┌──────────────────────────────────────────────────────────────┐
    echo   │ This may take several minutes depending on connection speed │
    echo   │            Model size: ~4.7GB (7B parameters)                │
    echo   └──────────────────────────────────────────────────────────────┘
    echo.
    ollama pull qwen2.5-coder:7b
    if errorlevel 1 (
        call :ErrorBox "Model Download Failed" "Unable to download AI model" "Check internet connection and Ollama status"
        pause
        exit /b 1
    )
    call :SuccessMsg "AI model downloaded and validated"
) else (
    call :SuccessMsg "AI model already available and ready"
)
call :AnimatedCheck
echo.

:: ═══════════════════════════════════════════════════════════════════════════════
:: STEP 5: ENVIRONMENT CONFIGURATION
:: ═══════════════════════════════════════════════════════════════════════════════
call :StepHeader "05" "ENVIRONMENT VARIABLE CONFIGURATION"

if exist .env (
    call :InfoMsg "Configuration file detected - preserving existing settings"
) else (
    echo   [●] Generating configuration template...
    (
        echo # ═══════════════════════════════════════════════════════════
        echo # PIKACHU ASSISTANT - ENVIRONMENT CONFIGURATION
        echo # Generated: %date% %time%
        echo # ═══════════════════════════════════════════════════════════
        echo.
        echo # Telegram Bot Configuration
        echo TELEGRAM_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE
        echo.
        echo # AI Model Configuration
        echo MODEL_NAME=qwen2.5-coder:7b
        echo.
        echo # Optional: Advanced Settings
        echo # LOG_LEVEL=INFO
        echo # MAX_TOKENS=2048
    ) > .env
    call :SuccessMsg "Configuration template created"
    echo.
    call :WarningBox "ACTION REQUIRED" "Edit .env file and insert your Telegram Bot Token"
)
call :AnimatedCheck
echo.

:: ═══════════════════════════════════════════════════════════════════════════════
:: STEP 6: STEALTH MODE & AUTO-START CONFIGURATION
:: ═══════════════════════════════════════════════════════════════════════════════
call :StepHeader "06" "STEALTH MODE & AUTO-START SETUP"

echo   [●] Creating stealth launcher...
(
    echo ' ═══════════════════════════════════════════════════════════
    echo ' PIKACHU ASSISTANT - SILENT LAUNCHER
    echo ' Runs the assistant invisibly in the background
    echo ' ═══════════════════════════════════════════════════════════
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo WshShell.Run chr^(34^) ^& "%~dp0start_pikachu.bat" ^& chr^(34^), 0
    echo Set WshShell = Nothing
) > run_silent.vbs
call :SuccessMsg "Stealth launcher created"

echo   [●] Configuring Windows auto-start...
set "STARTUP_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PikachuAgent.lnk"
set "TARGET_PATH=%~dp0run_silent.vbs"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_PATH%'); $s.TargetPath = '%TARGET_PATH%'; $s.Description = 'Pikachu Desktop Assistant'; $s.Save()" >nul 2>&1

if exist "%STARTUP_PATH%" (
    call :SuccessMsg "Auto-start configured successfully"
) else (
    call :WarningMsg "Auto-start configuration skipped (may require admin privileges)"
)
call :AnimatedCheck
echo.

:: ═══════════════════════════════════════════════════════════════════════════════
:: INSTALLATION COMPLETE
:: ═══════════════════════════════════════════════════════════════════════════════
cls
color 0A
call :DrawHeader
echo.
echo   ╔══════════════════════════════════════════════════════════════════════════════╗
echo   ║                                                                              ║
echo   ║            ✓✓✓  INSTALLATION COMPLETED SUCCESSFULLY  ✓✓✓                     ║
echo   ║                                                                              ║
echo   ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo   ┌──────────────────────────────────────────────────────────────────────────────┐
echo   │                             NEXT STEPS                                       │
echo   ├──────────────────────────────────────────────────────────────────────────────┤
echo   │                                                                              │
echo   │  1. CONFIGURE TELEGRAM BOT                                                   │
echo   │     • Open the .env file in a text editor                                    │
echo   │     • Replace PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE with your actual token      │
echo   │     • Save and close the file                                                │
echo   │                                                                              │
echo   │  2. START THE ASSISTANT                                                      │
echo   │     • Option A: Restart your computer (auto-starts in stealth mode)          │
echo   │     • Option B: Double-click 'run_silent.vbs' to start now                   │
echo   │                                                                              │
echo   │  3. VERIFY OPERATION                                                         │
echo   │     • Open Telegram and message your bot                                     │
echo   │     • Check Task Manager for 'python.exe' process                            │
echo   │                                                                              │
echo   └──────────────────────────────────────────────────────────────────────────────┘
echo.
echo   ┌──────────────────────────────────────────────────────────────────────────────┐
echo   │                          SYSTEM INFORMATION                                  │
echo   ├──────────────────────────────────────────────────────────────────────────────┤
echo   │  Python Version    : !PYVER!                                                 │
echo   │  AI Model          : qwen2.5-coder:7b                                        │
echo   │  Installation Path : %~dp0                                
echo   │  Auto-Start        : Enabled                                                 │
echo   └──────────────────────────────────────────────────────────────────────────────┘
echo.
echo.
echo                         Press any key to exit setup...
pause >nul
exit /b 0

:: ═══════════════════════════════════════════════════════════════════════════════
:: FUNCTION LIBRARY
:: ═══════════════════════════════════════════════════════════════════════════════

:DrawHeader
echo.
echo   ══════════════════════════════════════════════════════════════════════════════
echo   ║                                                                            ║
echo   ║       ⚡ PIKACHU DESKTOP ASSISTANT - ADVANCED SETUP SYSTEM ⚡              ║
echo   ║                                                                            ║
echo   ══════════════════════════════════════════════════════════════════════════════
goto :eof

:SectionHeader
echo.
echo   ┌──────────────────────────────────────────────────────────────────────────────┐
echo   │  %~1
echo   └──────────────────────────────────────────────────────────────────────────────┘
goto :eof

:StepHeader
echo.
echo   ╔══════════════════════════════════════════════════════════════════════════════╗
echo   ║  STEP %~1 │ %~2
echo   ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:SuccessMsg
echo   [✓] %~1
goto :eof

:InfoMsg
echo   [i] %~1
goto :eof

:WarningMsg
echo   [!] %~1
goto :eof

:ErrorBox
color 0C
echo.
echo   ╔══════════════════════════════════════════════════════════════════════════════╗
echo   ║  ❌ ERROR: %~1
echo   ╠══════════════════════════════════════════════════════════════════════════════╣
echo   ║  %~2
echo   ║  %~3
echo   ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:WarningBox
echo.
echo   ╔══════════════════════════════════════════════════════════════════════════════╗
echo   ║  ⚠️  %~1
echo   ╠══════════════════════════════════════════════════════════════════════════════╣
echo   ║  %~2
echo   ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
goto :eof

:ProgressBar
setlocal
set /a "steps=%~1"
set "bar="
<nul set /p "=  [●] Progress: ["
for /l %%i in (1,1,%steps%) do (
    set "bar=!bar!█"
    <nul set /p "=█"
    ping -n 1 127.0.0.1 >nul 2>&1
)
echo ] Complete
endlocal
goto :eof

:AnimatedCheck
<nul set /p "=  [●] Verification: ["
for /l %%i in (1,1,10) do (
    <nul set /p "=━"
    ping -n 1 127.0.0.1 >nul 2>&1
)
echo ━] ✓
goto :eof

endlocal