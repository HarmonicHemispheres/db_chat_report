from enum import Enum


#  Used to convert python data api types for C# to SQL types
class DATATABLE_DATATYPES(Enum):
    String = 'VARCHAR'
    Int16 = 'INT'
    Int32 = 'INT'
    Int64 = 'INT'
    Double = 'FLOAT'
    Single = 'FLOAT'
    Datetime = 'DATETIME'
    Boolean = 'BOOL'
    Byte = 'BIT'


    
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