from keras._tf_keras.keras.models import load_model
import cv2
import numpy as np
from PIL import Image
import os

Alzemeir_Model = ''
Alzemeir_Model = load_model('models/Alzeimer_model.h5')

def get_classname1(classNo):
    if (classNo==0):
        return "No Alzemeir Disease"
    elif classNo==1:
        return "Yes Alzemeir Disease"

def alzeimerckh(img):
    image = cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64,64))
    image = np.array(image)
    input_img = np.expand_dims(image, axis=0)
    result = Alzemeir_Model.predict(input_img)
    res = str(result)
    res = res.split('.')[0]
    result = res.split('[')[2]
    return int(result)