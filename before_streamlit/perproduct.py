import pandas as pd
import os
import warnings

def toprophet():
    warnings.filterwarnings("ignore")
    data = pd.read_csv("../mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)
    foods = sorted(list(set(data['product'])))
    for food in foods:
        fooddicc = {}
        date = []
        price = []
        for i, row in data.iterrows():
            if row['product'] == f'{food}':
                date.append(i)
                price.append(row['price'])

            fooddicc['product'] = f'{food}'
            fooddicc['ds'] = date
            fooddicc['y'] = price
        foodframe = pd.DataFrame(fooddicc)
        foodframe.drop(['product'], axis=1, inplace=True) # Deleting columns product and date to prepare them to plot a graph
        
        groupframe = pd.DataFrame(foodframe.groupby(foodframe.ds)["y"].mean()) # Some dates are repeated, so I group by date
        groupframe.sort_values(by='ds')
        groupframe = groupframe.reset_index()
        groupframe ['ds'] = pd.to_datetime(groupframe.ds)
        
        prophet = groupframe
        if not os.path.exists("../mydata/per_item/for_prophet"):
            os.makedirs("../mydata/per_item/for_prophet")
        prophet.to_csv(f"../mydata/per_item/for_prophet/prophet_{food}.csv",index=False)
        print(f"I saved {food}")
    return print("All good. The information for every product has been saved in '../mydata/per_item/for_prophet/'\n Now you can run 'scrapit.py' to scrap the products from the supermarkets you choose")
toprophet()