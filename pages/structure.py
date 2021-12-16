import streamlit as st
import pandas as pd
from PIL import Image

def app():
    st.sidebar.image("images/tools.png", use_column_width=True)

    #IMGS
    dataimg = Image.open("images/data.PNG")
    sql = Image.open("images/sqlschema.PNG")

    #WHY
    st.write("""# *Why have you done this!?*\n\n I have always been interested in economics and prices behaviour. Food prices are very variable so creating a predicting tool could be a nice challenge.\n""")
    st.write("""This project makes it easier to understand how food prices have been variating during last years and get a prediction for the next years. \n\n""")
    
    #TOOLS
    st.write("""## Tools used:\n""")
    st.write("""- API requests. \n""")
    st.write("""- SQL server and SQL Workbench.\n""")
    st.write("""- FB prophet for timeseries predictions.\n""")
    st.write("""- Selenium for scrapping supermarket prices.\n""")
    st.write("""- Streamlit to show my graphs and data.\n""")

    #STRUCTURE
    st.write("""## BUT HOW DID YOU DO IT?\n""")
    st.write("""I followed the following structure: \n""")
    st.write("""- Getting historical price data making a request to an [API](https://en.wikipedia.org/wiki/API) called [Agrifood](https://agridata.ec.europa.eu/extensions/DataPortal/API_Documentation.html).\n""")
    st.write("""- Saving it into different food categories to simplify it. After cleaning my dataframe, it looked like this:\n""")
    st.image(dataimg, use_column_width=False)
    st.write("""- Separating the dataframe per product and preparing it for predictions.\n""")
    st.write("""- Predicting the food prices per product.\n""")
    st.write("""- Getting today's food prices from different supermarkets (conditional scrapping).\n""")
    st.write("""- Creating a database to store the historical and today's data and the graphs generated.\n""")
    st.image(sql, use_column_width=True)
    st.write("""- Making a user-friendly web to show the graphs and conclusions.\n""")
    st.write("""- Making the whole process executable so the end user can just run the program and get all updated information everyday without knowing how the code looks like.""")
