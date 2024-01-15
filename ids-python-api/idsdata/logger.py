from idsdata.config import LoggerConfig
from pathlib import Path
from loguru import logger
import sys
from datetime import datetime

class Logger():
    def __init__(self, config: LoggerConfig = LoggerConfig(), base_path: Path = Path(".")):
        self.cfg = config
        logger.remove()

        run_stamp = f'ids_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
        log_format = "<green>{time:YYYY-MM-DD:ddd:HH-mm.ss}</green> | <level>{level:<8}</level> | <le>{module}:{function}:{line}</le> - <lvl>{message}</lvl>"
        file_name_fmt = "ids_{time:YYYY-MM-DD_HH-mm-ss}.log"

        if self.cfg.verbose:
            level = "DEBUG"
        else:
            level = "INFO"


        if self.cfg.active and self.cfg.log_to_stdout:
            logger.add(sys.stdout, 
                       format=log_format, 
                       level=level,
                       colorize=True,
            )

        if self.cfg.active and self.cfg.dir:
            outpath: Path = base_path / self.cfg.dir
            outpath.mkdir(parents=True, exist_ok=True)
            logpath = outpath / file_name_fmt
            logger.add(logpath, 
                       format=log_format, 
                       level=level,
                       retention=self.cfg.retention)

        logger.debug("Configured Logger")
        self.logger = logger
    
    def debug(self, msg):
        if self.cfg.active:
            self.logger.debug(msg)
    
    def info(self, msg):
        if self.cfg.active:
            self.logger.info(msg)
    
    def success(self, msg):
        if self.cfg.active:
            self.logger.success(msg)
    
    def warning(self, msg):
        if self.cfg.active:
            self.logger.warning(msg)
    
    def error(self, msg):
        if self.cfg.active:
            self.logger.error(msg)
    
    def critical(self, msg):
        if self.cfg.active:
            self.logger.critical(msg)
