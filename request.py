# importing the requests library
import requests
#import pandas as pd

# api-endpoint
URL = ""


def tempPostRequest(folder_path, tech_option,parameter):
    endPoint = URL + '/optimize'
    data = {
        'path': folder_path,
        'techniques': tech_option,
        'epochs': parameter[0],
        'batch_size':parameter[1],
        'optimizer':parameter[2],
        'learning_rate':parameter[3]
    }
    task_id = requests.post(url=endPoint, json= data) #task_id is array of task object

    print(x.text)

