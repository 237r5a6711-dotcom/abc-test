@echo off
REM Quick Start Script for Video Streaming Solution (Windows)

echo ======================================
echo Video Streaming Solution - Quick Start
echo ======================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.6 or higher
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Check if requirements are installed
echo Checking requirements...
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo OpenCV not found. Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
) else (
    echo [OK] Requirements already installed
)
echo.

REM Ask user what they want to run
echo What would you like to run?
echo.
echo 1) Transmitter (send video from webcam)
echo 2) Receiver (receive and display video)
echo 3) Both (testing on same computer)
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto transmitter
if "%choice%"=="2" goto receiver
if "%choice%"=="3" goto both
echo Invalid choice
pause
exit /b 1

:transmitter
echo.
echo Starting Transmitter...
echo Default settings: 640x480 @ 30fps
echo.
set /p custom="Use custom settings? (y/N): "
if /i "%custom%"=="y" (
    set /p width="Width (default 640): "
    if "%width%"=="" set width=640
    set /p height="Height (default 480): "
    if "%height%"=="" set height=480
    set /p fps="FPS (default 30): "
    if "%fps%"=="" set fps=30
    set /p quality="Quality 1-100 (default 80): "
    if "%quality%"=="" set quality=80
    echo.
    echo Starting transmitter with custom settings...
    python transmitter.py --width %width% --height %height% --fps %fps% --quality %quality%
) else (
    echo.
    echo Starting transmitter with default settings...
    python transmitter.py
)
goto end

:receiver
echo.
set /p host="Transmitter IP address (default 127.0.0.1): "
if "%host%"=="" set host=127.0.0.1
echo.
echo Starting receiver...
echo Connecting to %host%:9999
echo.
python receiver.py --host %host%
goto end

:both
echo.
echo Starting both transmitter and receiver...
echo This will open two windows
echo.
echo Starting transmitter...
start "Transmitter" python transmitter.py
echo Waiting 3 seconds for transmitter to start...
timeout /t 3 /nobreak >nul
echo Starting receiver...
python receiver.py
goto end

:end
pause
