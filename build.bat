@echo off
REM Build script for AI Assistant executable

echo ============================================
echo Building AI Assistant v1.0.0
echo ============================================
echo.

REM Install PyInstaller if not present
echo [1/4] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
) else (
    echo PyInstaller already installed.
)
echo.

REM Clean previous builds
echo [2/4] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "AI_Assistant.spec" del "AI_Assistant.spec"
echo.

REM Build executable
echo [3/4] Building executable (this may take a few minutes)...
pyinstaller --name="AI_Assistant" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data "config.json;." ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=google.genai ^
    --hidden-import=pystray ^
    --collect-all google-genai ^
    --collect-all pystray ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo.

REM Success
echo [4/4] Build complete!
echo.
echo ============================================
echo Executable location: dist\AI_Assistant.exe
echo ============================================
echo.
echo IMPORTANT: Before running the .exe:
echo 1. Copy 'dist\AI_Assistant.exe' to a new folder
echo 2. Create a 'config.json' file in the same folder
echo 3. Add your Gemini API key(s) to config.json
echo.
pause
