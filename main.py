import os
from flask import Flask, request, session, jsonify
from flask_session import Session
from from_root import from_root
from faceRecogniton.face import detect_face
from imageCapture.imageCapture import capture_image
from databaseConnector.database_connection import MysqlHelper
from utils.common_helper import unique_id_generator, make_user_folder
import re

mysql = MysqlHelper(host="127.0.0.1", password="Ramramsa@123", user="root")

app = Flask(__name__)


status = False

@app.route('/')
def index():
    if not session.get('name'):
        """Redirect to login page"""
        return "Ask user to login first"
    else:
        return "Move to Gate Asking Page"


@app.route('/device', methods=['GET', 'POST'])
def device_status():
    global status
    if request.method == 'GET':
        return status


@app.route('/registeration', methods=['GET', 'POST'])
def registeration():
    if request.method == 'GET':
        return jsonify('OK'), 200

    if request.method == 'POST':
        count = 0
        pid = request.form['pid']
        folder_status = make_user_folder(unique_id=pid, where='imageStore')
        if folder_status == "Folder Created":
            for imagefile in request.files.items():
                imagefile[1].save(os.path.join(from_root(), "imageStore", pid, str(count)+".jpg"))
                count += 1
            return jsonify({"Status": "Folder Created Images Stored"}), 200
        else:
            return jsonify({"Error": "Folder Already Present"}), 400


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return jsonify('OK'), 200
    if request.method == "POST":
        # Getting email and pass and checking
        userData = request.get_json()
        account = mysql.fetch_one(f"Select * from fia.details where email='{userData['email']}' and pass='{userData['pass']}';")
        if account:
            return jsonify({"status": "authorized", "PID": account[5]}), 200
        else:
            # Redirect to signup page
            return jsonify("Unauthorized"), 401


@app.route('/permission', methods=['GET', 'POST'])
def permission():
    if request.method == 'GET':
        return jsonify({"Status": "OK"}), 200
    else:
        if request.method == "POST":
            data = request.get_json()
            if data['gate'] == 'MainGate':
                query = f"update fia.details set mainGate = 1 where empid = '{data['pid']}';"
                value = mysql.update_record(query)
                if value:
                    return jsonify({"Status": "Permission Given"}), 200
                else:
                    return jsonify({"Status": "Permission denied"}), 101

            if data['gate'] == 'InnovationGate':
                query = f"update fia.details set innovationGate = 1 where empid = '{data['pid']}';"
                value = mysql.update_record(query)
                if value:
                    return jsonify({"Status": "Permission Given"}), 200
                else:
                    return jsonify({"Status": "Permission denied"}), 101


@app.route('/gateaccess/<gate>', methods=['GET', 'POST'])
def gate_access(gate=None):
    global status
    if request.method == 'GET':
        return jsonify({"Status": "OK"}), 200
    else:
        if request.method == "POST":
            if gate == "MainGate":
                pid = request.form['pid']
                query = f"select mainGate from fia.details where empid='{pid}';"
                value = mysql.fetch_one(query)
                if value[0]:
                    folder_status = make_user_folder(unique_id=pid, where='api')
                    imagefile = request.files['image_0']
                    imagefile.save(os.path.join(from_root(), "apiImage", pid, "user.jpg"))
                    apiImage_path = os.path.join(from_root(), "apiImage", pid, "user.jpg")
                    imageStore_path = os.path.join(from_root(), "imageStore", pid)
                    verified = detect_face(apiImage_path, imageStore_path, pid)
                    if verified['distance'] >= 70.0 and verified['verified'] > 3:
                        status = True
                        return jsonify({"Status": "Authorized"}), 200
                    else:
                        return jsonify({"Status": "Unauthorized"}), 401
                else:
                    return jsonify({"Status": "No Permission"}), 200

            elif gate == "InnovationLab":
                pid = request.form['pid']
                query = f"select innovationGate from fia.details where empid='{pid}';"
                value = mysql.fetch_one(query)
                if value[0]:
                    folder_status = make_user_folder(unique_id=pid, where='api')
                    imagefile = request.files['image_0']
                    imagefile.save(os.path.join(from_root(), "apiImage", pid, "user.jpg"))
                    apiImage_path = os.path.join(from_root(), "apiImage", pid, "user.jpg")
                    imageStore_path = os.path.join(from_root(), "imageStore", pid)
                    verified = detect_face(apiImage_path, imageStore_path, pid)
                    if verified['distance'] >= 70.0 and verified['verified'] > 3:
                        status = True
                        return jsonify({"Status": "Authorized"}), 200
                    else:
                        return jsonify({"Status": "Unauthorized"}), 401
                else:
                    return jsonify({"Status": "No Permission"}), 200

            else:
                return jsonify({"Status": "WRONG GATE"}), 401


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = None
    if request.method == "GET":
        # name ,email, password, confirm pass
        return "Render signup page"

    elif request.method == "POST":
        userData = request.get_json()
        username = userData['name']
        email = userData['email']
        password = userData['password']
        phone_number = userData['phonenumber']
        confirm_password = userData['confirm_password']
        account = mysql.fetch_one(f"select * from fia.details where email='{email}'")
        if account:
            return jsonify("Account already exists"), 409
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        elif confirm_password != password:
            msg = 'Password and Confirm password are not same!'
        elif not re.match(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', phone_number):
            msg = 'wrong phone number !'
        else:
            uniqueID = str(unique_id_generator())
            query = f"Insert Into fia.details (name,email,pass,phoneNumber, empid, mainGate, innovationGate) values('{username}','{email}','{password}','{phone_number}','{uniqueID}','{0}','{0}');"
            inserted = mysql.insert_record(query)
            if inserted:
                return jsonify({"status": "Account Created", "PID": str(uniqueID)}), 201
            else:
                return jsonify("Please Enter correctly"), 420

        return jsonify({"Error": msg}), 420
    else:
        return jsonify({"Error": "Unimplemented Methods"}), 404


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('name', None)
    session.pop('pid', None)
    session.pop('email', None)
    return "Logout Successful"


if __name__ == "__main__":
    # main()
    app.run(debug=True, port=8080)
