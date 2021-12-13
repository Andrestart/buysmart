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

    dia = pd.DataFrame(list(c.engine.execute(f"""SELECT  `namescrap` as `Name`, `supermarket` as `Super`, `price` FROM `dia` WHERE `product_idproduct` = {idprod}""")))
    dia.columns = ['Name', 'Super', 'Price']

    eroski = pd.DataFrame(list(c.engine.execute(f"""SELECT `namescrap` as `Name`, `supermarket` as `Super`, `price` FROM `eroski` WHERE `product_idproduct` = {idprod}""")))    
    eroski.columns = ['Name', 'Super', 'Price']
    
    carrefour = pd.DataFrame(list(c.engine.execute(f"""SELECT `namescrap` as `Name`, `supermarket` as `Super`, `price` FROM `carrefour` WHERE `product_idproduct` = {idprod}""")))
    carrefour.columns = ['Name', 'Super', 'Price']
    
    allperproduct = pd.concat([dia,carrefour,eroski],axis=0)
    allperproduct.to_csv("mydata/cleandata/allperproduct.csv",index=False)
    fin =  pd.read_csv("mydata/cleandata/allperproduct.csv")
    st.table(fin.style.format({'Price':'{:.2f}'}))