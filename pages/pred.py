import streamlit as st
import pandas as pd
import src.manage_data as dat
import plotly.express as px


def app():
    st.sidebar.image("images/Andres Perez logo2.png", use_column_width=True)

    ##SELECTBOX
    prod = st.selectbox("Select the product you are looking for", dat.product())
    if prod == "Choose":
        st.stop()

    #PREDICTIONS TABLE
    predictions = dat.pred(prod)
    predictions.to_csv("mydata/cleandata/stdata/pred.csv")
    pred = pd.read_csv("mydata/cleandata/stdata/pred.csv")
    
    fig = px.bar(pred, x='date', y='Price',title=prod.capitalize())
    fig.update_yaxes(range=[min(pred['Price']),max(pred['Price'])]) 
    fig.show()

    st.plotly_chart(fig)
    # st.table(predictions)
    st.table(pred.style.format({'Price':'{:.2f}','index':'{:.2f}'}))