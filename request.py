import os
# importing the requests library
import requests
# import pandas as pd
import streamlit as st

# api-endpoint
URL = "http://localhost:8080"


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
    r = requests.post(url=endPoint, json=data)  # project_id will be returned
    if r.status_code == 200:
        return r.json()
    else:
        print('Error During Query: tempPostRequest()')
        print(r)
        return '0'


def get_all_projects_id():
    """Get all task from projects folder"""
    files = os.listdir('/Users/guitoo/Documents/optimizer/')
    # remove hidden files
    files = [file for file in files if not file.startswith('.')]
    return files


def get_projects_status():
    """Get all task status"""
    endPoint = URL + '/status/projects'
    data = {
        'projects_ids': get_all_projects_id()
    }
    r = requests.post(url=endPoint, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        print('Error During Query: getProjects_Status()')
        print(r)
        return '0'


# Get the report of project
def get_project_report(project_id):
    """Get the report of project"""
    endPoint = URL + '/report/project/' + project_id
    r = requests.get(url=endPoint)
    if r.status_code == 200:
        return r.json()
    else:
        print('Error During Query: getProject_Report()')
        print(r)
        return '0'

# def getMetric(project_id):
