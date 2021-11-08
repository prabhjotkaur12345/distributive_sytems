'''
This script -
checks no. of rows in a window of time for the combination of source, destination, route_taken
'''
import uuid
import IdentityService as identity
import Constants as constants
import DatabaseConnector as db

mydb = db.get_Connection()
mycursor = mydb.cursor()

def get_route_list(userId, token, s, d):
  status = identity.authenticate_user(userId, token)
  if status:
    query = "select routeId from ROUTE_DETAILS where source LIKE '{}' and destination LIKE '{}'".format(s, d)
    mycursor.execute(query)
    number_of_rows = 0
    route_list = []
    for x in mycursor:
      for _x in x:
        route_list.append(_x)
        break
      number_of_rows = number_of_rows + 1
    print(number_of_rows, "routes found.")
    return route_list
  else:
    return constants.Error_Code_403

def update_route_info(userId, token, s, d, vehicle_number, timeslot, route_id, date_requested):
  status = identity.authenticate_user(userId, token)
  if status:
    query = "select count from BOOKINGS_AVAIL where timeslot = {} and route_id LIKE '{}' and date_requested LIKE '{}'".format(timeslot,route_id,date_requested)
    mycursor.execute(query)
    print(query)
    count = None
    route_avail = False
    for x in mycursor:
      for _x in x:
        count = _x

    if count and count < 50:
      route_avail = True
      try:
        query = "update BOOKINGS_AVAIL set count = count + 1 where timeslot = {} and route_id = '{}' and date_requested = '{}'".format(timeslot,route_id,date_requested)
        mycursor.execute(query)
        mydb.commit()
      except Exception as e:
        route_avail = False
        print(e)
        pass

    
    if not count:
      route_avail = True
      query = "INSERT INTO BOOKINGS_AVAIL (timeslot,route_id,count,date_requested) VALUES (%s, %s,%s,%s)"
      val = (timeslot, route_id, 1, date_requested)
      mycursor.execute(query,val)
      mydb.commit()
      
    if route_avail:
      passIssue = str(uuid.uuid4())
      # Insert into the trip_details table
      insert_trip_details(passIssue, userId, s, d, route_id, vehicle_number)
    else:
      passIssue = "Route not available"

    return passIssue
  else:
    return constants.Error_Code_403


def insert_trip_details(tripId ,owner_unique_Id, source, destination, route_taken, vehicle_number):
    query = "INSERT INTO TRIP_DETAILS (tripId ,owner_unique_Id, source, destination, route_taken, vehicle_number) VALUES (%s, %s,%s, %s,%s, %s)"
    val = (tripId ,owner_unique_Id, source, destination, route_taken, vehicle_number)
    mycursor.execute(query, val)
    mydb.commit()

# def main():
#   print(get_route_list("Dublin", "Galway"))

# if __name__ == "__main__":
#     main()
