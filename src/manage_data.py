import pandas as pd
from datetime import datetime
import streamlit as st

def product():
    data = pd.read_csv("mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)
    foods = sorted(list(set(data['product'])))
    foods.insert(0,'Choose')
    return list(foods)

def pred(prod):
    now = str(datetime.now())[:10].replace(":","_")
    now = pd.to_datetime(now)
    now

    #####################################################
    ############### FORECAST  ###########################
    #####################################################
    prod = pd.read_csv(f"mydata/per_item/forecasts/{prod}.csv")
    prod['date'] = [pd.to_datetime(i) for i in prod['ds']]
    prod.drop('ds',axis=1,inplace=True)

    #LASTPRICE#
    tillnow = prod[prod['date'] < now]
    lastprice = tillnow.tail(1)[['date','yhat']]

    ###5 PREDICTIONS######
    pred = prod[prod['date'] > now]
    pred = pd.DataFrame(pred.iloc[0:300,:])[['date','yhat']]

    #JOIN LAST PRICE AND PREDICTIONS
    joined = pd.concat([lastprice,pred],axis=0)
    joined['yhat'].iloc[0]

    #INSERT %CHANGE
    joined['change(%)'] = (joined['yhat']-joined['yhat'].iloc[0])/joined['yhat'].iloc[0]+1

    #####################################################
    ################## TODAY  ###########################
    #####################################################

    today = pd.read_csv("mydata/cleandata/stdata/minperproduct.csv")
    #JOIN PREDICTION AND TODAY
    fin = pd.DataFrame(pd.concat([pd.DataFrame(today.iloc[0,:]).T,joined]))

    #GET THE PRICES PREDICTED USING %CHANGE IN FORECASTS
    # ie = st.selectbox(list(fin.Name))
    fin['Name'] = fin['Name'].iloc[0]
    fin['Super'] = fin['Super'].iloc[0]
    fin['Price'] = fin['Price'].iloc[0]
    fin['newpprice'] = fin['Price']*fin['change(%)']
    fin['Price'] = fin['Price']*fin['change(%)']
    fin['Price'] = fin['newpprice']
    fin.drop('newpprice',axis=1,inplace=True)

    final = fin.iloc[1:,[0,1,2,4]]
    final.index = final.date
    final.drop(['date'],axis=1,inplace=True)

    return final