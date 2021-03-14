import unittest
from loganalyzer.analyzer import Analyzer


class TestAnalyzeFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.urls = [
            '/api/page1/index.html',
            '/api/page2/index.html',
            '/api/blogs/post1',
        ]
        cls.analyzer = Analyzer()
        cls.analyzer._count_requests = 5462
        cls.analyzer._time_requests = 10.678
        cls.analyzer._temp_result = {
            cls.urls[0]: {
                'count': 234,
                'time_sum': 2.845,
                'set_times_url': {0.4, 2.4, 0.1, 0.23, 0.34},
            },
            cls.urls[1]: {
                'count': 934,
                'time_sum': 3.8,
                'set_times_url': {0.6, 0.4, 0.15, 0.3, 1.4},
            },
            cls.urls[2]: {
                'count': 15,
                'time_sum': 0.9,
                'set_times_url': {0.3, 0.1, 0.1, 0.09, 0.07},
            },
        }

    def test_count_perc(self):
        perc1 = self.analyzer.count_perc(self.urls[0])
        perc2 = self.analyzer.count_perc(self.urls[1])
        perc3 = self.analyzer.count_perc(self.urls[2])
        self.assertEqual(
            perc1,
            round(
                self.analyzer._temp_result[self.urls[0]]['count'] * 100 / self.analyzer._count_requests,
                3,
            ),
        )
        self.assertEqual(
            perc2,
            round(
                self.analyzer._temp_result[self.urls[1]]['count'] * 100 / self.analyzer._count_requests,
                3,
            ),
        )
        self.assertEqual(
            perc3,
            round(
                self.analyzer._temp_result[self.urls[2]]['count'] * 100 / self.analyzer._count_requests,
                3,
            ),
        )

    def test_time_perc(self):
        perc1 = self.analyzer.time_perc(self.urls[0])
        perc2 = self.analyzer.time_perc(self.urls[1])
        perc3 = self.analyzer.time_perc(self.urls[2])
        self.assertEqual(
            perc1,
            round(
                self.analyzer._temp_result[self.urls[0]]['time_sum'] * 100 / self.analyzer._time_requests,
                3,
            ),
        )
        self.assertEqual(
            perc2,
            round(
                self.analyzer._temp_result[self.urls[1]]['time_sum'] * 100 / self.analyzer._time_requests,
                3,
            ),
        )
        self.assertEqual(
            perc3,
            round(
                self.analyzer._temp_result[self.urls[2]]['time_sum'] * 100 / self.analyzer._time_requests,
                3,
            ),
        )

    def test_time_avg(self):
        avg1 = self.analyzer.time_avg(self.urls[0])
        avg2 = self.analyzer.time_avg(self.urls[1])
        avg3 = self.analyzer.time_avg(self.urls[2])
        self.assertEqual(
            avg1,
            round(
                self.analyzer._temp_result[self.urls[0]]['time_sum'] / self.analyzer._temp_result[self.urls[0]][
                    'count'],
                3,
            ),
        )
        self.assertEqual(
            avg2,
            round(
                self.analyzer._temp_result[self.urls[1]]['time_sum'] / self.analyzer._temp_result[self.urls[1]][
                    'count'],
                3,
            ),
        )
        self.assertEqual(
            avg3,
            round(
                self.analyzer._temp_result[self.urls[2]]['time_sum'] / self.analyzer._temp_result[self.urls[2]][
                    'count'],
                3,
            ),
        )

    def test_time_med(self):
        med1 = self.analyzer.time_med(self.urls[0])
        med2 = self.analyzer.time_med(self.urls[1])
        med3 = self.analyzer.time_med(self.urls[2])
        self.assertEqual(
            med1,
            0.34,
        )
        self.assertEqual(
            med2,
            0.4,
        )
        self.assertEqual(
            med3,
            0.095,
        )

    def test_count_error_perc(self):
        self.analyzer._errors = 337
        perc1 = self.analyzer._count_errors_perc()
        self.assertEqual(perc1, 6.17)
        self.analyzer._errors = 3786
        perc2 = self.analyzer._count_errors_perc()
        self.assertEqual(perc2, 69.32)


class TestTempResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analyzer = Analyzer()
        cls.parsed_lines = [
            ('/url/one.html', '0.7'),
            ('/url/one.html', '0.3'),
            ('/blog/index.html', '0.2'),
            ('/news/ghj7gKjy887', '0.345'),
        ]

    def test_get_temp_result(self):
        for line in self.parsed_lines:
            self.analyzer.get_temp_result(line[0], line[1])
        self.assertEqual(
            self.analyzer._temp_result,
            {
                '/url/one.html': {'count': 2, 'time_sum': 1.0, 'set_times_url': {0.7, 0.3}},
                '/blog/index.html': {'count': 1, 'time_sum': 0.2, 'set_times_url': {0.2}},
                '/news/ghj7gKjy887': {'count': 1, 'time_sum': 0.345, 'set_times_url': {0.345}},
            }
        )


class TestFinalResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.analyzer = Analyzer()
        cls.analyzer._count_requests = 4
        cls.analyzer._time_requests = 1.545
        cls.analyzer._temp_result = {
            '/url/one.html': {'count': 2, 'time_sum': 1.0, 'set_times_url': {0.7, 0.3}},
            '/blog/index.html': {'count': 1, 'time_sum': 0.2, 'set_times_url': {0.2}},
            '/news/ghj7gKjy887': {'count': 1, 'time_sum': 0.345, 'set_times_url': {0.345}},
            }

    def test_get_final_result(self):
        result = self.analyzer.get_final_result()
        self.assertEqual(
                {
                    'url': '/url/one.html',
                    'count': 2,
                    'count_perc': 50.0,
                    'time_sum': 1.0,
                    'time_perc': 64.725,
                    'time_avg': 0.5,
                    'time_max': 0.7,
                    'time_med': 0.5,
                } in result, True
        )

        self.assertEqual(
                 {
                     'url': '/blog/index.html',
                     'count': 1,
                     'count_perc': 25.0,
                     'time_sum': 0.2,
                     'time_perc': 12.945,
                     'time_avg': 0.2,
                     'time_max': 0.2,
                     'time_med': 0.2,
                 } in result, True
                 )
        self.assertEqual(
                 {
                     'url': '/news/ghj7gKjy887',
                     'count': 1,
                     'count_perc': 25.0,
                     'time_sum': 0.345,
                     'time_perc': 22.330,
                     'time_avg': 0.345,
                     'time_max': 0.345,
                     'time_med': 0.345,
                 } in result, True
                )
