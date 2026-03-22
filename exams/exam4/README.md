# Экзамен: Отладка Python-приложения

## Ситуация
Python-игра находится в `/app/game/`. При запуске возникает ошибка `ModuleNotFoundError: No module named 'config'`.

## Задание
1. Подключитесь по SSH: `ssh student@localhost -p 2222` (пароль: exam2026)
2. Найдите файл `config.py` в `/app/logs/`
3. Скопируйте его в `/app/game/`
4. Запустите игру: `cd /app/game && python3 game.py`

## Подсказки
- Поиск файла: `find /app -name "config.py"`
- Копирование: `cp /app/logs/config.py /app/game/`
- При ошибке прав: используйте `sudo` или `su -`

## Ожидаемый результат
Игра запускается без ошибок импорта и начинает работу.