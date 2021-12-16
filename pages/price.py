import sys
sys.path.append("../")
import config.sqlconfig as c
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd
import before_streamlit.prohibido as p
import src.manage_data as dat
import os
import plotly.express as px
from datetime import datetime

def app():
    st.sidebar.image("images/Andres Perez logo2.png", use_column_width=True)
    
    ##SELECTBOX
    prod = st.selectbox("Select the product you are looking for", dat.product())
    if prod == "Choose":
        st.stop()
    
    imgfood = f"images/food/{prod}.jpg"
    st.image(imgfood, use_column_width=True)


    
    idprod = list(c.engine.execute(f"SELECT `idproduct` FROM `product` WHERE `nameproduct` ='{prod}';"))[0][0]
    
    #####SUPERMARKET DATAFRAMES#######
    ##DIA DATAFRAME
    dia = pd.DataFrame(list(c.engine.execute(f"""SELECT  `namescrap` as `Name`,  `price`,`supermarket` as `Super`, `link` FROM `dia` WHERE `product_idproduct` = {idprod}""")))
    try:
        dia.columns = ['Name', 'Price', 'Super', 'Link']
    except:
        pass
    ##EROSKI DATAFRAME
    eroski = pd.DataFrame(list(c.engine.execute(f"""SELECT  `namescrap` as `Name`,  `price`,`supermarket` as `Super`, `link` FROM `eroski` WHERE `product_idproduct` = {idprod}""")))    
    try:
        eroski.columns = ['Name', 'Price', 'Super', 'Link']
    except:
        pass
    ##CARREFOUR DATAFRAME
    carrefour = pd.DataFrame(list(c.engine.execute(f"""SELECT  `namescrap` as `Name`,  `price`,`supermarket` as `Super`, `link` FROM `carrefour` WHERE `product_idproduct` = {idprod}""")))
    try:
        carrefour.columns = ['Name', 'Price', 'Super', 'Link']
    except:
        pass

    ##MANAGING IF THERE IS NO DATA FOR A SUPERMARKET
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

    ##TABLES TO BE SHOWN
    allperproduct['product'] = prod
    if not os.path.exists("mydata/cleandata/stdata/"):
        os.makedirs("mydata/cleandata/stdata/")
    allperproduct.to_csv("mydata/cleandata/stdata/allperproduct.csv",index=False)
    wholetable =  pd.read_csv("mydata/cleandata/stdata/allperproduct.csv", index_col=False)
    
    #FILTERING 5 MINIMUM PRICES
    minperproduct = p.filter(wholetable, prod).sort_values(by='Price')
    st.write("""*These are the cheapest products*""")
    minper = minperproduct.drop_duplicates(subset=['Name','Super']).reset_index()
    minper = minper[:5]
    minper.drop(['index','product'],axis=1,inplace=True)
    minper.to_csv("mydata/cleandata/stdata/minperproduct.csv",index=False)
    

    #MANAGING IF THERE IS NO DATA IN 5 MIN TABLE
    if len(minper) == 0:
        st.write("\n\n Sorry, the product is not available in the supermarkets right now, but you can take a look at the products below that contain that word.")
    #5 MIN TABLE
    else:
        st.table(minper.style.format({'Price':'{:.2f}'}))
  

    #PREDICTIONS
    try:
        predictions = dat.pred(prod)
        predictions.to_csv("mydata/cleandata/stdata/pred.csv")
        pred = pd.read_csv("mydata/cleandata/stdata/pred.csv")
        #PREDICTIONS GRAPH
        fig = px.line(pred, x='date', y='Price',title=minper.Name[0])
        fig.update_yaxes(range=[0.99*min(pred['Price']),1.02*max(pred['Price'])]) 
        st.plotly_chart(fig)
    except:
        st.write("""Impossible to predict with no data.""")

    scat = px.scatter(wholetable, x='Super', y='Price', color='Super', title=prod.capitalize())
    st.plotly_chart(scat)
  
    #WHOLE TABLE
    st.write("\n\n\n\n\n If these products are not the ones you are looking for, you can check the whole table and its results below\n")
    st.table(wholetable.style.format({'Price':'{:.2f}'}))