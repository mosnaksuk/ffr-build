@echo off
chcp 65001 >nul
echo ===================================================
echo   Final Fantasy Resonance: 1-Click Save Sync & Run
echo ===================================================
echo [1/2] Scanning local game save...
python save_reader.py
echo.
echo [2/2] Opening Optimizer in browser...
start index.html
echo.
echo Done! Enjoy optimizing your builds!
pause
