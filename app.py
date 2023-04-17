from flask import Flask, redirect, request, render_template, send_from_directory
import os
from PIL import Image, ImageFilter
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def choose_mode():
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'upload':
            return redirect('/upload')
        elif mode == 'download':
            return redirect('/download')
    return render_template('choose_mode.html')
# ----------------------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file.save('uploads/' + filename)
        image = Image.open('uploads/' + filename)
        # Appliquer un filtre à l'image
        filtered_image = image.filter(ImageFilter.SHARPEN)
        # Enregistrer l'image filtrée
        filtered_filename = 'filtered_' + filename
        filtered_image.save('uploads/' + filtered_filename)
        return render_template('result.html', original_filename=filename, filtered_filename=filtered_filename)
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/download', methods=['GET', 'POST'])
def download_image():
    if request.method == 'POST':
        url = request.form['url']
        response = requests.get(url)
        filename = 'downloaded_image.jpg'
        with open(os.path.join('uploads', filename), 'wb') as f:
            f.write(response.content)
        return render_template('downloaded.html', filename=filename)
    return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=True)
