@echo off
title He Thong Phan Thu - Dang Uy Phuong Tay Nam
color 0C
echo ================================================
echo  HE THONG PHAN THU TU DONG
echo  Dang Uy Phuong Tay Nam
echo ================================================
echo.echo.
echo [0/4] Khoi dong Mock Web (gia lap dhtn.dcs.vn)...
start "Mock Web dhtn.dcs.vn" cmd /k "cd D:\demo_phanthu\mock_web && python mock_server.py"
ping 127.0.0.1 -n 3 > nul
echo OK - Mock web tai: http://localhost:8080

echo.
echo [1/4] Kiem tra Ollama...
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" list
if errorlevel 1 (
    echo LOI: Ollama chua chay! 
    echo Vui long mo Ollama truoc.
    pause
    exit
)
echo OK - Ollama dang chay

echo.
echo [2/4] Khoi dong WhatsApp Server...
start "WhatsApp Server" cmd /k "cd D:\demo_phanthu\whatsapp_server && node server.js"
ping 127.0.0.1 -n 4 > nul

echo.
echo [3/4] Khoi dong Flask App...
start "Flask App" cmd /k "cd D:\demo_phanthu && python app.py"
ping 127.0.0.1 -n 4 > nul

echo.
echo ================================================
echo  DA KHOI DONG XONG!
echo  Mo trinh duyet tai: http://localhost:5000
echo ================================================
echo.
start http://localhost:5000
pause
