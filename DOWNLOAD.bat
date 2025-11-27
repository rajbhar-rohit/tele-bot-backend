@echo off
echo Instagram Content Downloader
echo ============================

if "%1"=="" (
    set /p username="Enter username: "
) else (
    set username=%1
)

if "%2"=="" (
    set folder=downloads
) else (
    set folder=%2
)

echo Downloading from @%username% to %folder%
python insta_cli.py %username% -o %folder%
pause