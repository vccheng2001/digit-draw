import flask
import pickle
import base64
import numpy as np
import cv2
import torch
import torchvision
import replicate
import json 
from pathlib import Path

from flask import (
    Flask,
    jsonify,
    render_template,
    send_from_directory,
    request,
)


# Initialize the useless part of the base64 encoded image.
init_Base64 = 21

# Initializing new Flask instance. Find the html template in "templates".
app = flask.Flask(__name__, template_folder='templates')

# First route : Render the initial drawing template


@app.route('/')
def home():
    return render_template('draw.html')
    
from PIL import Image
import cv2
import io
import matplotlib.pyplot as plt
def string_to_img(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    img = np.array(Image.open(io.BytesIO(imgdata)))
    resized = cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)
    img = np.asarray(resized, dtype="uint8")
    img = 255-img
    return img

# Second route : Use our model to make prediction - render the results page.
@app.route('/api/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        draw = request.form['url']
        # Removing the useless part of the url.
        draw = draw[init_Base64:]
        # Decoding
        img = string_to_img(draw)
       
        image_path = 'image.jpg'
        cv2.imwrite(image_path, img)

        model = replicate.models.get("vganapati/mnist-classification")
        version = model.versions.get(
            "f3d94d920835d9ae085f0f0eb2ed8ff9f9771554e382af11e83cd79f1a646cb7"
        )
        prediction = replicate.predictions.create(
            version=version,
            input={
                "input":Path(image_path)
            },
        )

        prediction = replicate.predictions.get(prediction.id)
        output = None
        if prediction.output:
            output = prediction.output[0]['text']


    return render_template('results.html', prediction=output)


if __name__ == '__main__':
    app.run(debug=True)
