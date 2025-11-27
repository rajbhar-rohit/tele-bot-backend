@echo off
title Instagram Downloader - First Time Setup
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    FIRST TIME SETUP                     ║
echo ║              Instagram Content Downloader               ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org
    echo 2. Download Python 3.8 or newer
    echo 3. Run the installer and check "Add Python to PATH"
    echo 4. Run this setup again
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python found!
    python --version
)

echo.
echo 📦 Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install packages!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed successfully!
echo.
echo 🚀 You can now use the downloader:
echo    • Double-click DOWNLOAD.bat for easy use
echo    • Or run: python insta_cli.py username
echo.
echo 💡 Optional: Run build_exe.py to create standalone executable
echo.
pause