import redis
import IdentityService as identity
from datetime import timedelta
import mysql.connector
import DatabaseConnector as db

mydb = db.get_Connection()
r = redis.Redis(host='redis', port=6379, db=0)

mycursor = mydb.cursor()

def get_token(userId):
    query = "select user_token from USER_PROFILE where owner_unique_Id LIKE '{}'".format(userId)
    mycursor.execute(query)
    saved_token = None
    for x in mycursor:
        for _x in x:
            saved_token = _x
            # print("token: ", saved_token)
    return saved_token

def check_cache_user_token(userId):
    value = r.get(userId)
    # print("Found cached User_token")
    if value is None:
        token = get_token(userId)
        r.setex(userId, timedelta(minutes=30),value=token)
        value = token
        # print("User_token cached")
    else:
        value = value.decode("utf-8")
    return value