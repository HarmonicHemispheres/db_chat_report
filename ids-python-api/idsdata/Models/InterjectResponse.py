"""
Module defining the InterjectResponse class.
"""
from typing import Any, Dict, List
from pydantic import BaseModel
from idsdata.Models.RequestParameter import RequestParameter


class InterjectResponse(BaseModel):
    UserMessage: str = ""
    ErrorMessage: str = ""
    RequestParameterList: List[RequestParameter] = []
    ReturnedDataList: List[Any] = []
    SupplementalData: Dict[str, Any] = {}


    def set_msg_based_on_prefix(self, error_msg):
        """Sets the response error variable based on the
        contents of error_msg. If no prefix is found then
        set the error_message variable.

        Arguments:
            error_msg {str} -- error message to find prefixes.
        """

        self.UserMessage = ""
        self.ErrorMessage = ""

        notice_prefix = 'usernotice:'
        error_prefix = 'usererror:'

        err_index = error_msg.lower().find(error_prefix)
        notice_index = error_msg.lower().find(notice_prefix)

        if notice_index >= 0:
            self.UserMessage = error_msg[notice_index:] 
        elif err_index >= 0:
            self.ErrorMessage = error_msg[err_index:]
        else:
            self.ErrorMessage = error_msg
            
