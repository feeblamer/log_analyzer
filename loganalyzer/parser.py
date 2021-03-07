import re


class Parser:

    reg_exps = re.compile(
        r'"(?P<request>(?P<method>GET|POST)\s(?P<url>[\w\d\S]+)\s([\w\d\S]+))"'
        r'[\s\S]+'
        r'(?P<request_time>\d.\d{3}$)'
    )

    def __init__(
            self,
            log,
            ):
        self.log = log

    def __iter__(self):
        return self

    def __next__(self):
        next_iter = self.log.__next__()
        fields = self._parse_line(next_iter)
        if fields is not None:
            url, request_time = fields
            return url, request_time
        else:
            return '-', '0.0'

    @staticmethod
    def _parse_line(line,
                    reg_exps=reg_exps,
                    ):
        fields = reg_exps.search(line)
        try:
            url = fields.group('url')
            request_time = fields.group('request_time')
            return url, request_time
        except AttributeError as e:
            return None
