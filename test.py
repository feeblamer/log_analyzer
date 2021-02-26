import unittest
import os
from datetime import date
import logging
import log_analyzer

logging.disabled = True

class TestFindLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log_dir = 'test_log'
        try:
            os.mkdir(cls.log_dir)
        except FileExistsError:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(cls.log_dir)



    def tearDown(self) -> None:
        os.chdir('..')
        for file in os.listdir(self.log_dir):
            os.remove(
                os.path.join(self.log_dir, file)
            )


    def test_find_log_plain(self):
        #создаем файлы с именами
        os.chdir(self.log_dir)
        open('nginx-access-ui.log-20200630', 'w').close()
        open('nginx-access-ui.log-20200628', 'w').close()
        log_data = log_analyzer.find_log('.')
        self.assertEqual(
            log_data.path,
            './nginx-access-ui.log-20200630'
        )

    def test_find_log_gz(self):
        #создаем файлы с именами
        os.chdir(self.log_dir)
        open('nginx-access-ui.log-20200630.gz', 'w').close()
        open('nginx-access-ui.log-20200628.gz', 'w').close()
        log_data = log_analyzer.find_log('.')
        self.assertEqual(
            log_data.path,
            './nginx-access-ui.log-20200630.gz'
        )

    def test_find_log_not_exsist(self):
            #создаем файлы с именами
            os.chdir(self.log_dir)
            open('nginx-access-ui.log20200630.gz', 'w').close()
            open('nginx-access-ui.log20200628.gz', 'w').close()
            log_data = log_analyzer.find_log('.')
            self.assertEqual(
                log_data,
                None
            )

class TestMiscFunc(unittest.TestCase):

    def test_get_report_file_path(self):
        report_dir = './log'
        log_date = date(2019, 7, 22)
        report_file = log_analyzer.get_report_file_path(
            report_dir,
            log_date
        )
        self.assertEqual(
            report_file,
            './log/report-2019.07.22.html'
              )

class TesCommandLineFunc(unittest.TestCase):

    def test_merge_config_1(self):
        static_config = {
        'REPORT_SIZE': 1000,
        'REPORT_DIR': './reports',
        'LOG_DIR': './log',
        }
        file_config = {
        'REPORT_SIZE': 10,
        'REPORT_DIR': './REP1',
        'LOG_DIR': './LOG1',
        }
        merged_config = log_analyzer.merge_config(file_config, static_config)
        self.assertEqual(
            merged_config,
            file_config,
        )

    def test_merge_config_2(self):
        static_config = {
            'REPORT_SIZE': 1000,
            'REPORT_DIR': './reports',
            'LOG_DIR': './log',
        }
        file_config = {
            'REPORT_DIR': './REP2',
            'LOG_DIR': './LOG2',
        }
        merged_config = log_analyzer.merge_config(file_config, static_config)

        self.assertEqual(
            merged_config,
                {
                   'REPORT_SIZE': 1000,
                   'REPORT_DIR': './REP2',
                   'LOG_DIR': './LOG2',
                },
            )


    def test_merge_config_3(self):
        static_config = {
            'REPORT_SIZE': 1000,
            'REPORT_DIR': './reports',
            'LOG_DIR': './log',
        }
        file_config = {
            'LOG_DIR': './LOG3',
        }
        merged_config = log_analyzer.merge_config(file_config, static_config)

        self.assertEqual(
            merged_config,
            {
                'REPORT_SIZE': 1000,
                'REPORT_DIR': './reports',
                'LOG_DIR': './LOG3',
            },
        )

    def test_merge_config_4(self):
        static_config = {
            'REPORT_SIZE': 1000,
            'REPORT_DIR': './reports',
            'LOG_DIR': './log',
        }
        file_config = {}

        merged_config = log_analyzer.merge_config(file_config, static_config)

        self.assertEqual(
            merged_config,
            merged_config,
        )
    )