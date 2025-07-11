import os
import time
import logging
import configparser as cfp

def getDate():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

class LogHandler:
    logger = None
    log_filename = None

    @classmethod
    def set_logfile(cls, filename:str):
        # 移除舊有 handler
        if cls.logger:
            for handler in cls.logger.handlers[:]:
                cls.logger.removeHandler(handler)
                handler.close()
        else:
            cls.logger = logging.getLogger(__name__)
            cls.logger.setLevel(logging.INFO)
        
        # 設定新的 handler
        log_path = os.path.abspath(filename)
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        cls.logger.addHandler(file_handler)
        cls.log_filename = log_path

    @classmethod
    def log(cls, msg:str, level:str='info') -> None:

        print(f'[{getDate()}][{level}]{msg}')
        if level == 'info':
            cls.logger.info(msg)
        elif level == 'warning':
            cls.logger.warning(msg)
        elif level == 'debug':
            cls.logger.debug(msg)
        elif level == 'error':
            cls.logger.error(msg)
        elif level == 'critical':
            cls.logger.critical(msg)
