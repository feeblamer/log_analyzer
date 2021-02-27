#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Анализатор логов.

log_format ui_short
'$remote_addr  $remote_user $http_x_real_ip [$time_local]` "$request" '
'$status $body_bytes_sent "$http_referer" '
'"$http_user_agent" "$http_x_forwarded_for"
"$http_X_REQUEST_ID" "$http_X_RB_USER" '
'$request_time';
"""
import gzip
import logging
import os
import re
from collections import namedtuple
from datetime import date
from decimal import Decimal
from string import Template
import argparse
import json


config = {
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './reports',
    'LOG_DIR': './log',
}

logging.basicConfig(level=logging.INFO)

def find_log(log_dir):
    """Поиск последнего лога.

    Args:
        log_dir: каталог логов.

    Returns:
        return: именованый кортеж содержащий путь лога, дату в имени лога,
        расширение лога.
    """
    #logging.info('Trying to find last log ...\n')
    Log = namedtuple('Log', ['path', 'date', 'ext'])
    log_name_template = re.compile(r'^nginx-access-ui.log-(\d{8})(.gz){0,1}')
    logs = []
    for log_path, _, files in os.walk(log_dir, topdown=True):
        for file in files:
            log = log_name_template.search(file)
            try:
                date_iso_format = re.sub(
                    r'(\d{4})(\d{2})(\d{2})',
                    r'\1-\2-\3',
                    log.groups()[0],
                )
                log_date = date.fromisoformat(date_iso_format)
                logs.append(Log(
                    path=os.path.join(log_path, file),
                    date=log_date,
                    ext=log.groups()[1],
                    ),
                )
            except AttributeError:
                pass
    try:
        log = max(logs, key=lambda log: log[1])
        return log
    except ValueError:
        logging.info('Ни один лог соответсвующего формата не неайден')


def open_log(log_path, ext):
    """Открывает файл лога.
    Args:
        log_path: путь до файла.
        ext: расширение файла
    """
    logging.info('Open log {}'.format(log_path))
    with gzip.open(log_path, 'rb') if ext == '.gz' else open(log_path, 'rb') as log:
        while True:
            line = log.readline()
            if not line:
                break
            yield line.decode('utf-8', 'replace')


def parse(log):
    """Парсер лога.

    Генератор который парсит лог построчно.
    Args:
        log: именнованный кортеж содержащий путь лога, дату в имени лога,
        расширение лога.
    Returns:
        return: возвращает отчет в виде отсортированного списка словарей
    """

    for line in log:
        url_pattern = re.compile(r'(\"(GET|POST)\s)(?P<url>\S+)(\sHTTP/1.[10])')
        request_time_pattern = re.compile(r'\d+\.\d+$')
        try:
            url = url_pattern.search(line).group('url')
            request_time = request_time_pattern.search(line).group()
            yield url, request_time
        except AttributeError:
            pass

def count_time_median(time_sum:list):
    time_sum.sort(reverse=True)
    if len(time_sum) == 1:
        return time_sum[0]
    elif len(time_sum) == 2:
        return Decimal((time_sum[0] + time_sum[0]) / 2 )
    elif len(time_sum) >= 3 and len(time_sum) % 2 == 0:
        median = Decimal((time_sum[len(time_sum)//2] + time_sum[(len(time_sum)//2) + 1])/2)
        return median
    elif len(time_sum) >= 3 and len(time_sum) % 2 == 1:
        return time_sum[(len(time_sum)//2) + 1]


def count_metrics(metrics):
    d = {}
    logging.info('Calculate metrics')
    num_requests = 0
    sum_time_requests = Decimal(0.000)
    for url, time_request in metrics:
        num_requests += 1
        sum_time_requests += Decimal(time_request)
        if url in d.keys():
            d[url]['count'] += 1
            d[url]['time_requests'].append(Decimal(time_request))
        else:
            d[url] = {'count':1}
            d[url]['time_requests'] = [Decimal(time_request)]

    res = []
    for url in d:
        report_data = dict()
        time_sum = sum(d[url]['time_requests'])
        report_data['count'] = d[url]['count']
        report_data['url'] = url
        report_data['count_perc'] = str(Decimal((d[url]['count'] / num_requests) * 100)\
            .quantize(Decimal('.001'),
                     rounding='ROUND_HALF_UP'))
        report_data['time_perc'] = str(Decimal((time_sum / sum_time_requests ) * 100)\
            .quantize(Decimal('.001'), rounding='ROUND_HALF_UP'))
        report_data['time_averege'] = str(Decimal(time_sum / d[url]['count']))

        report_data['time_med'] = str(count_time_median(d[url]['time_requests']))
        report_data['time_max'] = str(max(d[url]['time_requests']))
        report_data['time_sum'] = str(time_sum)
        res.append(report_data)

    return sorted(res, reverse=True, key=lambda t: t['time_sum'])


def write_report(template_file, report_file, data):

    with open(template_file, 'r') as file:
        template = Template(file.read())
    with open(report_file, 'wb') as report:

        report.write(template.safe_substitute(table_json=json.dumps(data)).encode(encoding='utf-8'))

def get_report_file_path(report_dir, log_date):
    filename = 'report-{}.html'.format(log_date.strftime('%Y.%m.%d'))
    report_file_path= os.path.join(report_dir, filename)
    return report_file_path


def merge_config(file_config, static_config):
    for key in file_config:
        static_config[key] = file_config[key]
    return static_config


def main(**kwargs):

    log_data = find_log(kwargs['LOG_DIR'])
    try:
        report_file = get_report_file_path(
            kwargs['REPORT_DIR'],
            log_data.date,
        )
    except AttributeError:
        exit(0)

    template_file = './report.html'
    if not(os.path.exists(report_file)):
        log = open_log(log_data.path, log_data.ext)
        metrics = parse(log)
        result = count_metrics(
            metrics,
        )
        logging.info('Get result {}'.format(result[0]))

        try:
            write_report(template_file, report_file, result[:kwargs['REPORT_SIZE']])
        except IndexError:
            write_report(template_file, report_file, result)
    else:
        logging.info('Отчет по данному логу {} уже существет'.format(log_data.path))
    exit(0)

def get_cmd_argument(cmd_args):
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', help='Задать другой конфигурационный файл')
    return args_parser.parse_args(cmd_args)


def get_file_config(user_config):

    if user_config is not None:
        with open(user_config) as f:
            file_config  = {line.split('=')[0]:line.split('=')[1] for line in f}
    return  file_config

if __name__ == '__main__':

    args = get_cmd_argument(sys.arg[1:])
    config_file = get_file_config(args.config)
    config = merge_config(config_file, config)
    main(**config)