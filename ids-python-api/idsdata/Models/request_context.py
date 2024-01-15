"""
Module defining the InterjectRequest class.
"""
from pathlib import Path
import json
from typing import Any, Dict, List, Optional
from idsdata.Models.table import IDSTable, IDSColumn
import logging
import xml.etree.ElementTree as ET
from pydantic import BaseModel, validator, root_validator
from loguru import logger

class ColRowDefItem(BaseModel):
    Row: int = None
    Column: int = None
    ColumnName: str = None
    Value: Any = None

class ColDefItem(BaseModel):
    Row: int = None
    Column: int = None
    RowDef: bool = None
    Value: Any = None
    Json: Dict = None

class ColKey(BaseModel):
    Order: int = None
    Column: int = None
    Name: str = None
    Value: Any = None

class RowDefItem(BaseModel):
    Row: int = None
    RowDefName: str = None
    ColKeys: List[ColKey] = None
    Value: Any = None

    def get_value(self,name:str):
        for colkey in self.ColKeys:
            if colkey.Name == name:
                return colkey.Value
        return ""

class UserContext(BaseModel):
    MachineLoginName: str = ""
    MachineName: str = ""
    FullName: str = ""
    UserId: str = ""
    ClientId: str = ""
    LoginName: str = ""
    LoginAuthTypeId: int = 0
    LoginDateUtc: Optional[str] = None
    UserRoles: List[str] = []

class IDSRequestContext(BaseModel):
    ExcelVersion: Optional[str] = None
    IdsVersion: Optional[str] =  None
    FileName: Optional[Path] = None
    FilePath: Optional[Path] = None
    TabName: Optional[str] = None
    CellRange: Optional[str] = None
    SourceFunction: Optional[str] = None
    UtcOffset: Optional[int] = None
    ColDefItems: List[ColDefItem] = []
    RowDefItems: List[RowDefItem] = []
    ResultDefItems: List[Any] = []
    UserContext: Optional[str] = None
    UserContextEncrypted: Optional[str] = None
    XMLDataToSave: Optional[IDSTable] = None

        
    def load(self, xml: str):
        try:
            root = ET.fromstring(xml)

            for child in root: 
                if child.tag == "ExcelVersion":
                    self.ExcelVersion = child.text
                elif child.tag == "IdsVersion":
                    self.IdsVersion = child.text
                elif child.tag == "FileName":
                    self.FileName = Path(child.text)
                elif child.tag == "FilePath":
                    self.FilePath = Path(child.text)
                elif child.tag == "TabName":
                    self.TabName = child.text
                elif child.tag == "CellRange":
                    self.CellRange = child.text
                elif child.tag == "SourceFunction":
                    self.SourceFunction = child.text
                elif child.tag == "UtcOffset":
                    self.UtcOffset = int(child.text)
                elif child.tag == "ColDefItems":
                    self.ColDefItems = []
                    for row in child:
                        data_row = row.attrib.get("Row")
                        data_column = row.attrib.get("Column")
                        data_rowdef = row.attrib.get("RowDef")
                        data_name = row.find("Name").text
                        data_json = row.find("Json")
                        if isinstance(data_json,ET.Element):
                            data_json = json.loads(data_json.text)
                        self.ColDefItems.append(
                            ColDefItem(
                                Row = data_row,
                                Column = data_column,
                                RowDef = data_rowdef,
                                Value = data_name,
                                Json = data_json
                            )
                        )
                elif child.tag == "RowDefItems":
                    self.RowDefItems = []
                    for row in child:
                        data_row = row.attrib.get("Row")
                        data_column = row.attrib.get("Column")
                        data_columnname = row.attrib.get("ColumnName")
                        data_name = row.find("Name").text
                        self.RowDefItems.append(
                            RowDefItem(
                                Row = data_row,
                                Column = data_column,
                                ColumnName = data_name,
                                Value = data_columnname
                            )
                        )
                elif child.tag == "RowDefItems2":
                    self.RowDefItems = []
                    for row in child:
                        data_row = row.attrib.get("Row")
                        data_rowdef_name = row.attrib.get("RowDefName")
                        data_colkeys = []
                        for ck in row:
                            data_order = ck.attrib.get("Order")
                            data_column = ck.attrib.get("Column")
                            data_name = ck.attrib.get("Name")
                            data_value = ck.text
                            data_colkeys.append(
                                ColKey(
                                Order = data_order,
                                Column = data_column,
                                Name = data_name,
                                Value = data_value
                                )
                            )
                        self.RowDefItems.append(
                            RowDefItem(
                                Row = data_row,
                                RowDefName = data_rowdef_name,
                                ColKeys = data_colkeys,
                                Value = data_columnname
                            )
                        )
                elif child.tag == "ResultDefItems":
                    self.ResultDefItems = []
                    for row in child:
                        data_row = row.attrib.get("Row")
                        data_column = row.attrib.get("Column")
                        data_columnname = row.attrib.get("ColumnName")
                        data_name = row.find("Name").text
                        self.ResultDefItems.append(
                            ColRowDefItem(
                                Row = data_row,
                                Column = data_column,
                                ColumnName = data_name,
                                Value = data_columnname
                            )
                        )
                elif child.tag == "UserContext":
                    self.UserContext = UserContext(
                        MachineLoginName=child.find("MachineLoginName").text,
                        MachineName=child.find("MachineName").text,
                        FullName=child.find("FullName").text,
                        UserId=child.find("UserId").text,
                        ClientId=child.find("ClientId").text,
                        LoginName=child.find("LoginName").text,
                        LoginAuthTypeId=child.find("LoginAuthTypeId").text,
                        LoginDateUtc=child.find("LoginDateUtc").text,
                        UserRoles=[
                            role.text for role in child.find("UserRoles")
                        ]
                    )
                elif child.tag == "XMLDataToSave":
                    self.load_XMLDataToSaveParser(child)

        except Exception as error:
            logger.error(error)

        return self

    def load_XMLDataToSaveParser(self, xml):
        """loads data from an xml string into self"""
        columns = []
        rows = []

        for idx, child in enumerate(xml): 
            if child.tag == "c":
                columns.append(IDSColumn(
                    ColumnName=child.attrib.get("Column"),
                    Ordinal=idx,
                    # orig_value=child.attrib.get("OrigValue"),
                ))
            
            elif child.tag == "r":
                row_data = []
                for row in child:
                    row_data.append(row.text)
                rows.append(row_data)
        
        self.XMLDataToSave = IDSTable(
            Columns=columns,
            Rows=rows
        )
