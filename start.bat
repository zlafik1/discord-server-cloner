@echo off
chcp 65001 >nul
title Discord Server Cloner V3 - Blue Edition
color 0B

echo ═════════════════════════════════════════════════════════════
echo                     Discord Server Cloner V3
echo                     Blue Edition by zlafik
echo ═════════════════════════════════════════════════════════════
echo.

if exist "venv\Scripts\python.exe" (
    echo [*] Запуск программы...
    echo.
    call venv\Scripts\python.exe channel_copier.py
    pause
    exit
)

echo [*] Виртуальное окружение не найдено!
echo [*] Запустите install.bat для установки зависимостей
pause