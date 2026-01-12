@echo off
echo ========================================
echo Starting Backend Server...
echo ========================================
cd backend
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Backend will run on http://localhost:5000
echo.
python run.py
pause

