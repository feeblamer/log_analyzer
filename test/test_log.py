import unittest
from loganalyzer.log import Log
import os
import gzip
from datetime import date


class TestLogFunctions(unittest.TestCase):

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

        with open('nginx-access-ui.log20201203', 'wb') as log:
            log.write('log3'.encode('utf-8'))

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
        logs = os.listdir(cls.test_dir)
        for log in logs:
            os.remove(os.path.join(cls.test_dir, log))
        os.rmdir(cls.test_dir)

    def test_find_log(self):
        log = Log()
        log.log_date = date(1, 1, 1)
        log._find_log('.')

        self.assertEqual(
            log.log_path,
            './nginx-access-ui.log-20201203.gz',
        )

        self.assertEqual(
            log.log_ext,
            '.gz',
        )

        self.assertEqual(
            log.log_date,
            date(2020, 12, 3),
        )

    def test_open_log_plain(self):
        with Log() as log:
            log.log_path = 'nginx-access-ui.log-20170630'
            log._open_log()
            self.assertEqual(
                log.opened_log.readline(),
                'log1'.encode('utf-8'),
            )

    def test_open_log_gzip(self):
        with Log() as log:
            log.log_path = 'nginx-access-ui.log-20201203.gz'
            log.log_ext = '.gz'
            log._open_log()
            self.assertEqual(
                log.opened_log.readline(),
                'log2'.encode('utf-8'),
            )

    def test_parse_filename_1(self):
        file_1 = 'nginx-access-ui.log-20170630'
        res_1 = Log._parse_filename(file_1)

        self.assertEqual(
            res_1,
            (date(2017, 6, 30), None)
        )

    def test_parse_filename_2(self):
        file_2 = 'nginx-access-ui.log-20201203.gz'
        res_2 = Log._parse_filename(file_2)
        self.assertEqual(
            res_2,
            (date(2020, 12, 3), '.gz')
        )

    def test_parse_filename_3(self):
        file_3 = 'nginx-access-ui.log20201203'
        with self.assertRaises(AttributeError):
            Log._parse_filename(file_3)
