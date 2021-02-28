from log import Log
from parser import Parser


config = {
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './reports',
    'LOG_DIR': '/home/avm/log',
}


def main(**config):
 
    with Log(config['LOG_DIR']) as log:
        print(type(log))
        parser = Parser(log)
        try:
            for u, tr in parser:
                print(u)
        except TypeError as e:
            print(log.opened_log)
            print('OPa', next(parser))


if __name__ == "__main__":
    main(**config)
