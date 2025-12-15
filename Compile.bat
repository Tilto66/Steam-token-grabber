@echo off
echo Installation PyInstaller...
pip install pyinstaller

cd /d "%~dp0"

echo.
echo Compilation by PyInstaller...
pyinstaller --onefile --noconsole --icon=icone.ico graber.py

echo.
echo Terminé.
pause
