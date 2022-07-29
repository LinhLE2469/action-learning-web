import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from request import get_project_report
from utils import size_human_format, format_seconds, format_milliseconds, get_difference_percentage


def main():
    st.set_page_config(layout="wide")
    try:
        query_params = st.experimental_get_query_params()
        project_id = query_params['id'][0]
        results = get_project_report(project_id)
        tasks = results['tasks']

        if len(tasks):
            st.header(f"Project: {results['project_name']}")
            # Display the accuracy graph
            st.markdown("""---""")
            st.header("Accuracy")
            st.subheader("Accuracy Graph")
            accuracy_graph_cols = st.columns(len(tasks))
            for i, task in enumerate(tasks):
                technique = task['task_result']['technique']
                accuracy_graph_cols[i].write(technique.capitalize())
                if technique == 'distillation':
                    accuracy_data = pd.DataFrame(
                        {
                            'Epochs': np.arange(1, task['task_result']['epoch'] + 1),
                            'Training Accuracy': task['task_result']['metrics']['hist']['sparse_categorical_accuracy']
                        }
                    )
                    fig = px.line(
                        accuracy_data,
                        x='Epochs',
                        y=['Training Accuracy'],
                        labels={'Epochs': 'Epochs', 'Accuracy': 'Accuracy'}
                    )
                else:
                    accuracy_data = pd.DataFrame(
                        {
                            'Epochs': np.arange(1, task['task_result']['epoch'] + 1),
                            'Training Accuracy': task['task_result']['metrics']['hist']['sparse_categorical_accuracy'],
                            'Validation accuracy': task['task_result']['metrics']['hist']['val_sparse_categorical_accuracy']
                        }
                    )
                    fig = px.line(
                        accuracy_data,
                        x='Epochs',
                        y=['Training Accuracy', 'Validation accuracy'],
                        labels={'Epochs': 'Epochs', 'Training Accuracy': 'Training Accuracy',
                                'Validation accuracy': 'Validation accuracy'}
                    )
                fig.update_layout(
                    legend=dict(
                        title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
                    ),
                    margin=dict(l=5, r=5, t=20, b=20)
                )
                accuracy_graph_cols[i].plotly_chart(
                    fig, use_container_width=True)

            # Display the accuracy on unseen data
            st.subheader("Accuracy on unseen data")
            accuracy_on_unseen_data_cols = st.columns(len(tasks))
            for i, task in enumerate(tasks):
                technique = task['task_result']['technique']
                accuracy_on_unseen_data_cols[i].write(
                    f"{technique.capitalize()} accuracy:")
                accuracy_on_unseen_data_cols[i].header(
                    f"{task['task_result']['metrics']['test accuracy'] * 100:.2f}%")
                accuracy_on_unseen_data_cols[i].write(f"Baseline accuracy:")
                accuracy_on_unseen_data_cols[i].header(
                    f"{task['task_result']['baseline_accuracy']}%")

            # Display the size of the models
            st.markdown("""---""")
            st.subheader("Model Size")
            size_cols = st.columns(len(tasks))
            for i, task in enumerate(tasks):
                technique = task['task_result']['technique']
                size_cols[i].write(f"{technique.capitalize()} compression:")
                if technique == 'pruning':
                    size_cols[i].header(
                        f"{get_difference_percentage(task['task_result']['metrics']['baseline model size'], task['task_result']['metrics']['pruned_model_size'])}")
                    size_cols[i].write(
                        f"{technique.capitalize()} size: {size_human_format(task['task_result']['metrics']['pruned_model_size'])}")
                elif technique == 'quantization':
                    size_cols[i].header(
                        f"{get_difference_percentage(task['task_result']['metrics']['baseline model size'], task['task_result']['metrics']['quantized_model_size'])}")
                    size_cols[i].write(
                        f"{technique.capitalize()} size: {size_human_format(task['task_result']['metrics']['quantized_model_size'])}")
                else:
                    size_cols[i].header(
                        f"{get_difference_percentage(task['task_result']['metrics']['baseline model size'], task['task_result']['metrics']['distilled model size'])}")
                    size_cols[i].write(
                        f"{technique.capitalize()} size: {size_human_format(task['task_result']['metrics']['distilled model size'])}")

                size_cols[i].write(
                    f"Baseline size: {size_human_format(task['task_result']['metrics']['baseline model size'])}")

            # Display the time spent
            st.markdown("""---""")
            st.subheader("Time")
            time_cols = st.columns(len(tasks))
            for i, task in enumerate(tasks):
                technique = task['task_result']['technique']
                time_cols[i].write(f"{technique.capitalize()} Training time:")
                time_cols[i].header(
                    f"{format_seconds(task['task_result']['metrics']['training time'])}")
                time_cols[i].write(f"{technique.capitalize()} Inference time:")
                time_cols[i].header(
                    f"{format_milliseconds(task['task_result']['metrics']['inference time'])}")

            # Display the weights
            st.markdown("""---""")
            st.subheader("Weights")
            weights_cols = st.columns(len(tasks))
            for i, task in enumerate(tasks):
                technique = task['task_result']['technique']
                weights_cols[i].write(
                    f"{technique.capitalize()} weight reduction:")
                weights_cols[i].header(
                    f"{get_difference_percentage(task['task_result']['metrics']['baseline parameters'], task['task_result']['metrics']['parameters'])}")
                weights_cols[i].write(
                    f"{technique.capitalize()} weights: {task['task_result']['metrics']['parameters']}")
                weights_cols[i].write(
                    f"Baseline weights: {task['task_result']['metrics']['baseline parameters']}")

            # Display dowload button
            st.markdown("""---""")
            download_cols = st.columns(len(tasks))
            for i, task in enumerate(tasks):
                technique = task['task_result']['technique']
                if technique == 'pruning':
                    _file = open(
                        f"{task['task_result']['project_path']}/pruned_model.h5", "rb")
                    download_cols[i].download_button(
                        label=f"Download {technique} model",
                        data=_file,
                        file_name=f"{technique}_model.h5"
                    )
                elif technique == 'quantization':
                    _file = open(
                        f"{task['task_result']['project_path']}/quantized_model_lite.tflite", "rb")
                    download_cols[i].download_button(
                        label=f"Download {technique} model",
                        data=_file,
                        file_name=f"{technique}_model.tflite"
                    )
                else:
                    _file = open(
                        f"{task['task_result']['project_path']}/distilled_model.h5", "rb")
                    download_cols[i].download_button(
                        label=f"Download {technique} model",
                        data=_file,
                        file_name=f"{technique}_model.h5"
                    )

        else:
            st.write("No tasks found")

    except Exception as e:
        st.write(e)
        st.write('''Please create a project first''')


if __name__ == '__main__':
    main()
