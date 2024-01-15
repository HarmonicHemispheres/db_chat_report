import pyodbc
import sqlalchemy as sa
from idsdata.services.base_integration import Integration
from idsdata.Models.table import IDSColumn, IDSTable
from loguru import logger

class SQLServer(Integration):
    server: str = ""
    database: str = ""
    username: str = ""
    password: str = ""
    conn_str: str = ""
    conn_url: str
    engine: sa.Engine
    use_win_auth: bool = False

    def __init__(self, server, database, username = "", password = "", use_win_auth = False):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        if username == "" or password == "":
            self.use_win_auth = True
        if use_win_auth:
            self.conn_str = f"DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
        else:
            self.conn_str = f"DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        self.conn_url = sa.URL.create("mssql+pyodbc", query={"odbc_connect": self.conn_str})
        self.engine = sa.create_engine(self.conn_url)

    # Connect to database:
    def connect(self):
        try:
            connection = self.engine.connect()
            return connection
        except Exception as e:
            logger.error("Error connecting to the SQL Server database: " + str(e))
            return None

    # Runs sql query:
    def run_sql(self, query) -> IDSTable:
        connection = self.connect()
        if connection is None:
            return None

        try:
            result = connection.execute(sa.text(query))
        except Exception as e:
            logger.error(f"Error executing the query: " + str(e))
            return None

        table = self.sqlserver_result_to_idstable(result)
        connection.close()
        return table
    
    def sqlserver_result_to_idstable(self, result) -> IDSTable:
        table = IDSTable()

        # Add the rows to the IDSTable:
        for record in result:
            row = list(record.tuple())
            table.add(row)

        # dict_results: sa.Sequence[sa.RowMapping] = results.mappings().all()
        
        # Get the column names from results:
        results_keys = result._metadata.keys._keys

        # Add the column names to the IDSTable:
        for i in range(len(results_keys)):
            col = IDSColumn(ColumnName=results_keys[i], Ordinal=i+1)
            table.Columns.append(col)

        return table
