## importing 'mysql.connector' as mysql for convenient
import mysql.connector as mysql

mydb = mysql.connect(
  host=server["host"],
  user=server["user"],
  password=server["password"],
  database=server["database"]

)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE TRIP_DETAILS")
