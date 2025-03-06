from keras._tf_keras.keras.models import load_model
import cv2
import numpy as np
from PIL import Image
import pickle
import os

BrainTumor_Model = ''
BrainTumor_Model = load_model('models/BrainTumor.h5')

# DeepLearning models

def get_classname(classNo):
    if (classNo==0):
        return "No Brain Tumor"
    elif classNo==1:
        return "Yes Brain Tumor"

def getResult(img):
    image = cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64,64))
    image = np.array(image)
    input_img = np.expand_dims(image, axis=0)
    result = BrainTumor_Model.predict(input_img)
    res = str(result)
    res = res.split('.')[0]
    result = res.split('[')[2]
    return int(result)

# print(getResult('C:\\Users\\Jai_Jayathillak\\PycharmProjects\\OpenCvLearn\\BrainTumor\\dataset1\\no\\no1.jpg'))