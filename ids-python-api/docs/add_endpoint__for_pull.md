# Add Endpoint For Pull



```python
@APP.post("/example-pull", response_model=InterjectResponse)
async def data(request: InterjectRequest):
    global CONFIG

    # 1. get json data from request and create interject request object
    # get json data from request and create interject request object
    # request_dto = self.parse_request(request)
    try:
        req_data = request.dict()
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Request had issues: {error}")

    # 2. process request i.e. execute DB pass through command or another api call
    response: InterjectResponse = InterjectResponse()

    # 3. Initialize Response DTO and convert your dataset(s) to InterjectReturnedData objects
    # BELOW is an example of the InterjectResponse that would be returned
    # The dataset is hardcoded in this example
    table = IDSTable(
        TableName="Table",
        Columns=[
            IDSColumn(ColumnName="FirstName", Ordinal=0),
            IDSColumn(ColumnName="LastName", Ordinal=1),
            IDSColumn(ColumnName="Email", Ordinal=2),
            ]
    )
    table.add(["Joe", "Moe", "jmoe@example.com"])
    table.add(["Mary", "Loe", "mloe@example.com"])

    returned_data = ReturnedData(data=table)

    # 4. returned_data_list can handle multiple InterjectReturnedData objects
    response.ReturnedDataList.append(returned_data.to_dict())

    return response
```