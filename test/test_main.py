import unittest
import os
from loganalyzer.__main__ import get_cmd_argument
from loganalyzer.__main__ import merge_config
from loganalyzer.__main__ import get_file_config
from loganalyzer.__main__ import get_report_file_path
from datetime import date


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
        config = get_file_config('config_1')
        self.assertEqual(
            config,
            {
                'LOG_DIR': './log/log',
                'REPORT_SIZE': 100,
            },
        )

    def test_get_file_config_2(self):
        config = get_file_config('config_2')
        self.assertEqual(
            config,
            {'LOG_DIR': 'log'},
        )

    def test_get_file_config_3(self):
        config = get_file_config('config_3')
        self.assertEqual(
            config,
            {},
        )

    def test_get_file_config_4(self):
        config = get_file_config('config_4')
        self.assertEqual(
            config,
            {
                'REPORT_SIZE': 200,
                'REPORT_DIR': './report',
                'LOG_DIR': 'log',
            },
        )

    def test_merge_config_1(self):
        config = {
            'REPORT_SIZE': 1000,
            'REPORT_DIR': './reports',
            'LOG_DIR': './log',
        }
        file_config = get_file_config('config_1')
        merged_conf = merge_config(file_config, config)
        self.assertEqual(
            merged_conf,
            {
                'REPORT_SIZE': 100,
                'REPORT_DIR': './reports',
                'LOG_DIR': './log/log',
            },
        )

    def test_merge_config_3(self):
        config = {
            'REPORT_SIZE': 1000,
            'REPORT_DIR': './reports',
            'LOG_DIR': './log',
        }
        file_config = get_file_config('config_3')
        merged_conf = merge_config(file_config, config)
        self.assertEqual(
            merged_conf,
            {
                'REPORT_SIZE': 1000,
                'REPORT_DIR': './reports',
                'LOG_DIR': './log',
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

