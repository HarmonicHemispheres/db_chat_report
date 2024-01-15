from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer
from idsdata.Models.InterejectReturnedData import IDSColumn, IDSTable, ReturnedData
from idsdata.Models.InterjectRequest import InterjectRequest
from idsdata.Models.InterjectResponse import InterjectResponse
from idsdata.config import Config
from idsdata.logger import Logger
from idsdata.services.integrations.sqlServer import SQLServer
from idsdata.utils.verify_token import VerifyToken
from logging.config import dictConfig
from loguru import logger

# package for reading details about this package
import pkg_resources


#########################################
######           GLOBALS           ######
#########################################
CONFIG = None
DB = None
PKG_NAME = "idsdata"


##########################################################################
######           PRIMARY API ENDPOINTS STARTUP & SHUTDOWN           ######
##########################################################################
def create_ids_api():
    global CONFIG
    # global logging

    CONFIG = Config()
    CONFIG.load()

    init_logger(Path("config.py").parent.absolute())

    return FastAPI()

def create_auth_scheme():
    return HTTPBearer()

def init_logger(base_log_path: Path):
    logging = Logger(config=CONFIG.logging, base_path=base_log_path)
    

################################################
######           DEMO API SETUP           ######
################################################
AUTH_SCHEME = create_auth_scheme()
APP = create_ids_api()


@APP.on_event("shutdown")
async def app_shutdown():
    pass


#######################################################
######           PRIMARY API ENDPOINTS           ######
#######################################################
@APP.get("/")
async def root():
    """Check if the API is running"""
    return {"message": "ids data api is online!"}


@APP.get("/version")
async def version():
    """Get the version of this API"""
    return {
        "name": "interject python data api",
        "version": pkg_resources.get_distribution(PKG_NAME).version
        }


@APP.post("/example-auth", response_model=InterjectResponse)
async def example_auth(request: InterjectRequest, token: str = Depends(AUTH_SCHEME)):
    """Authenticates enterprise login token"""
    global CONFIG

    result = VerifyToken(token.credentials,CONFIG).verify()

    # get data
    table = IDSTable(
        TableName="Table",
        Columns=[
            IDSColumn(ColumnName="Result", Ordinal=1),
            ],
        Rows=[]
    )

    table.add([
            str(result),
        ])

    # create response
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=request.RequestParameterList,
        ReturnedDataList=[
            ReturnedData(data=table).to_dict(),
        ]
    )

    return response


@APP.post("/example-pull", response_model=InterjectResponse)
async def example_pull(request: InterjectRequest):
    """Returns sample report data to Interject"""
    global CONFIG

    # get data
    table = IDSTable(
        TableName="Table",
        Columns=[
            IDSColumn(ColumnName="Name", Ordinal=1),
            IDSColumn(ColumnName="Start Date", Ordinal=2),
            IDSColumn(ColumnName="Finish Date", Ordinal=3),
            IDSColumn(ColumnName="Manager", Ordinal=4),
            IDSColumn(ColumnName="Client", Ordinal=5),
            IDSColumn(ColumnName="Cost", Ordinal=6),
            IDSColumn(ColumnName="Bid", Ordinal=7),
            ],
        Rows=[]
    )

    table.add([
            "Project One",
            "11/25/2025",
            "1/15/2026",
            "Manny Leverly",
            "Apparent Technologies",
            50_200.34,
            55_054.00,
        ])

    table.add([
            "New Roof",
            "10/25/2025",
            "3/15/2026",
            "Manny Leverly",
            "Marlyn Mowery",
            15_600.34,
            20_000.00,
        ])

    table.add([
            "home Remodel",
            "10/25/2025",
            "3/15/2026",
            "Janice Owens",
            "Marlyn Mowery",
            15_600.34,
            20_000.00,
        ])

    table.add([
            "Office Window Replacement",
            "10/25/2025",
            "3/15/2026",
            "Janice Owens",
            "Tower Radio",
            50_900.00,
            72_870.00,
        ])

    if request.get_param("client").InputValue != "":
        table = table.filter({
            "Client": request.get_param("client").InputValue
            })
    
    
    table2 = table.copy()
    table2.TableName = "Table2"

    # create response
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=request.RequestParameterList,
        ReturnedDataList=[
            ReturnedData(data=table).to_dict(),
            ReturnedData(data=table2).to_dict(),
        ]
    )

    return response

@APP.post("/example-pull-sqlserver", response_model=InterjectResponse)
async def example_dbpull_sqlserver(request:InterjectRequest):
    """Connects to SQL Server database and retrieves data via query"""
    global CONFIG

    sql_object = SQLServer(server = "(local)", database = "StudentDetails")
    query = "Select * from dbo.Student"
    table = sql_object.run_sql(query)

    if request.get_param("client").InputValue != "":
        table = table.filter({
            "Client": request.get_param("client").InputValue
            })

    # create response
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=request.RequestParameterList,
        ReturnedDataList=[
            ReturnedData(data=table).to_dict(),
        ]
    )
    return response

@APP.post("/example-save", response_model=InterjectResponse)
async def example_save(request: InterjectRequest):
    """Performs an example Interject ReportSave"""
    global CONFIG

    table: IDSTable = request.XMLDataToSave

    notice_col_idx = table.col_index("SaveNotice")
    for row in table.Rows:
        row[notice_col_idx] = "row saved to database!"

    response: InterjectResponse = InterjectResponse(
        RequestParameterList=[],
        ReturnedDataList=[
            ReturnedData(data=table).to_dict(),
        ]
    )

    return response

@APP.post("/unauthorized", response_model=InterjectResponse)
async def unauthorized(request: InterjectRequest):
    """Returns an unauthorized status response"""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    return "Unauthorized"
