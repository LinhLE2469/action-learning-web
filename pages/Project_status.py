
import streamlit as st
from request import get_projects_status
import pandas as pd


def status():

    st.subheader("TRACKING TASK STATUS")
    projects = get_projects_status()
    if len(projects):
        df = pd.DataFrame()
        for elem in projects:
            data = {
                'Project id': elem['project_id'],
                'Project name': elem['project_name'],
                'Status': elem['status']
            }
            if elem['status'] == "DONE":
                project_link = f"http://localhost:8501/Reporting?id={elem['project_id']}"
                data['Report'] = f'<a target="_self" href="{project_link}"> See the report</a>'
            else:
                data['Report'] = "NOT READY"
            df = df.append(data, ignore_index=True)

        display = df.reindex(
            columns=[
                'Project id', 'Project name', 'Status', 'Report']
        )
        st.write(display.to_html(escape=False, index=False),
                 unsafe_allow_html=True)
    else:
        st.write("No projects to track")


if __name__ == '__main__':
    status()
