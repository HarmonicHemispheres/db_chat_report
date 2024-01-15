"""
Module of data classes that are
serialized and returned to the Interject platform
"""
from typing import Any, List
from pydantic import BaseModel, Field
from idsdata.Models.xml_datatosave_parser import IDSXMLDataToSaveParser
from idsdata.Models.InterjectEnums import DataFormat, ParameterDataType, SchemaFormat
from idsdata.utils.enums import TableDataType
from copy import deepcopy
import pandas as pd

class IDSColumn(BaseModel):
    AllowDBNull: bool = True
    Caption: str = ""
    ColumnName: str = ""
    # DataType: TableDataType = TableDataType.STRING
    # DataType: ParameterDataType = ParameterDataType.VARCHARMAX
    DataType: str = "String"
    MaxLength: int = -1
    Ordinal: int = 0
    # The last few columns are not necessary for the Interject platform
    # but are required due to how the returned json data is de-serialized
    AutoIncrement: bool = False
    AutoIncrementSeed: int = 0
    AutoIncrementStep: int = 1
    DateTimeMode: str = "UnspecifiedLocal"
    DefaultValue: Any = None
    ReadOnly: bool = False
    Unique: bool = False

class IDSTable(BaseModel):
    TableName: str = "Table" # must be unique to other InterjectTableObjects in returned list
    Columns: List[IDSColumn] = [] # list of InterjectColumnObjects
    Rows: List[List[Any]] = [] # list of lists of values representing data values
    PrimaryKey = [] # not used

    def __repr__(self) -> str:
        return f"""{self.TableName}
        {self.to_dataframe()}
        """

    def add(self, row: List[Any], force: bool = False):
        if force:
            self.Rows.append(row)
        else:
            for val, col in zip(row, self.Columns):
                #
                # ... run validation and checks for columns
                #
                pass
            self.Rows.append(row)
    
    def delete(self, idx: int):
        if len(self.Rows) >= idx:
            del self.Rows[idx]
    
    def replace(self, idx, new_row):
        """replace a row by index"""
        if len(self.Rows) >= idx:
            self.Rows[idx] = new_row

    def filter(self, filter_obj) -> "IDSTable":
        new_table: "IDSTable" = deepcopy(self)
        new_table.Rows = []
        col_indexes = {key.ColumnName:idx for idx,key in enumerate(self.Columns)}
        

        for row in self.Rows:
            for colkey, val in filter_obj.items():
                index_to_test = col_indexes.get(colkey)
                column: IDSColumn = new_table.Columns[index_to_test]
            
                if column and val in row[index_to_test]:
                    new_table.add(row)
        return new_table


    def col_index(self, column_name: str):
        col_indexes = {key.ColumnName:idx for idx,key in enumerate(self.Columns)}
        return col_indexes.get(column_name, None)
  
    def get_column_names(self):
        return [
            cols.ColumnName for cols in self.Columns
        ]

    def to_dataframe(self):
        return pd.DataFrame(data=self.Rows, columns=self.get_column_names())

    def from_dataframe(self, df: pd.DataFrame):
        for i in range(len(df.columns)):
            col = IDSColumn(ColumnName=df.columns[i], Ordinal=i)
            self.Columns.append(col)
        for i in range(len(df)):
            self.Rows.append(df.loc[i, :].values.flatten().tolist())

    def load_XMLDataToSave(self, xml: str):

        xml_data: IDSXMLDataToSaveParser = IDSXMLDataToSaveParser().parse(xml)
        
        # -- build columns for table
        self.Columns = []
        for idx, column in enumerate(xml_data.columns):
            self.Columns.append(
                IDSColumn(
                    ColumnName=column.name,
                    Ordinal=idx
                )
            )

        # -- build rows
        self.Rows = []
        for idx, row in enumerate(xml_data.rows):
            self.Rows.append(
                row
            )

        return self
    


    