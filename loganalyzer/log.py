import gzip
import os
import re
from datetime import date
import logging 


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Log:
    log_date_pattern = re.compile(
        r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})',
    )
    log_name_pattern = re.compile(
        r'^nginx-access-ui.log-(?P<date>\d{8})(?P<ext>.gz){0,1}',
    )

    def __init__(
            self,
            log_dir=None,
    ):
        logger.debug('Инициализация объекта и его атрибутов')
        if log_dir is not None:
            self.log_dir = log_dir
            self.log_path = None
            self.log_ext = None
            self.log_date = date(1, 1, 1)
            self._find_log(log_dir)

    def _open_log(self):
        opened_log = gzip.open(self.log_path, 'rb') if self.log_ext == '.gz' else open(self.log_path, 'rb')
        return opened_log

    def __enter__(self):
        if self.log_path is not None:
            self.opened_log = self._open_log()
        else:
            self.opened_log = None
            logger.info('Файл логов не найден')
        return self

    def __exit__(
            self,
            exc_type=None,
            exc_value=None,
            traceback=None,
    ):
        if self.opened_log is not None:
            self.opened_log.close()

    def __iter__(self):
        return self

    def __next__(self):
        
        if self.opened_log is not None:
            line = self.opened_log.__next__()
            return line.decode('utf-8', 'replace')
        else:
            raise StopIteration

    def __repr__(self):
        return '<Log object iterator>'

    @staticmethod
    def _parse_filename(
            file,
            log_name_pattern=log_name_pattern,
            log_date_pattern=log_date_pattern,
    ):

        logger.debug('Получили файл {}'.format(file))
        name_log = log_name_pattern.search(file)
        log_date = log_date_pattern.search(
            name_log.group('date')
        )
        dict_date = log_date.groupdict()
        log_date = date(
            int(dict_date['year']),
            int(dict_date['month']),
            int(dict_date['day']),
        )
        log_extension = name_log.group('ext')
        return log_date, log_extension

    def _find_log(self, log_dir):
        logger.debug('Поиск лога в директории {}'.format(log_dir))
        for path, _, files in os.walk(log_dir, topdown=True):
            logger.debug('В дерикории на ходятся файлы {}'.format(files))
            for f in files:
                try:
                    log_date, extension = self._parse_filename(f)
                except AttributeError:
                    continue
                if self.log_date < log_date:
                    self.log_date = log_date
                    self.log_path = os.path.join(path, f)
                    self.log_ext = extension
