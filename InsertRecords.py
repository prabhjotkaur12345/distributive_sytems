'''
This script -
inserts a row to the table 'trip_details' in the database 'mydatabase'
'''
import mysql.connector

mydb = mysql.connector.connect(
  host=server["host"],
  user=server["user"],
  password=server["password"],
  database=server["database"]
)

mycursor = mydb.cursor()
mycursor.execute("SET time_zone='+01:00'")
# query = "INSERT INTO trip_details (tripId, owner_unique_Id, source, destination, route_taken, vehicle_number) VALUES (%s, %s,%s, %s,%s, %s)"
# val = ("2", "RD", "Dublin", "Galway", "NH4", "AR4789")
query = "INSERT INTO route_details (routeId, source, destination) VALUES (%s, %s,%s)"
val = ("RD3", "Dublin", "Cork")
mycursor.execute(query, val)

mydb.commit()

number_of_rows = 0
mycursor.execute("SELECT * FROM route_details")

for x in mycursor:
  print(x)
  number_of_rows = number_of_rows + 1
print(number_of_rows, "record(s) inserted.")
