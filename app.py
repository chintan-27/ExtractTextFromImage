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
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        print(file)
        print(file.filename)
        
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print(file)
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            # call the OCR function on it
            extracted_text = ocr_core(file)
            response = jsonify(text = extracted_text)
            response.headers.add("Access-Control-Allow-Origin", "*")

            # extract the text and display it
            # return render_template('upload.html',
            #                        msg='Successfully processed',
            #                        extracted_text=extracted_text,
            #                        img_src=UPLOAD_FOLDER + file.filename)
            return response
        
    # elif request.method == 'GET':
    #     return render_template('upload.html')

if __name__ == '__main__':
    app.debug=True
    app.run('127.0.0.1',port=4444)
