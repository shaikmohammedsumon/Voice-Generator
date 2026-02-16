import os
from flask import Flask, render_template, request, send_file
from moviepy.editor import ImageClip, concatenate_videoclips

UPLOAD_FOLDER = "uploads"
VIDEO_FILE = "output.mp4"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Clear previous uploads
        for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        
        files = request.files.getlist("images")
        image_files = []

        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            image_files.append(file_path)

        # Create video
        clips = [ImageClip(img).set_duration(2) for img in image_files]
        video = concatenate_videoclips(clips, method="compose")
        video.write_videofile(VIDEO_FILE, fps=24)

        return send_file(VIDEO_FILE, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
