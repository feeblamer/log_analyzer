import unittest
from loganalyzer.log import Log
import os
from datetime import date


class TestLogFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_dir_2'
        os.mkdir(cls.test_dir)
        os.chdir(cls.test_dir)
        with open('nginx-access-ui.log-20170630', 'w') as log:
            log.write('log1')

        with open('nginx-access-ui.log-20201203.gz', 'w') as log:
            log.write('log2')

        with open('nginx-access-ui.log20201203', 'w') as log:
            log.write('log3')

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')
        logs = os.listdir(cls.test_dir)
        for log in logs:
            os.remove(os.path.join(cls.test_dir, log))
        os.rmdir(cls.test_dir)

    def test_find_log(self):
        pass

    def test_open_log(self):
        pass

    def test_parse_filename(self):
        file_1 = 'nginx-access-ui.log-20170630'
        file_2 = 'nginx-access-ui.log-20201203.gz'
        file_3 = 'nginx-access-ui.log20201203'
        res_1 = Log._parse_filename(file_1)
        res_2 = Log._parse_filename(file_2)

        self.assertEqual(
            res_1,
            (date(2017, 6, 30), None)
        )
        self.assertEqual(
            res_2,
            (date(2020, 12, 3), '.gz')
        )

        with self.assertRaises(AttributeError):
            Log._parse_filename(file_3)
