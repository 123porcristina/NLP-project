import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
from NLP_package.dashboard import app


UPLOAD_FOLDER = '../uploads/'
STATIC_FOLDER = './static/'
PREPROCESSED_FOLDER = '/processed_files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'csv'}

app.server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_processed_files():
    file_array = []
    for file in os.listdir(f'./{PREPROCESSED_FOLDER}/'):
        file_object = {
            "name": file,
            "href": f'/file?filename={file}' 
        }
        file_array.append(file_object)
    return file_array

@app.server.route('/dashboard')
def dashboard():
    return app.index()

@app.server.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.server.config['UPLOAD_FOLDER'], filename))
            return render_template('home.html', filename=filename, files=get_processed_files())
    return render_template('home.html', files=get_processed_files())

@app.server.route('/file', methods=['GET'])
def return_requested_file():
    print("[INFO] Download File Requested", request)
    # try:
    #     if request.args['filename']:
    #         filename = request.args['filename']
    #         print(f'../{PREPROCESSED_FOLDER}/{filename}')
    #         return send_from_directory(f'../uploads/df_tokens.pickle', )
    # except Exception as e:
    #     return str(e)
    return send_from_directory(UPLOAD_FOLDER, 'df_tokens.csv', as_attachment=True )

@app.server.route('/topic-graphic')
def return_topic_graphic():
    return render_template('ida.html')

