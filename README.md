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

## Запуск скрипта

### Успешный запуск


![Успешный запуск с указанием конфига](https://3.downloader.disk.yandex.ru/preview/7c1632bbcd86b49e6a05f2cdcc559989f37f39a3e66b25d5992bd8b155d8ffed/inf/92riRzPgdg9epfzTopCEvELxT92dp3cl2oKKBrr7I53QSnAC0_ba9n23s9nzQtXM42vEIDYGVTvqaY8YDxFUGQ%3D%3D?uid=160758080&filename=UserConfigSuccessfulRun.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=160758080&tknv=v2&size=1905x907)


### Повторный запуск.

Если файл отчета существует в директории **reports**, происходит выход из программы.


![Повторный запуск](https://1.downloader.disk.yandex.ru/preview/5cfc17744a8660dda6bbfcf52fd58c15ab3230aef81dd3ad889e0335adcdd47b/inf/f9YfhxEBNrHzTk_-lHVjb9ygt4RTgb4zyd36VryRBHaytKq_OKuFRtdk6TjljOnxbPzK7FhcnJ7TB8ZFOzTyHw%3D%3D?uid=160758080&filename=SecondTimeForExcsistingFile.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=160758080&tknv=v2&size=1905x907)
### Лог не найден 


![Не найден лог](https://1.downloader.disk.yandex.ru/preview/8068844526e927f74fb9cbc799a0e53244c5c2a319ef6987429a05a3a2a66022/inf/c2J7sabsZdWgUUCQctA6TPVAwvfKo240eZ1vb2m-7NNrEaof5ghTCNHjGVX9g51RKdDe21cCA9YIkS6MNR5FMw%3D%3D?uid=160758080&filename=Log_Not_Found.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=160758080&tknv=v2&size=1905x907)

### Отчет.

Количество строк из **config['REPORT_SIZE']**. Отсортировано по **time_sum** каждого **url**.


![Отчет](https://2.downloader.disk.yandex.ru/preview/5d787784e4b099795230110a61258664aa1b859c9423822829c66fb7fca90b6e/inf/FLIzTufpHww8U4frGpXNQtygt4RTgb4zyd36VryRBHY-kGjAC1A1LItVqYGnN7v3KC8yu5jG-_3-NV2VesP3_Q%3D%3D?uid=160758080&filename=report.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=160758080&tknv=v2&size=1905x907)

