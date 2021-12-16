# buysmart
Why have you done this!?

I have always been interested in economics and prices behaviour. Food prices are very variable so creating a predicting tool could be a nice challenge.

This project makes it easier to understand how food prices have been variating during last years and get a prediction for the next years.
Tools used:

    API requests.

    SQL server and SQL Workbench.

    FB prophet for timeseries predictions.

    Selenium for scrapping supermarket prices.

    Streamlit to show my graphs and data.

BUT HOW DID YOU DO IT?

I followed the following structure:

    Getting historical price data making a request to an API called Agrifood.

    Saving it into different food categories to simplify it. After cleaning my dataframe, it looked like this:

    Separating the dataframe per product and preparing it for predictions.

    Predicting the food prices per product.

    Creating a database to store my data.

    Getting today's food prices from different supermarkets (conditional scrapping).

    Making a user-friendly web to show the graphs and conclusions.

    Making the whole process executable so the end user can just run the program and get all updated information everyday without knowing how the code looks like.