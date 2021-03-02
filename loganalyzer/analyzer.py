class Analyzer:
    def __init__(self):
        self.result = []
        self._temp_result = {}
        self._count_requests = 0
        self._time_requests = 0.0

    def get_temp_result(self, url, request_time):
        self._count_requests += 1
        self._time_requests += request_time
        if url in temp_result.keys():
            self.temp_result[url]['count'] += 1
            self.temp_result[url]['time_sum'] += request_time
            self.temp_result[url]['set_times_url'].add(request_time)
        else:
            self.temp_result[url] = {
                'count': 1,
                'time_sum': request_time,
                'set_times_url': set(request_time),
            }

    def count_perc(self, url):
        count = self._temp_result[url]['count']
        result = count * 100 / self._count_requests
        return result

    def time_perc(self, url):
        time_sum = self.temp_result[url]['time_sum']
        result = time_sum * 100 / self._time_requests
        return result

    def time_avg(self, url):
        count = self._temp_result[url]['count']
        time_sum = self._temp_result[url]['time_sum']
        return time_sum / count

    def time_med(self, url):
        list_times = list(self._temp_result[url]['set_times_url'])
        list_times.sort(reverse=True)
        index = list_times // len(list_times)

        if len(list_times) % 2:
            return list_times[index]
        return sum(list_times[index-1:index+1]) / 2

    def get_final_result(self):
        for url in self._temp_result:
            self.result.append(
                {
                    'url': url,
                    'count': self._temp_result[url]['count'],
                    'count_perc': self.count_perc(url),
                    'time_sum': self._temp_result[url]['time_sum'],
                    'time_perc': self.time_perc(url),
                    'time_avg': self.time_avg(url),
                    'time_max': max(self._temp_result[url]['set_times_url']),
                    'time_med': self.time_med(url),
                }
            )
        return self.result
