# importing the requests library
import requests
# import pandas as pd
import streamlit as st

# api-endpoint
URL = ""




def tempPostRequest(folder_path, project_id, project_name, color_scheme, baseline_accuracy, tech_option, parameter):

    endPoint = URL + '/optimize'
    data = {
        'project_path': folder_path,
        'project_id': project_id,
        'project_name': project_name,
        'color_scheme': color_scheme,
        'baseline_accuracy': baseline_accuracy,
        'techniques': tech_option,
        'epoch': parameter[0],
        'batch_size': parameter[1],
        'optimizer': parameter[2],
        'learning_rate': parameter[3]
    }
    r = requests.post(url=endPoint, json= data) #project_id will be returned
    if r.status_code == 200:
        return r.json()
    else:
        print('Error During Query: postJsonRequest()')
        print(r)
        return '0'


def getProject_Status(list_id):

    """Get all task status"""
    endPoint = URL + '/tasks_status'
    r = requests.post(url=endPoint, json=list_id)
    if r.status_code == 200:
        return r.json()
    else:
        print('Error During Query: postJsonRequest()')
        print(r)
        return '0'


#def getMetric(project_id):
