from keras._tf_keras.keras.models import load_model
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import os
from braintumorchk import getResult
from alzemirchk import alzeimerckh
from pneumoniachk import predict_image
from sndemail import send_email, sends_email

Diabetes_Model = ''

with open('models/diabetes_model.sav', 'rb') as f:
    Diabetes_Model = pickle.load(f)

# sidebar for navigation menu

with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Brain Tumor', 
                            'Alzemeir Disease', 'Diabetes Detection', 
                            'Pneumonia Detection'],
                           icons=['activity', 'lungs', 'hospital', 'bandaid'],
                           default_index=0)

# BrainTumor detection page
if (selected == 'Brain Tumor'):
    st.title('Brain Tumor detection using ML from MRI image')
    
    Patient_Name = st.text_input('Patient Name')
    Phone_number = st.text_input('Mobile Number')
    Email = st.text_input('Email')
    Age = st.text_input('Age')
    upload_file = st.file_uploader('Upload MRI image', type=['jpg', 'png', 'jpeg'])
    
    tumor_diagnosis = ''
    
    if st.button('Predict'):
        if upload_file is not None:
            media_folder = "media"
            os.makedirs(media_folder, exist_ok=True)
            file_path = os.path.join(media_folder, upload_file.name)
            with open(file_path, 'wb') as f:
                f.write(upload_file.getbuffer())
            
            Tumor_Prediction = getResult(file_path)
            print(Tumor_Prediction)
            if Tumor_Prediction==1:
                tumor_diagnosis = "The person has Brain Tumor"
            elif Tumor_Prediction==0:
                tumor_diagnosis = "The person did not have Brain Tumor"
            
            full_content = f"Patient Name: {Patient_Name}\nPhone_Number: {Phone_number}\nAge: {Age}\n Result: {tumor_diagnosis} \nUploaded image: {file_path}"
            send_email(full_content, Email, file_path)
    
    st.markdown(f'### {tumor_diagnosis}')


if (selected == 'Alzemeir Disease'):
    st.title('Alzemeir Disease detection using ML from MRI image')
    
    Patient_Name = st.text_input('Patient Name')
    Phone_number = st.text_input('Mobile Number')
    Email = st.text_input('Email')
    Age = st.text_input('Age')
    upload_file = st.file_uploader('Upload MRI image', type=['jpg', 'png', 'jpeg'])
    
    alzeimer_diagnosis = ''
    
    if st.button('Predict'):
        if upload_file is not None:
            media_folder = "media"
            os.makedirs(media_folder, exist_ok=True)
            file_path = os.path.join(media_folder, upload_file.name)
            with open(file_path, 'wb') as f:
                f.write(upload_file.getbuffer())
            
            Alzeimer_Prediction = alzeimerckh(file_path)
            
            if Alzeimer_Prediction==1:
                alzeimer_diagnosis = "The person has Alzeimer Disease"
            elif Alzeimer_Prediction==0:
                alzeimer_diagnosis = "The person did not have Alzeimer Disease"
            full_content = f"Patient Name: {Patient_Name}\nPhone_Number: {Phone_number}\nAge: {Age}\n Result: {alzeimer_diagnosis} \nUploaded image: {file_path}"
            send_email(full_content, Email, file_path)

    st.markdown(f'### {alzeimer_diagnosis}')

if (selected == 'Pneumonia Detection'):
    st.title('Pneumonia Detection using ML from MRI image')
    
    Patient_Name = st.text_input('Patient Name')
    Phone_number = st.text_input('Mobile Number')
    Email = st.text_input('Email')
    Age = st.text_input('Age')
    upload_file = st.file_uploader('Upload X-Ray image', type=['jpg', 'png', 'jpeg'])
    
    pneumonia_diagnosis = ''
    
    if st.button('Predict'):
        if upload_file is not None:
            media_folder = "media"
            os.makedirs(media_folder, exist_ok=True)
            file_path = os.path.join(media_folder, upload_file.name)
            with open(file_path, 'wb') as f:
                f.write(upload_file.getbuffer())
            
            Pneumonia_Prediction = predict_image(file_path)
            pneumonia_diagnosis = Pneumonia_Prediction
            full_content = f"Patient Name: {Patient_Name}\nPhone_Number: {Phone_number}\nAge: {Age}\n Result: {pneumonia_diagnosis} \nUploaded image: {file_path}"
            send_email(full_content, Email, file_path)

    st.markdown(f'### {pneumonia_diagnosis}')

if (selected == 'Diabetes Detection'):
    st.title('Diabetes Detection using ML')
    
    Patient_Name = st.text_input('Patient Name')
    Age = st.text_input('Age of the person')
    Email = st.text_input('Email')
    Pregnancies = st.text_input('Number of Pregnancies')
    Glucose = st.text_input('Glucose level')
    BloodPressure = st.text_input('Blood pressure value')
    SkinThickness = st.text_input('Skin thickness value')
    Insulin = st.text_input('Insulin level')
    BMIs = st.text_input('BMI value')
    DiabetespedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    
    diab_diagnosis = ''

    if st.button('Diabetes Test Result'):
        diab_prediction = Diabetes_Model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMIs, DiabetespedigreeFunction, Age]])
        if(diab_prediction[0]==1):
            diab_diagnosis='The person have Diabetic'
        else:
            diab_diagnosis='The person is not have Diabetic'
        full_content = f"Patient Name: {Patient_Name}\nAge: {Age}\nResult: {diab_diagnosis}"
        sends_email(full_content, Email)
    
    st.markdown(f'### {diab_diagnosis}')
    Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMIs, Age, DiabetespedigreeFunction = '', '', '', '', '', '', '', ''