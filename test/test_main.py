import unittest
import os
from datetime import date
import gzip
from loganalyzer.__main__ import get_cmd_argument
from loganalyzer.__main__ import parse_file_config
from loganalyzer.__main__ import get_report_file_path
from loganalyzer.__main__ import get_log
from loganalyzer.__main__ import Log
from loganalyzer.__main__ import parse_log


class TestCmdParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_dir_1'
        os.mkdir(cls.test_dir)
        os.chdir(cls.test_dir)
        cls.configs = {
            'config_1': """LOG_DIR=./log/log
REPORT_SIZE=100""",
            'config_2': "LOG_DIR=log",
            'config_3': " ",
            'config_4': """REPORT_SIZE=200
REPORT_DIR=./report
LOG_DIR=log""",
        }
        for k in cls.configs:
            with open(k, 'w') as config:
                config.write(cls.configs[k])

    @classmethod
    def tearDownClass(cls):
        for k in cls.configs:
            os.remove(k)
        os.chdir('..')
        os.rmdir(cls.test_dir)

    def test_get_cmd_argument(self):
        cmd_argument_1 = ['--config', '.']
        cmd_argument_2 = ['--config', './config']
        cmd_argument_3 = ['--config', '.config/loganalyzer/conf']
        self.assertEqual(
            get_cmd_argument(cmd_argument_1).config,
            '.',
        )
        self.assertEqual(
            get_cmd_argument(cmd_argument_2).config,
            './config',
        )
        self.assertEqual(
            get_cmd_argument(cmd_argument_3).config,
            '.config/loganalyzer/conf',
        )

    def test_get_file_config_1(self):
        config = parse_file_config('config_1')
        self.assertEqual(
            config,
            {
                'LOG_DIR': './log/log',
                'REPORT_SIZE': 100,
            },
        )

    def test_get_file_config_2(self):
        config = parse_file_config('config_2')
        self.assertEqual(
            config,
            {'LOG_DIR': 'log'},
        )

    def test_get_file_config_3(self):
        config = parse_file_config('config_3')
        self.assertEqual(
            config,
            {},
        )

    def test_get_file_config_4(self):
        config = parse_file_config('config_4')
        self.assertEqual(
            config,
            {
                'REPORT_SIZE': 200,
                'REPORT_DIR': './report',
                'LOG_DIR': 'log',
            },
        )


class TestReport(unittest.TestCase):

    def setUp(self):
        self.report_dir = './test_report'

    def test_get_report_file_path(self):
        log_date = date(2021, 12, 22)
        report_file = get_report_file_path(
            self.report_dir,
            log_date,
        )
        self.assertEqual(
            report_file,
            os.path.join(
                self.report_dir,
                'report-{}.html'.format(log_date.strftime('%Y.%m.%d')),
            ),
        )


class TestGetLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_dir_2'
        os.mkdir(cls.test_dir)
        os.chdir(cls.test_dir)
        with open('nginx-access-ui.log-20170630', 'wb') as log:
            log.write('log1'.encode('utf-8'))

        with gzip.open('nginx-access-ui.log-20201203.gz', 'wb') as log:
            log.write('log2'.encode('utf-8'))

        with open('nginx-access-ui.log-20201204.bz2', 'wb') as log:
            log.write('not log'.encode('utf-8'))
        os.chdir('..')

    @classmethod
    def tearDownClass(cls):
        logs = os.listdir(cls.test_dir)
        for log in logs:
            os.remove(os.path.join(cls.test_dir, log))
        os.rmdir(cls.test_dir)

    def test_get_log(self):
        log = get_log(self.test_dir)
        self.assertEqual(
            log,
            Log(
                os.path.join(self.test_dir, 'nginx-access-ui.log-20201203.gz'),
                date(2020, 12, 3),
                '.gz',
            )
        )


class TestParseLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_dir_2'
        os.mkdir(cls.test_dir)
        os.chdir(cls.test_dir)
        cls.log_1 = Log('log_1', date(2021, 3, 18), None)
        cls.log_2 = Log('log_2', date(2021, 4, 14), '.gz')
        with open(cls.log_1.path, 'wb') as log_1:
            line = '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/1717161 HTTP/1.1" 200 2116 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752771" "712e90144abee9" 0.138\n'
            log_1.writelines([line.encode('utf-8')])

        with gzip.open(cls.log_2.path, 'wb') as log_2:
            line ='1.166.85.48 -  - [29/Jun/2017:03:50:22 +0300] "GET /export/appinstall_raw/2017-06-30/ HTTP/1.0" 404 162 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)" "-" "-" "-" 0.001\n'
            log_2.writelines([line.encode('utf-8')])

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
        logs = os.listdir(cls.test_dir)
        for log in logs:
            os.remove(os.path.join(cls.test_dir, log))
        os.rmdir(cls.test_dir)

    def test_parse_log_1(self):
        parser1 = parse_log(self.log_1)
        for url, request_time in parser1:
            self.assertEqual(
                url,
                '/api/v2/banner/1717161',
            )
            self.assertEqual(
                request_time,
                '0.138'
            )

    def test_parse_log_2(self):
        parser2 = parse_log(self.log_2)
        for url, request_time in parser2:
            self.assertEqual(
                url,
                '/export/appinstall_raw/2017-06-30/',
            )
            self.assertEqual(
                request_time,
                '0.001',
            )
