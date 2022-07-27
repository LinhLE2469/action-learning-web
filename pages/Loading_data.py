import os
import streamlit as st
import zipfile
import tensorflow as tf
import uuid
from request import tempPostRequest,getProject_Status

def saving (dataset,model):

    id = uuid.uuid1()
    project_id = str(id)
    path = ("C:/Users/trucl/Documents/optimizer/" + project_id)

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

    return folder_path, project_id

def main():
    st.subheader("LOAD DATASET")
    dataset = st.file_uploader('Upload dataset(csv.zip)', type='zip')
    color_scheme = st.selectbox("Color_scheme ",
                             ['grayscale', 'rgb'])
    st.subheader("LOAD MODEL")
    model = st.file_uploader('TF.Keras model file (.h5py.zip)', type='zip')
    baseline_accuracy = st.number_input("Current accuracy of the model", min_value=0, max_value=100)
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

    learning_rate = st.slider("Select learning rate(alpha):", pow(10, -3), 1.0)
    parameter = [epochs, batch_size, optimizer, learning_rate]


    ##BUTTON####
    alert_message = st.empty()  # keep space
    predict_button = st.button(label="Optimize", key="Optimize_button")
    folder_path = 1

    ###ACTION####
    if predict_button and not all(
            [dataset, model, color_scheme, project_name,baseline_accuracy, tech_option, epochs, batch_size, optimizer, learning_rate
             ]):
        alert_message.warning('Please full fill all information before clicking optimize !!!!')
    if predict_button and all([dataset, model, color_scheme, project_name,baseline_accuracy, tech_option, epochs, batch_size, optimizer, learning_rate]):
        path , project_id = saving(dataset,model)
        st.write(path)
        st.write(project_id)
        #project_ref = tempPostRequest(path,project_id,color_scheme, tech_option, parameter, baseline_accuracy, project_name)

        project_ref = {
            "project_id": '123456',
            "project_name": "Classification",
            "initiated time": "6 PM 39",
            "technique": "pruning",
            "status": "pending"
        }

        project_refs_update = [{
            "project_id": '123456',
            "project_name": "Classification",
            "initiated time": "6 PM 39",
            "technique": "pruning",
            "status": "done"

        },
            {
            "project_id": '1234567',
            "project_name": "Classification",
            "initiated time": "6 PM 39",
            "technique": "pruning",
            "status": "done"

        }
    ]

        if 'project_refs' not in st.session_state:
            st.session_state.project_refs = [project_ref]
        else:
            project_refs = st.session_state.project_refs
            project_refs.append(project_ref)
            st.session_state.project_refs = project_refs

        st.write(st.session_state.project_refs)

        # get id from data
        get_id = [project_ref['project_id'] for i in st.session_state.project_refs]
        list_id = list(get_id)
    ### GET PROJECT STATUS ###
        # project_refs_update = getProject_Status(list_id)
        for i in st.session_state.project_refs:
            for k in project_refs_update:
                if i['project_id'] == k['project_id']:
                    i['status'] = k['status']

        st.write(st.session_state.project_refs)

if __name__ == '__main__':
    main()
