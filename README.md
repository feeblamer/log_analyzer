# Анализатор логов

## Запуск

В командной строке:

    python log_analyzer.py
 
Находит последний файл по дате в названиии лога. В папке указаной в самом скрипте.

Или возможно указать конфигурационный файл:

    python log_analyzer.py --config <path to file>

## Тесты

Тесты запускаются из пакета **loganalyzer** (там где **__main__.py** и **__init__.py**) командой:

    python -m unittest discover -s '..'

## Проверка

### Успешный запуск

![Успешный запуск](https://i.imgur.com/rExtUdj.png)

### Повторный запуск

![Повторный запуск](https://i.imgur.com/m1HWXD4.png)

### Лог не найден

![Лог не найден](https://i.imgur.com/5T09CSc.png)

### Запуск тестов

![Тесты](https://imgur.com/yhx7omx.png)