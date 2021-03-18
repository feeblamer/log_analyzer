# Анализатор логов
#
import gzip
from collections import namedtuple
from analyzer import Analyzer
import argparse
import json
import os
import sys
import logging
from string import Template
import re
from datetime import date


config = {
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './reports',
    'LOG_DIR': './log',
    'ERROR_PERC': 50.0,
    # 'LOG': 'loganalyzer.log',
}

filename_pattern = re.compile(
    r'^nginx-access-ui.log-'
    r'(?P<year>\d{4})'
    r'(?P<month>\d{2})'
    r'(?P<day>\d{2})'
    r'(?=(?P<ext>.gz){0,1}$)'
)

line_pattern = re.compile(
    r'"(?P<request>(?P<method>GET|POST)\s(?P<url>[\w\d\S]+)\s([\w\d\S]+))"'
    r'[\s\S]+'
    r'(?P<request_time>\d.\d{3}$)'
)
report_template = './report.html'

Log = namedtuple('Log', ['path', 'date', 'ext'])


# Получение и обработка аргументов командной строки
def get_cmd_argument(cmd_args):
    """Возвращает объект Namespace с аргументами командной строки."""
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        '--config',
        help='Задать другой конфигурационный файл',
    )
    return args_parser.parse_args(cmd_args)


def parse_file_config(user_config):
    """Парсит заданный пользовательем конфигурационный файл."""
    if user_config is not None:
        file_config = {}
        with open(user_config, 'r') as f:
            try:
                for line in f:
                    attrs = line.split('=')
                    if attrs[1].rstrip().isnumeric():
                        file_config[attrs[0]] = int(attrs[1].rstrip())
                    else:
                        file_config[attrs[0]] = attrs[1].rstrip()
            except IndexError:
                file_config = {}
        return file_config


def get_config(config):
    """Возвращает итоговый конфиг.

    Происходит парсинг аргументов команодной строки.
    Cлияние конфигов. В итоговый конфиг включается поле LOG данного скрипта(loganalyzer)"""
    args = get_cmd_argument(sys.argv[1:])
    config_file = parse_file_config(args.config)
    if config_file is None:
        config_file = {}
    config.update(config_file)
    if 'LOG' not in config.keys():
        config['LOG'] = None
    return config


def write_report(
        template_file,
        report_file,
        data,
        report_size,
):
    """Запись REPORT_SIZE строк в файл отчета."""
    with open(template_file, 'r') as file:
        template = Template(file.read())
    with open(report_file, 'wb') as report:
        report.write(template.safe_substitute(table_json=json.dumps(data[:report_size])).encode(encoding='utf-8'))


def get_report_file_path(report_dir, log_date):
    """Формирует имя файла отчета и путь до него по имени анализируемого лога."""
    filename = 'report-{}.html'.format(log_date.strftime('%Y.%m.%d'))
    report_file_path = os.path.join(report_dir, filename)
    return report_file_path


def get_date(match):
    if match is None:
        return None
    return date.fromisoformat('{}-{}-{}'.format(
        match.group('year'),
        match.group('month'),
        match.group('day'),
    )
    )


def get_log(log_dir, regexp=filename_pattern):
    """Поиск файла лога."""
    latest_date = date(1, 1, 1)
    log = Log(None, None, None)
    for path, _, files in os.walk(log_dir, topdown=True):
        for f in files:
            match = regexp.search(f)
            log_date = get_date(match)
            if match and log_date > latest_date:
                latest_date = log_date
                log = Log(
                    os.path.join(path, f),
                    latest_date,
                    match.group('ext'),
                )
                continue
            else:
                continue
    return log


def parse_log(log, regexp=line_pattern):
    if log.ext == '.gz':
        f = gzip.open(log.path, 'rb')
    else:
        f = open(log.path, 'rb')
    for line in f:
        try:
            match = regexp.search(
                line.decode('utf-8')
            )
            yield match.group('url'), match.group('request_time')
        except AttributeError:
            yield '-', '0.0'
    f.close()


def main(config):
    log = get_log(config['LOG_DIR'])
    if log.path is None:
        sys.exit(0)
    report_file = get_report_file_path(
        config['REPORT_DIR'],
        log.date,
    )

    #  Если файл отчета существет, то происходит выход из программы.
    if os.path.isfile(report_file):
        logging.info('Отчет для последнего лога существует: {}'.format(report_file))
        sys.exit(0)
    logging.info('Отчет будет сохранен в файл: {}'.format(report_file))
    parser = parse_log(log)  # generator
    analyzer = Analyzer()
    # Для каждой строки лога парсер отдает url, time_request
    logging.info('Производится предварительный анализ')
    for url, time_request in parser:
        # Формируется предварительный результат для каждого url:
        # {
        # 'url1': {'count':xx, 'time_sum':xx, 'set_times':xxx},
        # }
        try:
            analyzer.get_temp_result(url, time_request)
        except KeyboardInterrupt as e:
            logging.exception(e)
    # Проверка процента ошибок
    if analyzer.errors_perc >= config['ERROR_PERC']:
        logging.error('Превышен порог ошибок')
        sys.exit(0)
    logging.info('Порог ошибок {}%'.format(analyzer.errors_perc))
    logging.info('Формируется итоговый результат')
    report = analyzer.get_final_result()

    logging.info('Запись отчета в файл: {}'.format(report_file))
    write_report(
        report_template,
        report_file,
        report,
        config['REPORT_SIZE'],
    )
    sys.exit(0)


if __name__ == "__main__":

    # Получение итогового конфига
    try:
        config = get_config(config)
    except FileNotFoundError as e:
        logging.exception(e)
    # Конфигурирование логгера.
    # Если лог скрипта не указан, то config['LOG'] = None
    # Лог будет выводится в stdout.
    # При указаном логе происходить запись в файл config['LOG'].
    logging.basicConfig(
        filename=config['LOG'],
        filemode='a',
        level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s %(message)s',
    )
    try:
        main(config)
    except Exception as e:
        logging.exception(e)
