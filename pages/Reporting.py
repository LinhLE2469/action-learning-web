import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

def main():
    st.title('Task_id: 12345678')
    # First SubPlot
    epoch = 20
    x = np.arange(epoch)
    train_loss = [3, 7, 8, 10, 5, 6, 9, 13, 9, 16,1, 4, 5, 6, 7, 3, 8, 9, 7, 5]
    test_loss = [1, 4, 5, 6, 7, 3, 8, 9, 7, 5,3, 7, 8, 10, 5, 6, 9, 13, 9, 16]
    train_accuracy = [20, 30, 60, 50, 80, 50, 90, 70, 80, 95,10, 40, 50, 60, 70, 30, 80, 90, 70, 50]
    test_accuracy = [10, 40, 50, 60, 70, 30, 80, 90, 70, 50,20, 30, 60, 50, 80, 50, 90, 70, 80, 95]
    true_positive = [10, 11, 10, 12, 10, 13, 14, 13, 12, 15,13, 14, 15, 12, 14, 15, 16, 15, 14, 13]
    false_positive = [20, 23, 26, 25, 28, 25, 29, 27, 28, 29,21, 24, 25, 26, 27, 23, 28, 29, 27, 25]
    true_negative = [40, 45, 45, 47, 48, 46, 47, 47, 48, 49,46, 49, 45, 45, 45, 45, 48, 45, 47, 45]
    false_negative = [85, 86, 86, 87, 88, 88, 89, 87, 85, 98,89, 89, 90, 94, 95, 98, 80, 70, 79, 90]


    st.header('Train and Test loss by epoch')
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(
        x=x,
        y=train_loss,
        name='train',  # Style name/legend entry with html tags
        connectgaps=True  # override default to connect the gaps

    ))
    fig_loss.add_trace(go.Scatter(
        x=x,
        y=test_loss,
        name='test',
    ))

    st.write(fig_loss)
###### Accuracy #####
    st.header('Train and Test accuracy by epoch')
    fig_accuracy = go.Figure()
    fig_accuracy.add_trace(go.Scatter(
        x=x,
        y=train_accuracy,
        name='train',  # Style name/legend entry with html tags
        connectgaps=True  # override default to connect the gaps

    ))
    fig_accuracy.add_trace(go.Scatter(
        x=x,
        y=test_accuracy,
        name='test',
    ))

    st.write(fig_accuracy)

    ##### Confusion Matrix #####

    st.header('Confusion Matrix by epoch')
    fig_matrix= go.Figure()
    fig_matrix.add_trace(go.Scatter(
        x=x,
        y=true_negative,
        name='true_negative',  # Style name/legend entry with html tags
        connectgaps=True  # override default to connect the gaps

    ))
    fig_matrix.add_trace(go.Scatter(
        x=x,
        y=true_positive,
        name='true_positive',
    ))
    fig_matrix.add_trace(go.Scatter(
        x=x,
        y=false_positive,
        name='false_positive',
    ))
    fig_matrix.add_trace(go.Scatter(
        x=x,
        y=false_negative,
        name='false_negative',
    ))

    st.write(fig_matrix)


if __name__ == '__main__':
        main()