import pyodbc
import pandas as pd
import sqlite3
from idsdata.services.base_integration import Integration
from idsdata.Models.table import IDSColumn, IDSTable
from loguru import logger

class SQLite(Integration):
    database_path: str = ""

    def __init__(self, database_path):
        self.database_path = database_path

    # Connect to database:
    def connect(self):
        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()
            return connection, cursor
        except Exception as e:
            logger.error("Error connecting to the sqlite database: {e}")
            return None
    
    # Runs sql query:
    def run_sql(self, query) -> IDSTable:
        connection, cursor = self.connect()
        if connection is None or cursor is None:
            return None

        try:
            cursor.execute(query)
        except Exception as e:
            logger.error(f"Error executing the query: {e}")
            return None

        table = self.sqlite_result_to_idstable(cursor)
        cursor.close()
        return table
    
    def sqlite_result_to_idstable(self, cursor) -> IDSTable:
        # Get the column names from the result description
        column_names = [column[0] for column in cursor.description]

        # Fetch all rows from the result
        rows = cursor.fetchall()

        table = IDSTable()

        # Add the rows to the IDSTable:
        for record in rows:
            table.add(record)

        for i in range(len(column_names)):
            col = IDSColumn(ColumnName=column_names[i], Ordinal=i+1)
            table.Columns.append(col)
        
        return table
        