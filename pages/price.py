import sys
sys.path.append("../")
import config.sqlconfig as c
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd
import before_streamlit.prohibido as p
import src.manage_data as dat


def app():
    prod = st.selectbox("Select the product you are looking for", dat.product())

    idprod = list(c.engine.execute(f"SELECT `idproduct` FROM `product` WHERE `nameproduct` ='{prod}';"))[0][0]

    dia = pd.DataFrame(list(c.engine.execute(f"""SELECT  `namescrap` as `Name`, `supermarket` as `Super`, `price`, `link` FROM `dia` WHERE `product_idproduct` = {idprod}""")))
    try:
        dia.columns = ['Name', 'Super', 'Price', 'Link']
    except:
        pass
    # dia['forlink'] = "['Click here to get it']("
    # dia['Link'] = dia['forlink']+dia['Link']+')'
    # dia.drop('forlink',axis=1, inplace=True)

    eroski = pd.DataFrame(list(c.engine.execute(f"""SELECT `namescrap` as `Name`, `supermarket` as `Super`, `price`, `link` FROM `eroski` WHERE `product_idproduct` = {idprod}""")))    
    try:
        eroski.columns = ['Name', 'Super', 'Price', 'Link']
    except:
        pass
    # eroski['forlink'] = "['Click here to get it']("
    # eroski['Link'] = eroski['forlink']+eroski['Link']+')'
    # eroski.drop('forlink',axis=1, inplace=True)

    carrefour = pd.DataFrame(list(c.engine.execute(f"""SELECT `namescrap` as `Name`, `supermarket` as `Super`, `price`, `link` FROM `carrefour` WHERE `product_idproduct` = {idprod}""")))
    try:
        carrefour.columns = ['Name', 'Super', 'Price', 'Link']
    except:
        pass
    # carrefour['forlink'] = "[Click here to get it]("
    # carrefour['Link'] = st.write(carrefour['forlink']+carrefour['Link']+')')
    # carrefour.drop('forlink',axis=1, inplace=True)

    if len (eroski) == 0 and len(dia) == 0:
        allperproduct = carrefour
    elif len(carrefour) == 0 and len(eroski) == 0:
        allperproduct = dia
    elif len(dia) == 0 and len(carrefour) == 0:
        allperproduct = eroski
    elif len(carrefour) == 0:
        allperproduct = pd.concat([dia,eroski],axis=0)
    elif len(eroski) == 0:
        allperproduct = pd.concat([dia,carrefour],axis=0)
    elif len(dia) == 0:
        allperproduct = pd.concat([eroski,carrefour],axis=0)
    else:
        allperproduct = pd.concat([eroski,carrefour, dia],axis=0)

    allperproduct['product'] = prod
    allperproduct.to_csv("mydata/cleandata/allperproduct.csv",index=False)
    wholetable =  pd.read_csv("mydata/cleandata/allperproduct.csv", index_col=False)
    
    minperproduct = p.filter(wholetable, prod).sort_values(by='Price').reset_index().head()
    minperproduct.drop(['index','product'],axis=1,inplace=True)
    minperproduct.to_csv("mydata/cleandata/minperproduct.csv",index=False)

    st.write("HOLAAA")
    st.table(minperproduct.style.format({'Price':'{:.2f}'}))
    st.write("\n\n\n\n\n If these products are not the ones you are looking for, you can check the whole table and its results below\n")
    st.table(wholetable.style.format({'Price':'{:.2f}'}))