from log import Log
from parser import Parser
from analyzer import Analyzer
import argparse
import json
import os
import sys
import logging
from string import Template
import re



config = {
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './reports',
    'LOG_DIR': './log',
}


report_template = './report.html'


def get_cmd_argument(cmd_args):
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        '--config',
        help='Задать другой конфигурационный файл',
    )
    return args_parser.parse_args(cmd_args)

def get_file_config(user_config):
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

def merge_config(file_config, static_config):
    for key in file_config:
        static_config[key] = file_config[key]
    return static_config

def get_config(config):
    args = get_cmd_argument(sys.argv[1:])
    config_file = get_file_config(args.config)
    if config_file is None:
        config_file = {}
    config = merge_config(config_file, config)
    if 'LOG' not in config.keys():
        config['LOG'] = None
    return config


config = get_config(config)
logging.basicConfig(
        filename=config['LOG'],
        filemode='a',
        level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        )


def write_report(template_file, report_file, data):
    with open(template_file, 'r') as file:
        template = Template(file.read())
    with open(report_file, 'wb') as report:
        report.write(template.safe_substitute(table_json=json.dumps(data)).encode(encoding='utf-8'))


def get_report_file_path(report_dir, log_date):
    filename = 'report-{}.html'.format(log_date.strftime('%Y.%m.%d'))
    report_file_path = os.path.join(report_dir, filename)
    return report_file_path



def main(**config):
    logging.info('Поиск последнего лога в директори {}'.format(config['LOG_DIR']))
    with Log(config['LOG_DIR']) as log:
         
        if log.log_path is None:
            sys.exit(0)
        logging.info('Найден лог {}'.format(log.log_path))
        report_file = get_report_file_path(
            config['REPORT_DIR'],
            log.log_date,
        )
        
        if os.path.isfile(report_file):
            logging.info('Отчет для последнего лога существует: {}'.format(report_file))
            sys.exit(0)
        
        logging.info('Создается парсер лога')        
        parser = Parser(log)
        analyzer = Analyzer()
        for u, tr in parser:
            logging.info('Для {} производится предварительный анализ'.format(u))
            analyzer.get_temp_result(u, tr)

    logging.info('Формируется итоговый результат')
    report = analyzer.get_final_result()

    logging.info('Запись отчета в файл: {}'.format(report_file))
    write_report(
            report_template,
            report_file,
            report,
        )
    sys.exit(0)

if __name__ == "__main__":
    logging.debug('Точка входа')
    try:
        main(**config)
    except Exception  as e:
        logging.exception(e)
    except KeyboardInterrupt as e:
        logging.exception(e)

