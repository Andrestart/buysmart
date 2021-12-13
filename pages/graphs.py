import sys
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import sqlalchemy as alch
import os
import dotenv
import pandas as pd
import src.manage_data as dat

dotenv.load_dotenv()
password = os.getenv("pass")
dbName = "buysmart"
connectionData = f"mysql+pymysql://root:{password}@localhost/{dbName}"
engine = alch.create_engine(connectionData)


def app():
    prod = st.selectbox("Select the product you are looking for", dat.product())

    idprod = list(engine.execute(f"SELECT `idproduct` FROM `product` WHERE `nameproduct` ='{prod}';"))[0][0]

    e = list(engine.execute(f"""SELECT `graph` FROM `graphs` WHERE `product_idproduct` = {idprod}"""))
    try:
        graph0 = Image.open(str(e[0])[6:-3])
        graph1 = Image.open(str(e[1])[6:-3])

        st.image(graph0, use_column_width=True)
        st.image(graph1, use_column_width=True)
    except:
        st.write("""We don't have predictions for""", prod)