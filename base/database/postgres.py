"""
database.py
Date: 3/2022
Updated: 6/22/2023
Author: xc383@drexel.edu
Desc: A Postgresql database interface
REF: https://github.com/NCATSTranslator/Explanatory-Agent/blob/master/xARA-ETL/src/clsDatabase.py
"""

# Update Notes
# 8/11/2022: Edited uploadTableViaDataFrame() to support returning clause
# 6/22/2023: Conformed class to pep styling

import psycopg2
import psycopg2.extras
from base import Database

class Postgres(Database):
    def __init__(self, host: str, database: str, user: str, password: str):
        """
        Constructor
        """
        super().__init__()
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password

    def connect(self):
        """
        Connect to Postgresql
        :return: None
        """
        super().connection = psycopg2.connect(
            host=self.__host,
            database=self.__database,
            user=self.__user,
            password=self.__password
        )

if __name__ == '__main__':

    credentials = {
        "host": "",
        "database": "aact",
        "user": "xc383@drexel.edu",
        "password": ""
    }

    print("Connecting to database")
    db = Postgres(**credentials)
    db.connect()

    print("Querying database")
    df = db.execute(sql="select current_timestamp", expecting_return=True)
    print(df)

    print("Disconnecting from database")
    db.disconnect()