@echo off
REM Reliable Setup Script for AI Pattern Detector (Windows)
REM This script ensures all dependencies are installed and the environment is ready

echo.
echo ========================================
echo   AI Pattern Detector Setup (Windows)
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)
python --version
echo [OK] Python detected
echo.

REM Check pip
echo Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed. Please install pip.
    exit /b 1
)
echo [OK] pip found
echo.

REM Virtual environment (optional but recommended)
if "%VIRTUAL_ENV%"=="" (
    echo Virtual environment not detected
    set /p CREATE_VENV="Create virtual environment? (recommended) [Y/n] "
    if /i not "%CREATE_VENV%"=="n" (
        echo Creating virtual environment...
        python -m venv venv
        if errorlevel 1 (
            echo [ERROR] Failed to create virtual environment
            exit /b 1
        )
        echo [OK] Virtual environment created
        echo.
        echo [INFO] To activate virtual environment, run:
        echo        venv\Scripts\activate
        echo.
    )
) else (
    echo [OK] Virtual environment already active: %VIRTUAL_ENV%
    echo.
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip (continuing anyway)
) else (
    echo [OK] pip upgraded
)
echo.

REM Install dependencies
echo Installing dependencies...
if not exist "ai_tools\requirements.txt" (
    echo [ERROR] requirements.txt not found!
    exit /b 1
)

python -m pip install -r ai_tools\requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Verify installation
echo Verifying installation...
python check_environment.py
if errorlevel 1 (
    echo [WARNING] Some optional components may not be available (this is OK)
) else (
    echo [OK] Installation verified successfully!
)
echo.

REM Success message
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Start the dashboard:
echo      streamlit run dashboard\app.py
echo.
echo   2. Or run tests:
echo      python demo_dashboard.py
echo.
echo   3. Check environment:
echo      python check_environment.py
echo.

if exist "venv" (
    if "%VIRTUAL_ENV%"=="" (
        echo [INFO] Remember to activate virtual environment:
        echo        venv\Scripts\activate
        echo.
    )
)

echo For more information, see:
echo   - Quick Start: QUICKSTART.md
echo   - Documentation: docs\README.md
echo.

pause

