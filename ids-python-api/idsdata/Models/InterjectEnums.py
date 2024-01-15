
"""
Module containing enums used in IdsDataModel classes
"""
from enum import Enum

class ParameterDataType(Enum):
    NONE = 0
    VARCHAR = 1
    VARCHARMAX = 2
    NVARCHAR = 3
    NVARCHARMAX = 4
    TEXT = 5
    NTEXT = 6
    CHAR = 7
    NCHAR = 8
    BIGINT = 9
    INT = 10
    SMALLINT = 11
    TINYINT = 12
    BOOLEAN = 13
    BIT = 14
    MONEY = 15
    SMALLMONEY = 16
    FLOAT = 17
    REAL = 18
    SINGLE = 19
    DOUBLE = 20
    DECIMAL = 21
    DATETIME = 22
    SMALLDATETIME = 23
    DATE = 24

    def __str__(self):
        return self.name

class TableDataType(Enum):
    NONE = 0
    STRING = 1
    DATETIME = 2
    BOOLEAN = 3
    DECIMAL = 4
    SINGLE = 5
    DOUBLE = 6
    INT64 = 7
    INT32 = 8
    INT16 = 9
    BYTE = 10
    GUID = 11

    def __str__(self):
        # .NET is case-sensitive with datatypes
        # so we must treat DATETIME as 'DateTime' instead of 'Datetime'
        if self.value == self.DATETIME.value:
            return "DateTime"
        else:
            return self.name.capitalize()

class CommandType(Enum):
    NONE = 0
    STOREDPROCEDURE = 1
    TABLEDIRECT = 2
    TEXT = 3

class DataFormat(Enum):
    NONE = 0
    XMLSTRING = 1
    JSONTABLEWITHSCHEMA = 2
    JSONTABLE = 3
    DATASET = 4

class SchemaFormat(Enum):
    NONE = 0
    INTERJECT_OBJECT = 1
    XML_FirstRowAttribute = 2

class DbDriverType(Enum):
    NONE = 0
    ODBC = 1
    MSSQL = 2
    MYSQL = 3
    SQLITE = 4
    POSTGRESQL = 5
    ORACLE = 6
