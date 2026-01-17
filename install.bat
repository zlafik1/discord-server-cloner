@echo off
chcp 65001 >nul
title Discord Server Cloner V3 - Установка
color 0B

echo ═════════════════════════════════════════════════════════════
echo                  Установка Discord Server Cloner
echo                     Blue Edition by zlafik
echo ═════════════════════════════════════════════════════════════
echo.

echo [*] Проверка наличия Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [-] Python не найден!
    echo [*] Скачайте и установите Python с официального сайта:
    echo [*] https://python.org/downloads/
    echo [*] Не забудьте поставить галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo [+] Python найден
python --version

echo.
echo [*] Создание виртуального окружения...
python -m venv venv
if errorlevel 1 (
    echo [-] Ошибка создания виртуального окружения
    echo [*] Установите модуль venv: python -m pip install virtualenv
    pause
    exit /b 1
)

echo [+] Виртуальное окружение создано

echo.
echo [*] Установка зависимостей...
call venv\Scripts\pip.exe install --upgrade pip
call venv\Scripts\pip.exe install colorama requests aiohttp

if errorlevel 1 (
    echo [-] Ошибка установки зависимостей
    pause
    exit /b 1
)

echo [+] Зависимости установлены

echo.
echo [*] Проверка установки...
call venv\Scripts\python.exe -c "import colorama, requests, aiohttp; print('[*] Все модули успешно импортированы')"

echo.
echo ═════════════════════════════════════════════════════════════
echo                    УСТАНОВКА ЗАВЕРШЕНА
echo ═════════════════════════════════════════════════════════════
echo.
echo [*] Для запуска программы используйте start.bat
echo [*] Или запустите вручную: venv\Scripts\python.exe channel_copier.py
echo.
echo [*] Создайте файл token.txt в папке с программой
echo [*] Добавьте в него ваш Discord токен (одной строкой)
echo.
echo [*] Поддержка: Telegram @qtiq0 | Discord zlafik
echo.
pause