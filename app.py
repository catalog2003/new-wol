import os
from flask import Flask, request, render_template
import pytesseract
import easyocr
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure Tesseract is installed
if os.system('which tesseract') != 0:
    raise EnvironmentError('Tesseract is not installed.')

# Define the Tesseract and EasyOCR functions
def ocr_with_tesseract(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return pytesseract.image_to_string(thresh)

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

            # Process the file with Tesseract or EasyOCR
            text_type = request.form.get("text_type")
            if text_type == "printed":
                result_text = ocr_with_tesseract(filepath)
            else:
                result_text = ocr_with_easyocr(filepath)

            return f"<h1>Extracted Text:</h1><pre>{result_text}</pre>"
    return '''
        <form method="POST" enctype="multipart/form-data">
            <label>Upload Image: <input type="file" name="file" /></label><br/>
            <label>Choose Text Type: </label>
            <select name="text_type">
                <option value="printed">Printed</option>
                <option value="handwritten">Handwritten</option>
            </select><br/>
            <button type="submit">Submit</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
