import mysql.connector
import Credentials as creds

def get_Connection():
    for server in creds.servers:
        try:
            mydb = mysql.connector.connect(
                host=server["host"],
                user=server["user"],
                password=server["password"],
                database=server["database"]
            )
            return mydb
        except Exception as e:
            print(e)