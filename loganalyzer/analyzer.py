def round_decorate(func):
    def rounder(*args):
        result = func(*args)
        return round(result, 3)

    return rounder


class Analyzer:
    def __init__(self):
        self.result = []
        self._temp_result = {}
        self._count_requests = 0
        self._time_requests = 0.0
        self._errors = 0
        self.errors_perc = 0.0

    def _count_errors_perc(self):
        perc = self._errors * 100 / self._count_requests
        return round(perc, 2)

    def get_temp_result(self, url, request_time):
        self._count_requests += 1
        self._time_requests += float(request_time)
        if url == '-' and request_time == '0.0':
            self._errors += 1
            self.errors_perc = self._count_errors_perc()
        if url in self._temp_result.keys():
            self._temp_result[url]['count'] += 1
            self._temp_result[url]['time_sum'] += float(request_time)
            self._temp_result[url]['set_times_url'].add(float(request_time))
        else:
            self._temp_result[url] = {
                'count': 1,
                'time_sum': float(request_time),
                'set_times_url': {float(request_time)},
            }

    @round_decorate
    def count_perc(self, url):
        count = self._temp_result[url]['count']
        percents = count * 100 / self._count_requests
        return percents

    @round_decorate
    def time_perc(self, url):
        time_sum = self._temp_result[url]['time_sum']
        percents = time_sum * 100 / self._time_requests
        return percents

    @round_decorate
    def time_avg(self, url):
        count = self._temp_result[url]['count']
        time_sum = self._temp_result[url]['time_sum']
        return time_sum / count

    @round_decorate
    def time_med(self, url):
        list_times = list(self._temp_result[url]['set_times_url'])
        list_times.sort()
        index = len(list_times) // 2

        if len(list_times) % 2 != 0:
            return list_times[index]
        return sum(list_times[index - 1:index + 1]) / 2

    def get_final_result(self):
        for url in self._temp_result:
            self.result.append(
                {
                    'url': url,
                    'count': self._temp_result[url]['count'],
                    'count_perc': self.count_perc(url),
                    'time_sum': round(self._temp_result[url]['time_sum'], 3),
                    'time_perc': self.time_perc(url),
                    'time_avg': self.time_avg(url),
                    'time_max': max(self._temp_result[url]['set_times_url']),
                    'time_med': self.time_med(url),
                }
            )
        self.result = sorted(
            self.result,
            reverse=True,
            key=lambda d: d['time_sum'],
        )
        return self.result
