# New Pull Example

### with XML changes from the addin.

Example Code for endpoint.

```python
@APP.post("/project-pull-newXml", response_model=InterjectResponse)
async def data(request: InterjectRequest):
    global CONFIG

    table = IDSTable(
        TableName="Table",
        Columns=[],
        Rows=[]
    )
    # get data
    for col in request.RequestContext.ColDefItems:
        if col.RowDef == None:
            table.Columns.append(
                IDSColumn(ColumnName = col.Value)
            )

    num = 0
    for row in request.RequestContext.RowDefItems:
        div = row.get_value("Div")
        acct = row.get_value("Acct")

        num = num + 1
        table.add([
            div,
            acct,
            f"account_{num}",
            10000.99,
            13000.99,
            50200.34,
        ])


    # if request.get_param("client").InputValue != "":
    #     table = table.filter({
    #         "Client": request.get_param("client").InputValue
    #         })

    table2 = table.copy()
    table2.TableName = "Table2"

    # create response
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=request.RequestParameterList,
        ReturnedDataList=[
            ReturnedData(data=table).to_dict(),
            ReturnedData(data=table2).to_dict(),
        ]
    )
    return response
```

How this API parses the new xml from the Request Context.

```python


```
