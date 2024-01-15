"""
Copyright <<year>> <<insert publisher name>>
DESCRIPTION:
    this is a sample Typer CLI layout
USAGE EXAMPLE:
    > python template_simple_cli.py example_cmd
"""


# ::IMPORTS ------------------------------------------------------------------------ #

# cli framework - https://pypi.org/project/typer/
import json
import typer

# data types for validation - https://docs.python.org/3/library/typing.html
from typing import Optional

# cross platform path handling - https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# package for reading details about this package
import pkg_resources

# project imports
import uvicorn

from idsdata.config import Config


# ::SETUP -------------------------------------------------------------------------- #
app = typer.Typer(
    add_completion=False,
    no_args_is_help=True
    )

# ::SETUP SUBPARSERS --------------------------------------------------------------- #
# app.add_typer(<<module.app>>, name="subparser")

PKG_NAME = "idsdata"

# ::CORE LOGIC --------------------------------------------------------------------- #
# place core script logic here and call functions
# from the cli command functions to separate CLI from business logic

# ::CLI ---------------------------------------------------------------------------- #
@app.command()
def create_config(dev: bool = False):
    config = Config()
    config.save(Path("./config.py"))

@app.command()
def config():
    config = Config()
    config.load()
    print(json.dumps(config.dict(), indent=3))

# @app.command()
# def run(module: str = "idsdata.app:APP", dev: bool = False):
#     cfg = Config()
#     cfg.load()
    
#     uvicorn_config = uvicorn.Config(module, 
#                                     host=cfg.host,
#                                     port=cfg.port, 
#                                     log_level="info",
#                                     reload=cfg.reload
#                                     )
#     server = uvicorn.Server(uvicorn_config)
#     server.run()

@app.command()
def version():
    """
    get the version of the package
    """
    version = pkg_resources.get_distribution(PKG_NAME).version
    typer.echo(version)



# ::EXECUTE ------------------------------------------------------------------------ #
def main():
    app()


if __name__ == "__main__":  # ensure importing the script will not execute
    main()
