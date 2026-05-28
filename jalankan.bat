@echo off

echo ============================
echo MENJALANKAN FLASK CHESS AI
echo ============================

start cmd /k "python app.py"

timeout /t 5

echo ============================
echo MENJALANKAN NGROK
echo ============================

start cmd /k "ngrok http 5003"