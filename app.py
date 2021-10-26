import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ocr_core import ocr_core
from blur import test_blurry

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

        if 'file' not in request.files:
            return jsonify(message="No file selected")
        file = request.files['file']
        if file.filename == '':
            return jsonify(success=False, message="No file selected")

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            # call the OCR function on it
            check_blur = test_blurry("static/uploads/" + file.filename)
            if (check_blur['fm'] > 5000):
                return jsonify(
                    success=False,
                    message=
                    "Image too blurred, click a better image for accurate results",
                    blur=check_blur)
            extracted_text = ocr_core(file)
            response = jsonify(
                success=True,
                response=extracted_text,
                link="https://extract-text-image.herokuapp.com/static/uploads/"
                + file.filename)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            return jsonify(success=False,
                           message="Only jpg, jpeg, png and gif files allowed")

    elif request.method == 'GET':
        return jsonify(success=False, message="Cannot GET")


if __name__ == '__main__':
    app.debug = True
    app.run()
