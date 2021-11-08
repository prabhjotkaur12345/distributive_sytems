from flask import Flask
from flask import jsonify
from flask import request
import Minion as minion
import IdentityService as identity
import json
import Constants as constants
import py_eureka_client.eureka_client as eureka_client


app = Flask(__name__)
your_rest_server_port = 5000
# The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
eureka_client.init(eureka_server="http://eurekaService:8761/",
                   app_name="flask-app",
                   instance_port=your_rest_server_port)

@app.route('/route_list',methods=['POST'])
def route_list():

    client_json = request.get_json(force=True)

    user = client_json['user']
    token = client_json['token']
    source = client_json['source']
    destination = client_json['destination']

    route_list = minion.get_route_list(user, token, source, destination)
    if route_list == constants.Error_Code_403:
        return jsonify(
            errorMessage=constants.Error_Code_403
    ), 403
    else:
        return jsonify(
                route_list=route_list
        ), 200

@app.route('/register',methods=['POST'])
def register():
    print("goddddd")

    client_json = request.get_json(force=True)

    userId = client_json['user']

    user_token = identity.register_user(userId)
    if user_token is None:
        return jsonify(
            status="Registration Not Successful, username not available"
    )  
    else:
        return jsonify(
            status="Registration Successful",
            userToken = user_token
    )

@app.route('/route_avail', methods=['POST'])
def route_avail():

    client_json = request.get_json(force=True)

    route_id = client_json['route']
    timeslot = client_json['timeslot']
    date_requested = client_json['date']
    user = client_json['user']
    token = client_json['token']
    source = client_json['source']
    destination = client_json['destination']
    vehicle_number = client_json['vehicle_number']
    
    route_avail = minion.update_route_info(user, token, source, destination, vehicle_number, timeslot, route_id, date_requested)
    res = jsonify(
        passcode=route_avail
    )
    if route_avail == constants.Error_Code_403:
        return jsonify(
            errorMessage=constants.Error_Code_403
    ), 403
    else:
        return res, 200

@app.route('/health')
def healthcheck():
    print("hellooooo")
    return "hello world"
    with app.app_context():
        print("All is well in port 8080")
        return jsonify(
            status="running"
        )


if __name__ == '__main__':
    db_setup = False
    while not db_setup:
        db_setup = identity.create_databases()
        if db_setup:
            db_setup = identity.create_tables()
            db_setup=True
            
    app.run('0.0.0.0',debug=True)
    