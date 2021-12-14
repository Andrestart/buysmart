from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os
import warnings
warnings.filterwarnings("ignore")
import shutil



def prophet():
    warnings.filterwarnings("ignore")
    data = pd.read_csv("../mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)
    foods = sorted(list(set(data['product'])))

    for i in foods:
        item = pd.read_csv(f"../mydata/per_item/for_prophet/prophet_{i}.csv")
        print(f"Predicting {i}...\n>>>>>>>>>>\n\n")
        
        if os.path.exists(f"../mydata/per_item/graphs/{i}/"):
            shutil.rmtree(f"../mydata/per_item/graphs/{i}/")
        os.makedirs(f"../mydata/per_item/graphs/{i}/")
            
        model = Prophet(weekly_seasonality=True)
        model.fit(item)
        future = model.make_future_dataframe(periods=200, freq='W')
        forecast = model.predict(future)
        if not os.path.exists(f"../mydata/per_item/forecasts/"):
            os.makedirs(f"../mydata/per_item/forecasts/")
        forecast.to_csv(f"../mydata/per_item/forecasts/{i}.csv",index=False)

        fig3in1 = model.plot_components(forecast).savefig(f"../mydata/per_item/graphs/{i}/{i}_3in1.png")
        figchange = model.plot(forecast)
        a = add_changepoints_to_plot(figchange.gca(), model, forecast)
        figchange = model.plot(forecast).savefig(f"../mydata/per_item/graphs/{i}/{i}_figchange.png")
        print(f"\n\n{i.capitalize()} prices predicted")
    return print(f"""\n\nALL PREDICTIONS ARE WELL SAVED IN YOUR PC :)\n Now it's time to create a database and save them all in the SQL Server.
    \n Change your environment to the one you used before the predictions and run 'sql.py' to save them""")

prophet()