"""
Module of data classes that are
serialized and returned to the Interject platform
"""
from typing import Any, List
from pydantic import BaseModel, Field
from idsdata.Models.InterjectEnums import DataFormat, ParameterDataType, SchemaFormat
from idsdata.utils.enums import TableDataType
from idsdata.Models.table import IDSTable,IDSColumn

class ReturnedData(BaseModel):
    data: IDSTable = IDSTable()
    serialized_data = ""
    data_format: int = 2
    schema_name: str = Field(None, alias="schema")
    schema_format: int = 0

    def to_dict(self):
        """Returns dictionary representation of
        InterjectReturnedData that can be json
        serialized. 
        
        Returns:
            [dict] -- dict representation of InterjectReturnedData
        """
        dict_repr = { "Data": self.data.json(),
                      'DataFormat':self.data_format,
                      'Schema': self.schema_name,
                      'SchemaFormat': self.schema_format,
                    }
        return dict_repr



