import re

class Parser:

    reg_exps = re.compile(
        r'"(?P<request>(?P<method>GET|POST)\s(?P<url>[\w\d\S]+)\s([\w\d\S]+))"'
        r'[\s\S]+'
        r'(?P<request_time>\d.\d{3}$)'
    )

    def __init__(
            self,
            log:Log,
            ):
        self.log = log

    def __iter__(self):
        return self

    def __next__(self):
        try:
            url, request_time = self._parse_line(log.__next__())
            return url, request_time
        except Exception:
            pass

    @staticmethod
    def _parse_line(line,
                    reg_exps=reg_exps,
                    ):
        fields = reg_exps.search(line)
        url = fields.group('url')
        request_time = fields.group('request_time')
        return url, request_time
