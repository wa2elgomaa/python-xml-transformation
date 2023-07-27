from datetime import  datetime, time
from traceback import format_exception
from utils import create_folder


class Logger:
    def __init__(self):
        self.logs_folder = 'xmlscript-logs'
        self.logs_file_prefix = 'logs-'

    def get_traceback(ex, ex_traceback=None):
        if ex is None:
            return 'Undefined Error'
        if ex_traceback is None:
            ex_traceback = ex.__traceback__
        return format_exception(ex.__class__, ex, ex_traceback)

    def log_message(self, message, e=None):
        log_msg = f'{datetime.now()} : ---LOG--- {message}'
        print(log_msg)

        # create logs folder if not exists
        create_folder(self.logs_folder)
        # log the error in a separate file
        with open(f'{self.logs_folder}/{self.logs_file_prefix}{time().strftime("%Y-%m-%d")}.txt', 'a+',
                  encoding='utf-8') as f:
            # Move read cursor to the start of file.
            f.seek(0)
            # If file is not empty then append '\n'
            txt = f.read(100)
            if len(txt) > 0:
                f.write('\n')
            f.write(log_msg)
            if e:
                f.write('\n')
                f.write(f'Error : {self.get_traceback(e)}')
            f.close()
