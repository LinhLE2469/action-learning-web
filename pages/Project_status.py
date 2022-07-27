
import streamlit as st
from request import tempPostRequest
import pandas as pd


def status():

    st.subheader("TRACKING TASK STATUS")
    #link1 = "http://localhost:8501/Reporting"
    df = pd.DataFrame()
    for elem in st.session_state.project_refs:
        data = {'Project_id': elem['project_id'], 'Project_name': elem['project_name'],
                'Technique': elem['technique'],
                'Status': elem['status']}
        # if project['status'] == "done":
        # task_link = f"{link1}/{task['task_id']}"
        # data['Report'] =f'<a target="_blank" href="{task_link}"> See the report</a>'
        df = df.append(data, ignore_index=True)

    display = df.reindex(
        columns=[
            'Project_id', 'Project_name', 'Technique', 'Status']
    )
    st.write(display.to_html(escape=False, index=False), unsafe_allow_html=True)


if __name__ == '__main__':
    status()
