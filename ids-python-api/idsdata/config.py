############################################
###     IMPORTS
############################################
from pathlib import Path
import json
from pydantic import BaseModel
import importlib
import sys
from loguru import logger
from typing import Union

############################################
###     GLOBALS
############################################
CFG_FILE_NAME = "config.py"
TEMPLATE = """
# domain where api runs
host = "127.0.0.1"

# port where api runs
port = 5555
reload = False
"""

############################################
###     MODELS
############################################
# class Database(BaseModel):
#     conn: str = f"{Path(__file__).parent.parent / 'dataform.db'}"
#     engine: str = "sqlite"

############################################
###     MAIN CONFIG SECTIONS
############################################

class LoggerConfig(BaseModel):
    active: bool = True
    verbose: bool = False
    dir: Path = Path("logs")
    retention: Union[int,str] = 5
    log_portal_calls: bool = False
    log_to_stdout: bool = True


############################################
###     MAIN CONFIG
############################################
class Config(BaseModel):
    host: str = "127.0.0.1"
    port: int = 5555
    reload: bool = False
    issuer: str = "localhost:5555"
    audience: str = "localhost:5555/audience"
    algorithms = []
    logging: LoggerConfig = LoggerConfig()

    def load(self):
        global CFG_FILE_NAME

        path = Path(CFG_FILE_NAME)
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[f"{path.stem}"] = mod
        spec.loader.exec_module(mod)
        

        self.host = getattr(mod, "host")
        self.port = getattr(mod, "port")
        self.reload = getattr(mod, "reload", False)
        self.issuer = getattr(mod, "issuer")
        self.audience = getattr(mod, "audience")
        self.algorithms = getattr(mod, "algorithms")
        # for item in dir(mod):
        #     var = getattr(mod, item)
        #     if isinstance(var, PromptStyle):
        #         self.prompt_style = var
        #         break

    def save(self, file: Path):
        with open(file, 'w+') as fp:
            fp.write(TEMPLATE)
    
    def exists(self):
        return self._CFG_PATH.exists()


############################################
###     CONFIG TEMPLATE
############################################
