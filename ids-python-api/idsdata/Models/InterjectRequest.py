"""
Module defining the InterjectRequest class.
"""
from typing import Any, Dict, List, Optional
from idsdata.Models.table import IDSTable
from idsdata.Models.RequestParameter import RequestParameter
from idsdata.Models.InterjectEnums import CommandType
from idsdata.Models.InterjectEnums import ParameterDataType
from idsdata.Models.request_context import IDSRequestContext
import logging
import xml
from pydantic import BaseModel, validator, root_validator


class PassThroughCmd(BaseModel):
    ConnectionStringName: Optional[str] = ""
    OnConnectionStringLookup: Optional[str] = ""
    CommandType: Optional[int] = 0
    CommandText: Optional[str] = ""
    CommandTimeout: Optional[int] = 0


class InterjectRequest(BaseModel):
    DataPortalName: str = ""
    RequestParameterList: List[RequestParameter] = []
    SupplementalData: Dict[str, Any] = {}
    PassThroughCommand: PassThroughCmd = PassThroughCmd()

    # Formula Parameters Already Parsed
    # _RequestContext: Optional[IDSRequestContext] = PrivateAttr()
    # _XMLDataToSave: Optional[IDSTable] = PrivateAttr()
    # _ExcelVersion: Optional[str] = PrivateAttr()
    RequestContext: Optional[IDSRequestContext] = None
    XMLDataToSave: Optional[IDSTable] = None
    ExcelVersion: Optional[str] = None


    def __init__(self, *args, **kwargs):

        # Do Pydantic validation
        super().__init__(*args, **kwargs)

        # 
        for param in self.RequestParameterList:
            if 'XMLDataToSave' in param.Name:
                self.XMLDataToSave = IDSTable().load_XMLDataToSave(param.InputValue)
            elif 'RequestContext' in param.Name:
                self.RequestContext = IDSRequestContext().load(param.InputValue)


    def get_param(self, name: str, default=RequestParameter()) -> RequestParameter:
        for p in self.RequestParameterList:
            if p.Name.startswith("@"):
                p_name = p.Name[1:]
            else:
                p_name = p.Name

            if p_name.lower() == name.lower():
                return p
        return default

