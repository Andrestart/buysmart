import requests
import pandas as pd
import os
import numpy as np
from datetime import datetime

API = "https://agridata.ec.europa.eu/extensions/DataPortal/API_Documentation.html"


def getmydata():
    foods = ["beef","pigmeat","sheepAndGoat","rawMilk","dairy","fruitAndVegetable","cereal","rice","oilseeds","sugar","oliveOil","wine"]

    data={}
    date = []
    price = []
    prod = []
    var = []
    veg = []
    shandgoat=[]
    print("Ok, Let's get the food prices!")

    for food in foods:
        url = f"https://www.ec.europa.eu/agrifood/api/{food}/prices?memberStateCodes=ES&beginDate=01/01/2001"
        resp = requests.get(url).json()

        for i in resp:
            try:
                date.append(i['beginDate'])
            except: #Rice doesn't have beginDate but has ym which means year month
                date.append(i['ym'])
            price.append(float(i['price'][1:].replace(",",".")))
            try:
                var.append(i['productName'])
            except:
                var.append("unknown")
            try:
                veg.append(i['product'])
            except:
                veg.append('unknown')
            try:
                shandgoat.append(i['category'])
            except:
                shandgoat.append('unknown')
            prod.append(food)

        data['product'] = prod
        data['date'] = date
        data['price'] = price
        data['variety'] = var
        data['veg'] = veg
        data['shandgoat'] = shandgoat

    print("Request made, I have the data")
    data = pd.DataFrame(data)
    data.date = pd.to_datetime(data.date)
    data.index = data.date
    data = data.sort_index()

    o = []
    for i, row in data.iterrows():
        if row['variety'] != 'unknown':
            o.append(row['variety'].replace(" ","_").lower()) 
        elif row['veg'] != 'unknown':
            o.append(row['veg'].replace(" ","_").lower())
        elif row['shandgoat']!='unknown':
            o.append(row['shandgoat'].replace(" ","_").lower())
        else:
            o.append(row['product'].replace(" ","_").lower())
    data ['product'] = o

    price = []
    for i, row in data.iterrows():
        if row['price'] != 0.00 or row['price'] != 0.0:
            price.append(row['price'])
        else:
            price.append(np.nan)
    data['price'] = price
    data.dropna(how='any',inplace=True)

    # Translating product names to simplified Spanish to use them as keywords to search later
    names = {'abricots':'albaricoque',
    'apples':'manzana',
    'asparagus':'esparrago',
    'beans':'judia',
    'beef':'ternera',
    'butter':'mantequilla',
    'cabbages':'col',
    'carrots':'zanahoria',
    'cauliflowers':'coliflor',
    'cherries':'cereza',
    'clementines':'clementina',
    'courgettes':'calabacin',
    'crude_olive-pomace_oil_(from_5_to_10%)':'aceite de orujo de oliva crudo de 5 a 10%',
    'crude_soya_bean_oil':'salsa de soja',
    'crude_sunflower_oil':'aceite de girasol',
    'cucumbers': 'pepino',
    'durum_wheat':'harina de trigo',
    'edam':'queso edam',
    'egg_plants,_aubergines':'berenjena',
    'emmental':'queso emmental',
    'extra_virgin_olive_oil_(up_to_0.8%)':'aceite de oliva',
    'feed_barley':'cebada',
    'garlic':'ajo',
    'lampante_olive_oil_(2%)':'aceite de oliva',
    'leeks':'puerro',
    'lemons':'limon',
    'lettuces':'lechuga',
    'light_lamb':'cordero',
    'maize':'maiz',
    'malting_barley':'malta',
    'mandarins':'mandarina',
    'melons':'melon',
    'milling_wheat':'harina de trigo',
    'mushrooms,_cultivated':'champiñon',
    'nectarines':'nectarina',
    'olive-pomace_oil_(up_to_1%)':'aceite de orujo de oliva (hasta 1%)',
    'onions':'cebolla',
    'oranges':'naranja',
    'organic_raw_milk':'leche entera organica',
    'peaches':'melocoton',
    'pears':'pera',
    'peppers':'pimiento',
    'pigmeat':'cerdo',
    'plums':'ciruela',
    'rapeseed':'colza',
    'raw_milk':'leche entera',
    'refined_olive-pomace_oil_(up_to_0.3%)':'aceite de orujo de oliva refinado (hasta 3%)',
    'refined_olive_oil_(up_to_0.3%)':'aceite de oliva',
    'rice':'arroz',
    'satsumas':'mandarina',
    'smp':'leche semidesnatada en polvo',
    'soya_meal':'harina de soja',
    'strawberries':'fresa',
    'sugar':'azucar',
    'sunflower_seed':'pipas de girasol',
    'sunflower_seed_meal':'harina de pipas de girasol',
    'table_grapes':'uva',
    'tomatoes':'tomate',
    'virgin_olive_oil_(up_to_2%)':'aceite de oliva',
    'water_melons':'sandia',
    'wheypowder':'suero de leche',
    'wine':'vino',
    'wmp':'leche entera en polvo'}

    #Unifying the product names and their categories
    data['product'] = data['product'].map(names)
    data.drop(['date','variety','veg','shandgoat'], axis=1, inplace=True)

    #Dropping rare products and data with less than 50 records 
    gooddata = []
    for i, row in data.iterrows():
        if row['product']=='leche entera en polvo':
            gooddata.append(np.nan)
        elif row['product']=='leche entera en polvo':
            gooddata.append(np.nan)
        elif row['product']=='leche entera organica':
            gooddata.append(np.nan)
        elif row['product']=='leche semidesnatada en polvo':
            gooddata.append(np.nan)
        elif row['product']=='aceite de orujo de oliva (hasta 1%)':
            gooddata.append(np.nan)
        elif row['product']=='aceite de orujo de oliva crudo de 5 a 10%':
            gooddata.append(np.nan)
        elif row['product']=='aceite de orujo de oliva refinado (hasta 3%)':
            gooddata.append(np.nan)    
        elif row['product']=='col':
            gooddata.append(np.nan)
        elif row['product']=='colza':
            gooddata.append(np.nan)
        elif row['product']=='harina de soja':
            gooddata.append(np.nan)
        elif row['product']=='salsa de soja':
            gooddata.append(np.nan)
        elif row['product']=='harina de pipas de girasol':
            gooddata.append(np.nan)
        elif row['product']=='clementina':
            gooddata.append(np.nan)
        elif row['product']=='cebada':
            gooddata.append(np.nan)
        elif row['product']=='nectarina':
            gooddata.append(np.nan)
        else:
            gooddata.append(row['product'])
    data['product'] = gooddata
    
    # Deleting nans created to drop those rare products
    data.dropna(how='any',inplace=True)
    
    #Saving the data
    now = str(datetime.now())[:19].replace(":","_")
    if not os.path.exists(f"../mydata/cleandata/{now}"):
        os.makedirs(f"../mydata/cleandata/{now}")
    data.to_csv(f"../mydata/cleandata/{now}/data_{now}.csv")
    data.to_csv(f"../mydata/cleandata/data.csv")

    #Saving the API response
    resp = pd.DataFrame(resp)
    if not os.path.exists(f"../data/"):
        os.makedirs(f"../data/")
    resp.to_csv(f"../data/api_raw.csv")

    return print("Food prices are saved in your PC. Now run 'perproduct.py' to get the data per product")
getmydata()

