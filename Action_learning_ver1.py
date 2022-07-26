import os
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import zipfile
import tempfile
import tensorflow as tf
import uuid
from request import tempPostRequest



def main():

    st.subheader("LOAD DATASET")
    dataset = st.file_uploader('Upload dataset(csv.zip)', type='zip')
    st.subheader("LOAD MODEL")
    model = st.file_uploader('TF.Keras model file (.h5py.zip)', type='zip')

    ### TECH OPTION###
    tech_option = []
    st.subheader("TECHNIQUE OPTION")
    # setup file upload
    st.write('Select optimize technique:')
    option_1 = st.checkbox('Pruning')
    option_2 = st.checkbox('Quantization')
    option_3 = st.checkbox('Knowledge Distillation')
    if option_1 is True:
        tech_option.append('pruning')
    if option_2 is True:
        tech_option.append('quantization')
    if option_3 is True:
        tech_option.append('knowledge_distillation')

    ### PARAMETER####

    st.subheader("PARAMETER")
    epochs = st.slider("Select number of epochs:", 1, 1000)
    st.text('epochs: {}'.format(epochs))
    optimizer = st.selectbox("Optimizer ",
                             ['Adam', 'SGD', 'RMSprop', 'Adadelta', 'Adagrad', 'Adamax', 'Nadam', 'Ftrl'])
    learning_rate = st.slider("Select learning rate(alpha):", pow(10, -3), 1.0)
    batch_size = st.number_input("Batch_size")
    parameter = [epochs,batch_size,optimizer,learning_rate]
    st.write(parameter)

    ##BUTTON####
    alert_message = st.empty()  # keep space
    predict_button = st.button(label="Optimize", key="Optimize_button")
    folder_path = 1

    ###SAVING####

    if predict_button is False and all([tech_option,epochs,batch_size,optimizer,learning_rate, dataset, model]) :

        id = uuid.uuid1()
        str(id)
        path = ("C:/Users/trucl/Documents/optimizer/" + str(id))

        dataset_zip = zipfile.ZipFile(dataset)
        dataset_zip.extractall(path)
        files = dataset_zip.namelist()[0]  # file_name
        folder_path = os.path.join(path, files)
        # st.info(f'trying to load model from tmp dir {model_dir}...')
        st.write(folder_path)

        ####MODEL####
        model_zip = zipfile.ZipFile(model)
        model_zip.extractall(path)
        model_file = model_zip.namelist()[0]  # e.g. "model.h5py"
        folder_path = os.path.join(path, model_file)
        # st.info(f'trying to load model from tmp dir {model_dir}...')
        model = tf.keras.models.load_model(folder_path)
        st.write(folder_path)

    ###ACTION####

    if predict_button and not all([dataset,model, tech_option,epochs,batch_size,optimizer,learning_rate]):
        alert_message.warning('Please full fill all information before clicking optimize !!!!')
    if predict_button and all([dataset,model, tech_option,epochs,batch_size,optimizer,learning_rate]):
        task_ids = tempPostRequest(folder_path, tech_option,parameter)
        

if __name__ == '__main__':
    html_temp = """
            <div style="background-color:green;padding:5px">
            <h2 style="color:white;text-align:center;">
                Optimization of deep learning models
            </h2>
            </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)

    main()


