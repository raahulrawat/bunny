from flask import Flask, render_template, request, redirect, url_for, flash
import os
from transform import Trans
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "static/upload"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

transfer = Trans()


@app.route("/")
def home():
    return render_template("selection.html")

@app.route("/main", methods=['GET'])
def he():
    return render_template("selection.html")

# processing uploaded image to create art..
@app.route("/download", methods=['GET', 'POST'])
def hoe():
    if request.method == 'POST':
        image = os.listdir("static/upload/")[0]
        imPath = "static/upload/"+image
        model = request.form.get('check')
        mPath = "static/models/"+model
        try:
            os.remove("static/output/processed.png")
        except:
            pass
        transfer.bunny(model=mPath, image=imPath)
        os.remove(imPath)
        return render_template("download.html")


# validation function for not accepting other than images documents...
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
