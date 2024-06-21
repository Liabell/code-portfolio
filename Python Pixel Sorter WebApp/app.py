import numpy as np
from moviepy.editor import VideoFileClip, ImageSequenceClip
from PIL import Image
from flask import Flask, request, render_template, send_from_directory
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
def upload_media():
    if 'file' not in request.files and 'video' not in request.files:
        return 'No file part'
    
    file = request.files['file'] if 'file' in request.files else None
    video = request.files['video'] if 'video' in request.files else None

    if file and file.filename == '' and not video:
        return 'No selected file'
    if video and video.filename == '' and not file:
        return 'No selected file'

    filename = f"{int(time.time())}_{file.filename if file else video.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if file:
        file.save(filepath)
    else:
        video.save(filepath)

    # Get parameters from the form
    interval_function = request.form.get('interval_function', 'threshold')
    randomness = float(request.form.get('randomness', 0))
    lower_threshold = float(request.form.get('lower_threshold', 0.25))
    upper_threshold = float(request.form.get('upper_threshold', 0.8))
    angle = int(request.form.get('angle', 0))
    sorting_function = request.form.get('sorting_function', 'lightness')
    external_interval_file = request.files['external_interval_file'] if 'external_interval_file' in request.files else None
    mask = request.files['mask'] if 'mask' in request.files else None

    all_functions = request.form.get('all_functions') == 'on'

    if file:
        return process_image(filepath, interval_function, randomness, lower_threshold, upper_threshold, angle, sorting_function, external_interval_file, mask, all_functions)
    else:
        return process_video(filepath, interval_function, randomness, lower_threshold, upper_threshold, angle, sorting_function, external_interval_file, mask, all_functions)

def process_image(filepath, interval_function, randomness, lower_threshold, upper_threshold, angle, sorting_function, external_interval_file, mask, all_functions):
    sorted_files = []

    if all_functions:
        functions_to_apply = ['random', 'edges', 'threshold', 'waves', 'none']
        if external_interval_file:
            functions_to_apply.append('file')
        if mask:
            functions_to_apply.append('file-edges')

        function_set_length = len(functions_to_apply)
        i=1
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
            sorted_filename = f"sorted_{func}_{os.path.basename(filepath)}"
            sorted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], sorted_filename)
            sorted_img.save(sorted_filepath, format='PNG')
            sorted_files.append(sorted_filename)
            print(f'Functions applied: {i} of {function_set_length}')
            i = i + 1

        return render_template('result_all_functions.html', original=os.path.basename(filepath), sorted_files=sorted_files)
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
        sorted_filename = f"sorted_{interval_function}_{os.path.basename(filepath)}"
        sorted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], sorted_filename)
        sorted_img.save(sorted_filepath, format='PNG')

        return render_template('result.html', original=os.path.basename(filepath), sorted=sorted_filename)

def process_video(filepath, interval_function, randomness, lower_threshold, upper_threshold, angle, sorting_function, external_interval_file, mask, all_functions):
    clip = VideoFileClip(filepath)
    frames = [Image.fromarray(frame) for frame in clip.iter_frames()]
    total_frames = len(frames)
    
    sorted_frames = []
    for idx, frame in enumerate(frames):
        # Display progress
        print(f"Processing frame {idx + 1} of {total_frames} {int((idx/total_frames)*100)}%")
        
        sorted_frame = pixelsort(
            frame,
            interval_function=interval_function,
            randomness=randomness,
            lower_threshold=lower_threshold,
            upper_threshold=upper_threshold,
            angle=angle,
            sorting_function=sorting_function,
            interval_image=external_interval_file,
            mask_image=mask
        )
        sorted_frames.append(np.array(sorted_frame))
    
    sorted_clip = ImageSequenceClip(sorted_frames, fps=clip.fps)
    sorted_filename = f"sorted_{interval_function}_{os.path.basename(filepath)}"
    sorted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], sorted_filename)
    sorted_clip.write_videofile(sorted_filepath, codec='libx264')
    
    return render_template('result_video.html', original=os.path.basename(filepath), sorted=sorted_filename)

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
    app.run(host='0.0.0.0', port=5000, debug=True)