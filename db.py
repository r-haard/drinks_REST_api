import pyodbc
import os
from dotenv import load_dotenv

load_dotenv(override=True)

connection_string = f"""
DRIVER={os.getenv('odbc_driver')};
SERVER={os.getenv('server_name')};
DATABASE={os.getenv('db_name')};
UID={os.getenv('username')};
PWD={os.getenv('password')};
Trusted_Connection=no;
"""

class DB:
    def call_db(self, query: str, *args):
        conn = pyodbc.connect(connection_string)
        if query.strip().lower().startswith("select"):
            cur = conn.cursor()
            res = cur.execute(query, args)
            data = res.fetchall()
            cur.close()
        else:
            conn.execute(query, args)
            data = None
        conn.commit()
        conn.close()
        return data

def main():
    db = DB()
    query = open("db_setup/drinks_db_init.sql", "r")
    query = query.read()
    db.call_db(query)


if __name__ == "__main__":
    main()

#test
# query = """
# SELECT * FROM ingredient WHERE ingredient_id = ?
# """
# db = DB()
# a = db.call_db(query, 1)
# print(a)