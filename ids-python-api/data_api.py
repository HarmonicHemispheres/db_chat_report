from idsdata import *
import uvicorn
from fastapi import FastAPI
from openai import OpenAI
import os
import duckdb
import uuid
import datetime
import json

# [NOTE] use this to manually set your openai api key rather then reading from an environment variable  
# os.environ["OPENAI_API_KEY"] = "sk-???????????????????????????????"

API = FastAPI()

# Set-Item -Path Env:OPENAI_API_KEY -Value ($Env:OPENAI_API_KEY + ";<new-value>")
AI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )
con = duckdb.connect("file.db")

# ---------------------------- #
# -------- GPT MODELS -------- #
# ---------------------------- #
# gpt-4-1106-preview
# gpt-3.5-turbo-1106
# gpt-3.5-turbo
# gpt-4
MODEL = "gpt-4-1106-preview"
def insert_logs(sid=None, status=None, tags=None, prompt=None, query="", created=None):

    if not sid:
        sid = str(uuid.uuid4())[:7]
    
    if not created:
        created = datetime.datetime.now()

    SQL = f"INSERT INTO logs (sid, created, status, tags, prompt, query) VALUES (?,?,?,?,?,?);"
    con.execute(SQL, [sid, created, status, tags, prompt, query])

@API.post("/get_prompts", response_model=InterjectResponse)
async def get_prompts(request: InterjectRequest):

    result = con.sql("SELECT prompt FROM (SELECT prompt, MAX(created) AS cr FROM logs GROUP BY prompt ORDER BY cr DESC LIMIT 20)")
    print(result)

    # --- get data
    table: IDSTable = IDSTable(
        TableName="Table",
        Columns=[IDSColumn(ColumnName="Prompt", Ordinal=1),],
        Rows=list(result.fetchall())
    )

    # create response
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=request.RequestParameterList,
        ReturnedDataList=[
            ReturnedData(data=table).to_dict()
        ]
    )
    return response


@API.post("/the_one_call", response_model=InterjectResponse)
async def the_one_call(request: InterjectRequest):
    
    data_cols = []
    rows = []

    result = con.sql("SHOW ALL TABLES;")
    all_tables = f"ALL TABLES:\n{result.fetchall()}\n\n"
    print(all_tables)

    try:
        # --- process request for actions
        prompt: str = request.get_param("prompt").InputValue
    
        print("PROMPT:   ", prompt)
            
        SYS_MESSAGE = """
    you are a duckdb database management engine. when the user sends a request you return one of the 
    following json response templates:

    - "READ" : "<sql query>"
    - "WRITE" : "<sql query for creating or inserting data>"
        """
            
        PROMPT_TEMPLATE = f"""
PROMPT:        
{prompt}

TABLES:
{all_tables}
        """

        print(PROMPT_TEMPLATE)

        chat_completion = AI.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYS_MESSAGE
                },
                {
                    "role": "user",
                    "content": PROMPT_TEMPLATE,
                }
            ],
            model=MODEL,
            response_format={"type": "json_object"},
            # temperature=0
        )

        sql = chat_completion.choices[0].message.content
        print("RESPONSE:  ", sql)
        sql_dict = json.loads(sql)

        ##############################
        # READ
        ##############################
        if "READ" in sql_dict:
            result = con.sql(sql_dict['READ'])
            result.show()

            # --- build columns
            # Get column names
            column_names = result.description
            print(column_names)

            # Print column names
            for idx,col in enumerate(column_names):
                data_cols.append(
                    IDSColumn(ColumnName=col[0], Ordinal=idx)
                )

            print(data_cols)
            
            # Fetch and print rows of data
            rows = list(result.fetchall())
            print("R:   ", rows)

            sql = f"READ -- {sql_dict['READ']}"
            insert_logs(status="INFO", tags="READ", prompt=prompt, query=sql_dict['READ'])


        ##############################
        # WRITE
        ##############################
        elif "WRITE" in sql_dict:
            result = con.sql(sql_dict['WRITE'])
            sql = f"WRITE -- {sql_dict['WRITE']}"
            insert_logs(status="INFO", tags="WRITE", prompt=prompt, query=sql_dict['WRITE'])

    except Exception as error:
        sql = f"ERROR -- {error}"
        insert_logs(status="ERROR",tags="",prompt=str(error))
    
    # --- get data
    table: IDSTable = IDSTable(
        TableName="Table",
        Columns=[IDSColumn(ColumnName="MSG", Ordinal=1),],
        Rows=[[sql,],]
    )

    table2: IDSTable = IDSTable(
        TableName="Table2",
        Columns=data_cols,
        Rows=rows
    )

    # create response
    response: InterjectResponse = InterjectResponse(
        RequestParameterList=request.RequestParameterList,
        ReturnedDataList=[
            ReturnedData(data=table).to_dict(),
            ReturnedData(data=table2).to_dict(),
        ]
    )
    return response

if __name__ == '__main__':
    cfg = Config()
    cfg.load()

    # ---- SETUP DB ---- #
    SQL = "CREATE TABLE IF NOT EXISTS logs (sid VARCHAR, created TIMESTAMP, status VARCHAR, tags VARCHAR, prompt VARCHAR, query VARCHAR);"
    con.sql(SQL)


    uvicorn_config = uvicorn.Config("data_api:API", 
                                    host=cfg.host,
                                    port=cfg.port, 
                                    log_level="info",
                                    reload=cfg.reload
                                    )
    server = uvicorn.Server(uvicorn_config)
    server.run()
