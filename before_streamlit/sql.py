import sys
sys.path.append("../")
import config.sqlconfig as c
import os
import pandas as pd

supermarket = input("Write here the supermarket you want to insert scrapped values from ('dia', 'carrefour' or 'eroski' or 'all' for all the supermarkets\n\n")

def check(string):
    """
    This funtion checks if the product returning True if it does or False if it doesn't.
    """
    query = list(c.engine.execute(f"SELECT `nameproduct` FROM `product` WHERE `nameproduct` = '{string}'"))
    if len(query) > 0:
        return True
    else:
        return False

def giveid(prodname):
    """
    It returns the product ID from a product name.
    """
    try:
        e = list(c.engine.execute(f"SELECT `idproduct` FROM `product` WHERE `nameproduct` ='{prodname}';"))[0][0]
    except:
        print(f"I can't add {prodname}")
        e = "unknown"
    return e

def deletescrap():
    if supermarket == 'all':
        try:
            c.engine.execute(f"""TRUNCATE `dia`;""")
        except:
            pass
        try:
            c.engine.execute(f"""TRUNCATE `carrefour`;""")
        except:
            pass
        try:
            c.engine.execute(f"""TRUNCATE `eroski`;""")
        except:
            pass
    else:
        try:
            c.engine.execute(f"""TRUNCATE `{supermarket}`;""")
        except:
            pass


    return print("All scraps previously saved have been deleted")

def deleteproducts():
    try:
        c.engine.execute(f"""DROP TABLE `product`;""")
    except:
        pass
    return print("All products previously saved have been deleted")

def insertproducts():
    """
    First it checks if the product is in the database using the function "check", and if it's not, it inserts the product.
    """
    try:
        c.engine.execute(f"""CREATE TABLE `product`;""")
    except:
        pass
    data = pd.read_csv("../mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)
    foods = sorted(list(set(data['product'])))
    for f in foods:
        if check(f):
            return print(f"{f} is already in your table")
        else:
            c.engine.execute(f"INSERT INTO `product` (`nameproduct`) VALUES ('{f}');")
    return print("All products have been inserted to the database")
    
def insertscrap():
    if supermarket=='all':
        supers = ['dia','carrefour','eroski']
        for superm in supers:
            scrap = pd.read_csv(f'../mydata/scraps_{superm}/scrap.csv')
            try:
                c.engine.execute(f"""TRUNCATE `{superm}`;""")
            except:
                pass
            for i, row in scrap.iterrows():
                idprod =  giveid(row['product'])
                try:
                    c.engine.execute(f"""
            INSERT INTO `{superm}` (`namescrap`, `supermarket`, `link`, `price`, `product_idproduct`) VALUES
            ("{row['name']}", "{row['supermarket']}","{row['link']}",{row['price']},{idprod})
            ;
            """)
                    print(f"I have inserted {row['name']}")
                except:
                    print(f"I can't add {row['name']}")
        print(f"\n\n\n{superm.capitalize()} scrapping has been correctly added to the database\n\n\n")


    else:
        scrap = pd.read_csv(f'../mydata/scraps_{supermarket}/scrap.csv')
        try:
            c.engine.execute(f"""TRUNCATE `{supermarket}`;""")
        except:
            pass
        for i, row in scrap.iterrows():
                idprod =  giveid(row['product'])
                try:
                    c.engine.execute(f"""
            INSERT INTO `{supermarket}` (`namescrap`, `supermarket`, `link`, `price`, `product_idproduct`) VALUES
            ("{row['name']}", "{row['supermarket']}","{row['link']}",{row['price']},{idprod})
            ;
            """)
                    print(f"I have inserted {row['name']}")
                except:
                    print(f"I can't add {row['name']}")
        print(f"\n\n\n{supermarket.capitalize()} scrapping has been correctly added to the database\n\n\n")
    return print("All scrapped information has been inserted to the database")


def deletegraphs():
    c.engine.execute(f"""TRUNCATE `graphs`;""")
    return print("All previous graphs have been deleted")

def insertgraphs():
    data = pd.read_csv("../mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)
    foods = sorted(list(set(data['product'])))
    for i in foods:
        for r in range (0,len(os.listdir(f"../mydata/per_item/graphs/{i}/"))):
            graphtype= os.listdir(f"../mydata/per_item/graphs/{i}/")[r].split('_')[1].split('.')[0]
            e = os.listdir(f"../mydata/per_item/graphs/{i}/")[r].split('_')[1].split('.')[0]
            graph = (f"../mydata/per_item/graphs/{i}/{i}_{e}.png")
            idprod =  giveid(i)

            try:
                c.engine.execute(f"""
                INSERT INTO `graphs` (`graphtype`, `graph`, `product_idproduct`) VALUES
                ("{graphtype}", "{graph}",{idprod})
                ;
                """)
            except:
                print(f"I can't add {i}")
    return print(f"All graphs have been inserted into the SQL database. Now you can run streamlit if you execute 'main.py'.")

deletescrap()
deletegraphs()
deleteproducts()
insertproducts()
insertscrap()
insertgraphs()