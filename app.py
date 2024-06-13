from flask import Flask, render_template, request, send_file, redirect, url_for
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    try:
        input_image = Image.open(io.BytesIO(file.read()))
        output_image = remove(input_image)

        output_io = io.BytesIO()
        output_image.save(output_io, format='PNG')
        output_io.seek(0)

        return send_file(output_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
