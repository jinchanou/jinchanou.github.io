@echo off

echo Starting backend server...
start "Backend Server" /min python main.py

timeout /t 5 /nobreak >nul

echo Starting frontend server...
start "Frontend Server" /min python -m http.server 8001 --bind 0.0.0.0

echo.
echo Services started:
echo Backend: http://localhost:8002
echo Frontend: http://localhost:8001
echo.
echo Please open http://localhost:8001 in your browser
echo API docs: http://localhost:8002/docs

echo.
echo To access from other devices, use the IP address of this computer and port 8001
echo For example: http://192.168.1.100:8001 (replace with actual IP)

echo.
pause