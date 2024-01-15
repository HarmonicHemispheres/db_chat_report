# Add Endpoint For Save



```python
@APP.post("/example-save", response_model=InterjectResponse)
async def data(request: InterjectRequest):
    global CONFIG

    try:
        # 1. get json data from request and create interject request object
        # get json data from request and create interject request object
        xml_data_to_save = request.get_param("Interject_XMLDataToSave")
        xml_data: IDSXMLParser = IDSXMLParser().parse(xml_data_to_save.InputValue)

        # 2. process xml data from the request
        print(xml_data.dict())

    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=f"Request had issues: {error}")

    # 3. create response to return
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=[],
        ReturnedDataList=[]
    )

    return response
```