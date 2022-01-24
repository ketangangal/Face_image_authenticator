import os
from flask import Flask, request, session
from from_root import from_root
from faceRecogniton.face import detect_face
from imageCapture.imageCapture import capture_image
from databaseConnector.database_connection import MysqlHelper


mysql = MysqlHelper(host="127.0.0.1", password="test@123", user="root")

app = Flask(__name__)


@app.route('/getimage', methods=['GET', 'POST'])
def getImageFromUser():
    if request.method == 'GET':
        return "OK", 200

    if request.method == 'POST':
        gateNumber = request.form['gateNumber']
        imagefile = request.files['image']
        imagefile.save(os.path.join(from_root(), "apiImage/api.jpg"))
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


@app.route('/login', methods=['GET','POST'])
def login():
    session = {}
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        account = mysql.fetch_one(f"Select * from fia.details where email={email} and password={password}")
        if account:
            session['pid'] = account[0]
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

# @app.route('/logout', methods=['POST'])
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     session.pop('pid', None)
#     session.pop('project_name', None)
#     session.pop('project_type', None)
#     session.pop('target_column', None)
#     logger.info('Thanks For Using System!')
#     return redirect(url_for('contact'))

# Normalize the image and convert it greyscale
# def main():
#     apiImage_path = os.path.join(from_root(), "apiImage", 'api.jpg')
#     imageStore_path = os.path.join(from_root(), "imageStore")
#
#     # status, msg = capture_image(imageStore_path, 5)
#     # if status:
#     #     result = detect_face(apiImage_path, imageStore_path)
#     #     print(result)


if __name__ == "__main__":
    # main()
    app.run(debug=False, port=8080)
