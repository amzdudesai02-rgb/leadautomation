@echo off
echo ========================================
echo Starting Frontend Server...
echo ========================================
cd frontend
echo.
echo Installing dependencies...
call npm install
echo.
echo Starting Vite development server...
echo Frontend will run on http://localhost:3000
echo.
call npm run dev
pause

