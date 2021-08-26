import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ocr_core import ocr_core

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        print(request.data)
        print(request.json)
        print(request.get_data())
        print(request.get_data())
        print(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(message="No file selected")
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify(message="No file selected")

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            # call the OCR function on it
            extracted_text = ocr_core(file)
            response = jsonify(message="Successful", text=extracted_text)
            response.headers.add("Access-Control-Allow-Origin", "*")

            # extract the text and display it
            # return render_template('upload.html',
            #                        msg='Successfully processed',
            #                        extracted_text=extracted_text,
            #                        img_src=UPLOAD_FOLDER + file.filename)
            return response
        else:
            return jsonify(message="Only jpg, jpeg, png and gif files allowed")

    elif request.method == 'GET':
        return jsonify(message="Cannot GET")


if __name__ == '__main__':
    app.debug = True
    app.run()
