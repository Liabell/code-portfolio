from flask import Flask, request, render_template, send_from_directory
from PIL import Image
from pixelsort import pixelsort
import os
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = f"{int(time.time())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get parameters from the form
        interval_function = request.form.get('interval_function', 'threshold')
        randomness = float(request.form.get('randomness', 0))
        lower_threshold = float(request.form.get('lower_threshold', 0.25))
        upper_threshold = float(request.form.get('upper_threshold', 0.8))
        angle = int(request.form.get('angle', 0))
        sorting_function = request.form.get('sorting_function', 'lightness')
        external_interval_file = request.files['external_interval_file'] if 'external_interval_file' in request.files else None
        mask = request.files['mask'] if 'mask' in request.files else None

        # Apply all functions separately if checkbox is checked and at least one required file is uploaded
        all_functions = request.form.get('all_functions') == 'on'
        sorted_files = []
        if all_functions:
            functions_to_apply = ['random', 'edges', 'threshold', 'waves', 'none']
            if external_interval_file:
                functions_to_apply += ['file']
            if mask:
                functions_to_apply += ['file-edges']
            
            for func in functions_to_apply:
                sorted_img = apply_function(
                    filepath,
                    func,
                    randomness,
                    lower_threshold,
                    upper_threshold,
                    angle,
                    sorting_function,
                    external_interval_file,
                    mask
                )
                sorted_filename = f"sorted_{func}_{filename}"
                sorted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], sorted_filename)
                sorted_img.save(sorted_filepath, format='PNG')
                sorted_files.append(sorted_filename)

            return render_template('result_all_functions.html', original=filename, sorted_files=sorted_files)
        else:
            sorted_img = apply_function(
                filepath,
                interval_function,
                randomness,
                lower_threshold,
                upper_threshold,
                angle,
                sorting_function,
                external_interval_file,
                mask
            )

            sorted_filename = f"sorted_{interval_function}_{filename}"
            sorted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], sorted_filename)
            sorted_img.save(sorted_filepath, format='PNG')

            return render_template('result.html', original=filename, sorted=sorted_filename)

def apply_function(filepath, interval_function, randomness, lower_threshold, upper_threshold, angle, sorting_function, external_interval_file, mask):
    img = Image.open(filepath)
    sorted_img = pixelsort(
        img,
        interval_function=interval_function,
        randomness=randomness,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        angle=angle,
        sorting_function=sorting_function,
        interval_image=external_interval_file,
        mask_image=mask
    )
    return sorted_img

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
