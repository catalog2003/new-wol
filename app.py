import os
from flask import Flask, request, render_template
import easyocr
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the EasyOCR function
def ocr_with_easyocr(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    return "\n".join([detection[1] for detection in result])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get uploaded file
        file = request.files["file"]
        if file:
            filepath = os.path.join("static", secure_filename(file.filename))
            file.save(filepath)

            # Process the file with EasyOCR
            result_text = ocr_with_easyocr(filepath)

            return f"<h1>Extracted Text:</h1><pre>{result_text}</pre>"
    return '''
        <form method="POST" enctype="multipart/form-data">
            <label>Upload Image: <input type="file" name="file" /></label><br/>
            <button type="submit">Submit</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
