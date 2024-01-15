
from typing import Optional
from idsdata.Models.InterjectEnums import ParameterDataType
from pydantic import BaseModel


class RequestParameter(BaseModel):
    Name: str = ""
    DataType: int = 1
    ExpectsOutput: bool = False
    InFormula: bool = False
    InputValue: str = ""
    OutputValue: str = ""
    UserValidationMessage: str = ""
    DefaultValue: Optional[str] = ""
