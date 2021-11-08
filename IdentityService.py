import mysql.connector
import uuid
import redis_connector as cache
import DatabaseConnector as db

def authenticate_user(userId, token):
    saved_token = cache.check_cache_user_token(userId)
    
    token_Matched = False
    if token == saved_token:
        token_Matched = True
    print("status: ", token_Matched)
    return token_Matched

def register_user(userId):
    
    mydb = db.get_Connection()

    mycursor = mydb.cursor()

    user_token = str(uuid.uuid4())
    query = "INSERT INTO USER_PROFILE (owner_unique_Id, user_token) VALUES (%s, %s)"
    val = (userId, user_token)
    try:
        mycursor.execute(query, val)
        mydb.commit()
        print("user_token is: ", user_token)
    except Exception as e:
        user_token = None
        print(e)
        pass
    return user_token

def create_databases():
    try:
        mydb = db.get_Connection()
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS bdteste")                    
    except Exception as e:
        print(e)
        return False
    return True
    
def create_tables():
    try:
        mydb = db.get_Connection()
        mycursor = mydb.cursor()
        
        mycursor.execute("CREATE TABLE IF NOT EXISTS TRIP_DETAILS (tripId VARCHAR(255) PRIMARY KEY, owner_unique_Id VARCHAR(255), source VARCHAR(255), destination VARCHAR(255), route_taken VARCHAR(255), vehicle_number VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        mycursor.execute("CREATE TABLE IF NOT EXISTS ROUTE_DETAILS (routeId VARCHAR(255) PRIMARY KEY, source VARCHAR(255), destination VARCHAR(255))")
        mycursor.execute("CREATE TABLE IF NOT EXISTS BOOKINGS_AVAIL(timeslot INT, route_id VARCHAR(255), count INT CHECK (count BETWEEN 1 and 49), date_requested DATE)")
        mycursor.execute("CREATE TABLE IF NOT EXISTS USER_PROFILE(owner_unique_Id VARCHAR(255) PRIMARY KEY, user_token VARCHAR(255))")
        query = "INSERT INTO ROUTE_DETAILS (routeId, source, destination) VALUES (%s, %s,%s)"
        val = ("RD3", "Dublin", "Cork")
 
        mycursor.execute(query, val)
        mydb.commit()
    except Exception as e:
        print(e)
        return False
    return True
    
# def main():
# #   register_user("Rupasmita1")
#   user_token = "4a265670-c0e5-4e95-8e2b-b3eb2ec9c3a4"
#   authenticate_user("Rupasmita123",user_token)

# if __name__ == "__main__":
#     main()

