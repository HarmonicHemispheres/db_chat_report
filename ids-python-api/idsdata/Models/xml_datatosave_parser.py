from typing import List, Any
from pydantic import BaseModel
import xml.etree.ElementTree as ET
from loguru import logger

class XMLColumn(BaseModel):
    name: str = ""
    orig_value: str = ""
    row_data: List[Any] = []

class IDSXMLDataToSaveParser(BaseModel):
    columns: List[XMLColumn] = []
    rows: List[Any] = []

    def _get_col_row_data(self, idx:int):
        rows = []
        for row in self.rows:
            rows.append(
                row[idx]
            )
        return rows

    def parse(self, xml_text: str):
        """loads data from an xml string into self"""
        self.columns = []
        self.rows = []

        try:
            root = ET.fromstring(xml_text)

            for child in root: 
                if child.tag == "c":
                    self.columns.append(XMLColumn(
                        name=child.attrib.get("Column"),
                        orig_value=child.attrib.get("OrigValue"),
                    ))
                
                elif child.tag == "r":
                    row_data = []
                    for row in child:
                        row_data.append(row.text)
                    self.rows.append(row_data)
            return self

        except Exception as error:
            logger.error(error)


    def get_column(self, name: str, with_rows: bool = False) -> XMLColumn:
        for idx, col in enumerate(self.columns):
            if col.name.lower() == name.lower():
                if with_rows:
                    col.row_data = self._get_col_row_data(idx)
                return col

