import unittest
from loganalyzer import main


class TestCmdParsing(unittest.TestCase):

    def test_get_cmd_argument(self):
        cmd_argument_1 = ['--config', '.']
        cmd_argument_2 = ['--config', './config']
        cmd_argument_3 = ['--config', '.config/loganalyzer/conf']
        self.assertEqual(
            main.get_cmd_argument(cmd_argument_1).config,
            '.',
        )
        self.assertEqual(
            main.get_cmd_argument(cmd_argument_2).config,
            './config',
        )
        self.assertEqual(
            main.get_cmd_argument(cmd_argument_3).config,
            '.config/loganalyzer/conf',
        )

    def test_get_file_config(self):
        pass

    def test_merge_config(self):
        pass


class TestReportPreparing(unittest.TestCase):

    def test_get_report_file_path(self):
        pass

    def test_write_report(self):
        pass
