from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/generate-trees', methods=['POST'])
def generate_trees():
    data = request.json
    if not data or 'image' not in data:
        app.logger.error('No image provided in request')
        return jsonify({'error': 'No image provided'}), 400
    
    image_data = data['image']
    app.logger.info('Received image data')

    # Decode the image
    try:
        image_data = image_data.split(',')[1]
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        app.logger.info('Image decoded successfully')
    except Exception as e:
        app.logger.error('Error decoding image: %s', e)
        return jsonify({'error': 'Error decoding image'}), 500

    # Placeholder: Process the image and generate trees
    try:
        # Perform image processing here to generate trees
        result_image = image  # This should be the processed image with trees
        app.logger.info('Image processing completed')
    except Exception as e:
        app.logger.error('Error processing image: %s', e)
        return jsonify({'error': 'Error processing image'}), 500

    # Encode the result image to base64
    try:
        _, buffer = cv2.imencode('.png', result_image)
        result_image_base64 = base64.b64encode(buffer).decode('utf-8')
        app.logger.info('Image encoded successfully')
    except Exception as e:
        app.logger.error('Error encoding image: %s', e)
        return jsonify({'error': 'Error encoding image'}), 500

    return jsonify({'result': 'data:image/png;base64,' + result_image_base64})

if __name__ == '__main__':
    app.run(debug=True)