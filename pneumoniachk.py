import cv2
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing import image
import numpy as np
from PIL import Image

Pneumonia_Model = ''
Pneumonia_Model = load_model('./models/pneumonia_model.h5')

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict_image(img_path):
    processed_image = preprocess_image(img_path)
    prediction = Pneumonia_Model.predict(processed_image)
    print(prediction)
    if prediction[0][0] > 0.5:
        return ("The person has Pneumonia")
    else:
        return ("The person did not have Pneumonia")