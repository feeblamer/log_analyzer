import unittest
from loganalyzer.parser import Parser


class TestParser(unittest.TestCase):

    def test_parse_line_1(self):
        line = '1.168.65.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/internal/banner/24294027/info HTTP/1.1" ' \
               '200 407 "-" "-" "-" "1498697422-2539198130-4709-9928846" "89f7f1be37d" 0.146'
        result = Parser._parse_line(line)
        self.assertEqual(
            result,
            ('/api/v2/internal/banner/24294027/info', '0.146'),
        )

    def test_parse_line_2(self):
        line = '1.194.135.240 -  - [29/Jun/2017:03:50:23 +0300] "GET ' \
               '/api/v2/group/7786683/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28 ' \
               'HTTP/1.1" 200 22 "-" "python-requests/2.13.0" "-" "1498697423-3979856266-4708-9752782" ' \
               '"8a7741a54297568b" 0.061'
        result = Parser._parse_line(line)
        self.assertEqual(
            result,
            ('/api/v2/group/7786683/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28', '0.061'),
        )
