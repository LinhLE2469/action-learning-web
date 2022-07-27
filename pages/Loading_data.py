import os
import streamlit as st
import zipfile
import tensorflow as tf
import uuid
from request import tempPostRequest


def saving(dataset, model):

    id = uuid.uuid1()
    project_id = str(id)
    path = ("/Users/guitoo/Documents/optimizer/" + project_id)

    dataset_zip = zipfile.ZipFile(dataset)
    dataset_zip.extractall(path)

    ####MODEL####
    model_zip = zipfile.ZipFile(model)
    model_zip.extractall(path)

    return path, project_id


def main():
    st.subheader("LOAD DATASET")
    dataset = st.file_uploader('Upload dataset(csv.zip)', type='zip')
    color_scheme = st.selectbox("Color_scheme ",
                                ['grayscale', 'rgb'])
    st.subheader("LOAD MODEL")
    model = st.file_uploader('TF.Keras model file (.h5py.zip)', type='zip')
    baseline_accuracy = st.number_input(
        "Current accuracy of the model", min_value=0.00, max_value=100.00, step=1., format="%.2f")
    project_name = st.text_input("Project name")

    ### TECH OPTION###
    tech_option = []
    st.subheader("TECHNIQUE OPTION")
    # setup file upload
    st.write('Select optimize technique:')
    option_1 = st.checkbox('Pruning')
    option_2 = st.checkbox('Quantization')
    option_3 = st.checkbox('Distillation')
    if option_1 is True:
        tech_option.append('pruning')
    if option_2 is True:
        tech_option.append('quantization')
    if option_3 is True:
        tech_option.append('distillation')

    ### PARAMETER####

    st.subheader("PARAMETER")
    epochs = st.number_input("Select number of epochs:")
    batch_size = st.number_input("Batch_size")
    optimizer = st.selectbox("Optimizer ",
                             ['Adam', 'SGD', 'RMSprop'])

    learning_rate = st.number_input(
        "Select learning rate(alpha):", step=0.001, format="%.3f")
    parameter = [epochs, batch_size, optimizer, learning_rate]

    ##BUTTON####
    alert_message = st.empty()  # keep space
    predict_button = st.button(label="Optimize", key="Optimize_button")

    ###ACTION####
    if predict_button and not all(
            [dataset, model, color_scheme, project_name, baseline_accuracy, tech_option, epochs, batch_size, optimizer, learning_rate
             ]):
        alert_message.warning(
            'Please full fill all information before clicking optimize !!!!')
    if predict_button and all([dataset, model, color_scheme, project_name, baseline_accuracy, tech_option, epochs, batch_size, optimizer, learning_rate]):
        path, project_id = saving(dataset, model)
        project_ref = tempPostRequest(
            folder_path=path,
            project_id=project_id,
            project_name=project_name,
            color_scheme=color_scheme,
            baseline_accuracy=baseline_accuracy,
            tech_option=tech_option,
            parameter=parameter
        )

        st.success('We are currently optimizing your model using the selected techniques. It might take a while. Please check the "Project Status" tab to see the status of your project.')


if __name__ == '__main__':
    main()
