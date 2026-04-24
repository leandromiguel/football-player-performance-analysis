@echo off
echo ============================================
echo   Football Player Performance Dashboard
echo ============================================
echo.
echo Iniciando o dashboard Streamlit...
echo.
cd /d "%~dp0"
streamlit run app.py
pause