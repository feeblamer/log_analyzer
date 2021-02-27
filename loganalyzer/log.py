import re

class Log:
    
    date_pattern = re.compile(
            r'(\d{4})(\d{2})(\d{2})',
            )
    file_name_pattern = re.compile(
            r'^nginx-access-ui.log-(\d{8})(.gz){0,1}',
            )


    def __init__(
            log_dir=None,
            )
        if log_dir is not None:
            self.log_dir = log_dir
            self.log_file = self._find_log(log_dir)

    @property
    def log_name(self):
        pass
    
    @property
    def log_date(self):
        pass

    @property
    def log_extension(self):
        pass

    def __enter__(self):
       self.opend_file = open(self.log_file, 'r') 
       return self.opend_file

    def __exit__(
            self,
            exc_type=None,
            exc_value=None,
            traceback=None,
            ):
        self.opend_file.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.opend_file.__next__()

    def __repr__(self):
        return '<Log object iterator>' 

    def _find_log(self, log_dir):
        pass
