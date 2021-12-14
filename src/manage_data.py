import pandas as pd
def product():
    data = pd.read_csv("mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)
    foods = sorted(list(set(data['product'])))
    foods.insert(0,'Choose')
    return list(foods)