import sys
sys.path.append("../")
import config.sqlconfig as c
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd

import src.manage_data as dat


def app():
    prod = st.selectbox("Select the product you are looking for", dat.product())

    idprod = list(c.engine.execute(f"SELECT `idproduct` FROM `product` WHERE `nameproduct` ='{prod}';"))[0][0]

    # try:
    dia = pd.DataFrame(list(c.engine.execute(f"""SELECT  `namescrap` as `Name`, `supermarket` as `Super`, `price` FROM `dia` WHERE `product_idproduct` = {idprod}""")))
    dia.columns = ['Name', 'Super', 'Price']
    print(dia)
    # except:
    #     dia = f"No data for {prod}"
    #     print(f"No data for {prod} in Dia")
    eroski = pd.DataFrame(list(c.engine.execute(f"""SELECT `supermarket` as Super,`price` as Price, `namescrap` as Product FROM `eroski` WHERE `product_idproduct` = {idprod}""")))    
    carrefour = pd.DataFrame(list(c.engine.execute(f"""SELECT `namescrap` as `Name`, `supermarket` as `Super`, `price` FROM `carrefour` WHERE `product_idproduct` = {idprod}""")))
    print(carrefour)
    # dframe = pd.DataFrame(dia)
    # dframe = pd.concat([pd.DataFrame(dia), pd.DataFrame(eroski),pd.DataFrame(carrefour)], axis=1)
    # dframe = pd.concat([dia, carrefour], axis=1)
    # print(dframe)
    dia.to_csv("diaaa.csv",index=False)
    final = pd.read_csv('diaaa.csv')
    final = final.round(2)
    print(final.dtypes)
    st.table(final.style.format({'Price':'{:.2f}'}))