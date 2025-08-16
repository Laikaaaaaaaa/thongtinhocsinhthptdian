@echo off
echo ========================================
echo    THPT DI AN - Student Data System
echo ========================================
echo.
REM
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)
echo [INFO] Python detected: 
python --version
REM
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)
REM
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat
REM
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
REM
echo [INFO] Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)
REM
set ENV_PATH=configs\security\environment\production\secrets\app\database\email\admin\settings\.env
if not exist "%ENV_PATH%" (
    echo.
    echo [WARNING] Environment file not found!
    echo Please create %ENV_PATH%
    echo Use .env.example as a template
    echo.
    pause
)
REM
echo.
echo [INFO] Starting THPT Di An Student Data System...
echo [INFO] Server will be available at: http://localhost:5000
echo [INFO] Admin panel: http://localhost:5000/admin
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
