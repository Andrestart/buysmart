import streamlit as st
import pandas as pd
from PIL import Image

def app():
    st.sidebar.image("images/tools.png", use_column_width=True)

    #IMGS
    sql = Image.open("images/sqlschema.PNG")

    #WHY
    st.write("""# *Why have you done this!?*\n\n I have always been interested in economics and prices behaviour. Food prices are very variable so creating a predicting tool could be a nice challenge.\n""")
    st.write("""This project makes it easier to understand how food prices have been variating during last years and get a prediction for the following years. \n\n""")
    
    #TOOLS AND PROCESS
    st.write("""## TOOLS AND PROCESS\n""")
    st.write("""- 1. Getting historical food prices making [API](https://en.wikipedia.org/wiki/API) requests to [Agrifood](https://agridata.ec.europa.eu/extensions/DataPortal/API_Documentation.html). \n""")
    st.write("""- 2. Cleaning, organizing and unifying categories.\n""")
    st.write("""- 3. Predicting the prices based on the historical data using FB PROPHET. \n""")
    st.write("""- 4. Getting today's food prices from different supermarkets (conditional scrapping) using SELENIUM.\n""")
    st.write("""- 5. Creating a database to store and organize my data using SQL.""")
    st.image(sql, use_column_width=True)
    st.write("""\n- 6. Filtering the database to get exactly the information I'm looking for.\n""")
    st.write("""- 7. User-friendly platform to show my graphs and data using STREAMLIT.\n""")
    st.write("""- 8. Making the whole process executable so the end user can just run the program and get all updated information everyday without knowing how the code looks like.""")