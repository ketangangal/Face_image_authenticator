import os
from flask import Flask, request, session
from flask_session import Session
from from_root import from_root
from faceRecogniton.face import detect_face
from imageCapture.imageCapture import capture_image
from databaseConnector.database_connection import MysqlHelper
from utils.common_helper import unique_id_generator
import re

mysql = MysqlHelper(host="127.0.0.1", password="@123", user="root")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/getimage', methods=['GET', 'POST'])
def getImageFromUser():
    if request.method == 'GET':
        return "OK", 200

    if request.method == 'POST':
        gateNumber = request.form['gateNumber']
        imagefile = request.files['image']
        imagefile.save(os.path.join(from_root(), "apiImage/1234/api.jpg"))
        return "OK", 200


status = False
def set_status(verified):
    global status
    if verified is True:
        status = True
    else:
        status = False


@app.route('/device', methods=['GET', 'POST'])
def device_status():
    global status
    if request.method == 'GET':
        return status


@app.route('/registeration', methods=['GET', 'POST'])
def registeration():
    if request.method == 'GET':
        return "OK", 200

    if request.method == 'POST':
        count = 0
        gatenumber = request.form['metadata']
        for imagefile in request.files.items():
            imagefile[1].save(os.path.join(from_root(), "imageStore", str(gatenumber)+ str(count)+".jpg"))
            count += 1
        return "OK", 200


@app.route('/authenticated', methods=['GET', 'POST'])
def authenticated():
    pass


@app.route('/')
def index():
    if not session.get('name'):
        """Redirect to login page"""
        return "Ask user to login first"
    else:
        return "Move to Gate Asking Page"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return 'OK', 200
    if request.method == "POST":
        # Getting email and pass and checking
        userData = request.get_json()
        account = mysql.fetch_one(f"Select * from fia.details where email='{userData['email']}' and pass='{userData['pass']}';")
        if account:
            session['name'] = account[1]
            session['email'] = account[2]
            session['pid'] = account[5]
            # Redirect to gate page
            return "Logged in", 200
        else:
            # Redirect to signup page
            return "No Content ", 204


@app.route('/gateaccess/<gate>', methods=['GET', 'POST'])
def gate_access(gate=None):
    global status
    if not session.get('pid'):
        return "Login first"
    else:
        if request.method == "POST":
            if gate == "MainGate":
                query = f"select mainGate from fia.details where empid='{session['pid']}';"
                value = mysql.fetch_one(query)
                if value:
                    # Open camera
                    # click photo
                    # store that in apiimage folder
                    apiImage_path = os.path.join(from_root(), "apiImage", str(session['pid']), "api.jpg")
                    imageStore_path = os.path.join(from_root(), "imageStore", str(session['pid']))
                    verified = detect_face(apiImage_path, imageStore_path)
                    if verified['distance'] >= 70.0 and verified['verified'] > 3:
                        status = True
                        # return "user not verified"
                        return "Access granted"
                else:
                    return "No value in database"

            elif gate == "InnovationLab":
                query = f"select innovationGate from fia.details where empid='{session['pid']}';"
                value = mysql.fetch_one(query)
                if value:
                    # Open camera
                    # click photo
                    # store that in apiimage folder
                    apiImage_path = os.path.join(from_root(), "apiImage", str(session['pid']), "api.jpg")
                    imageStore_path = os.path.join(from_root(), "imageStore", str(session['pid']))
                    verified = detect_face(apiImage_path, imageStore_path)
                    if verified['distance'] >= 70.0 and verified['verified'] > 3:
                        status = True
                        # return "user not verified"
                        return "Access granted"
                else:
                    return "No value in database"

            else:
                return "Wrong gate"
        else:
            return "NO CONTENT", 204


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
        account = mysql.fetch_one(f"select * from fia.details where email={email}")

        if account:
            return "Account already exists"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        elif confirm_password != password:
            msg = 'Password and Confirm password are not same!'
        elif not re.match(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',phone_number):
            msg = 'wrong phone number !'
        else:
            uniqueID = str(unique_id_generator())
            query = f"Insert Into fia.details (name,email,pass,phoneNumber, empid, mainGate, innovationGate) values({username},{email},{password},{phone_number},{uniqueID},{0},{0})"
            inserted = mysql.insert_record(query)
            if inserted:
                return "Successful redirect to login"
            else:
                return "Error while updating"

    else:
        pass





# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if 'loggedin' in session:
#         return redirect(url_for('index'))
#     else:
#         if request.method == "GET":
#             logger.info('Signup Template Rendering')
#             return render_template('signup.html')
#         else:
#             msg = None
#             if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#                 username = request.form['username']
#                 password = request.form['password']
#                 confirm_password = request.form['confirm-password']
#                 email = request.form['email']
#                 account = mysql.fetch_one(f'SELECT * FROM tblUsers WHERE Email = "{email}"')
#                 logger.info('Checking Database')
#                 if account:
#                     msg = 'EmailId already exists !'
#                 elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#                     msg = 'Invalid email address !'
#                 elif not re.match(r'[A-Za-z0-9]+', username):
#                     msg = 'Username must contain only characters and numbers !'
#                 elif not username or not password or not email:
#                     msg = 'Please fill out the form !'
#                 elif confirm_password != password:
#                     msg = 'Password and Confirm password are not same!'
#                 else:
#                     hashed_password = Hashing.hash_value(password)
#                     rowcount = mysql.insert_record(
#                         f'INSERT INTO tblUsers (Name, Email, Password, AuthToken) VALUES ("{username}", "{email}", "{hashed_password}", "pankajtest")')
#                     if rowcount > 0:
#                         return redirect(url_for('login'))
#             elif request.method == 'POST':
#                 msg = 'Please fill out the form !'
#                 logger.error(msg)
#             logger.info(msg)
#             return render_template('signup.html', msg=msg)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('name', None)
    session.pop('pid', None)
    session.pop('email', None)
    return "Logout Successful"

# Normalize the image and convert it greyscale
# def main():
#     apiImage_path = os.path.join(from_root(), "apiImage", '0.jpg')
#     imageStore_path = os.path.join(from_root(), "imageStore")
#
#     # status, msg = capture_image(imageStore_path, 5)
#     # if status:
#     #     result = detect_face(apiImage_path, imageStore_path)
#     #     print(result)


if __name__ == "__main__":
    # main()
    app.run(debug=True, port=8080)
