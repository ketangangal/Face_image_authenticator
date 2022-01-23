import os
from flask import Flask, request
from from_root import from_root
from faceRecogniton.face import detect_face
from imageCapture.imageCapture import capture_image

app = Flask(__name__)


@app.route('/getimage', methods=['GET', 'POST'])
def getImageFromUser():
    if request.method == 'GET':
        return "Hello World"

    if request.method == 'POST':
        data = request.form['metadata']
        print(data)
        imagefile = request.files['image']
        imagefile.save(os.path.join(from_root(), "apiImage/api.jpg"))
        return "OK", 200

@app.route('/deviceoff', methods=['GET', 'POST'])
def deviceoff():
    if request.method == 'GET':
        return 'False'

@app.route('/deviceon', methods=['GET', 'POST'])
def deviceon():
    if request.method == 'GET':
        return 'True'



@app.route('/getimage', methods=['GET', 'POST'])
def registeration():
    if request.method == 'GET':
        pass
    if request.method == "POST":
        pass


@app.route('/authenticated', methods=['GET', 'POST'])
def authenticated():
    pass

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
