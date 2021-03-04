from .log import Log
from .parser import Parser
from .analyzer import Analyzer
import argparse
import json
import os
import sys


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
        with open(user_config) as f:
            file_config = {line.split('=')[0]: line.split('=')[1] for line in f}
    return file_config


def merge_config(file_config, static_config):
    for key in file_config:
        static_config[key] = file_config[key]
    return static_config


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
    with Log(config['LOG_DIR']) as log:
        parser = Parser(log)
        analyzer = Analyzer()
        for u, tr in parser:
            analyzer.get_temp_result(u, tr)

    report = analyzer.get_final_result()

    report_file = get_report_file_path(
        config[REPORT_DIR],
        log.log_date,
    )

    write_report(
        report_template,
        report_file,
        report,
    )


if __name__ == "__main__":
    args = get_cmd_argument(sys.arg[1:])
    config_file = get_file_config(args.config)
    config = merge_config(config_file, config)
    main(**config)
