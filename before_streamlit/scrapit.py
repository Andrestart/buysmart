from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")

opciones=Options()
opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False 
opciones.add_argument('--start-maximized')
opciones.add_argument('--incognito')     

def scrap():
    supermarket = input("Type the supermarket to scrap from ('dia', 'carrefour' or 'eroski') or 'every super' to scrap them all >>>>>  \n")
    warnings.filterwarnings("ignore")

    data = pd.read_csv("../mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)

    foods = sorted(list(set(data['product'])))    
    driver = "../driver/chromedriver.exe"
    driver = webdriver.Chrome(driver, options=opciones)
    prices = []
    prod = []
    sup = []
    links = []
    names = []
    newprice = []
    frame = {}

    for f in foods:
        if supermarket == 'carrefour':
            print(f"SCRAPPING {f} from {supermarket}...")
            for i in range(2,4):
                url = f"https://www.carrefour.es/?q={f}&page={i}"
                driver.get(url)
                time.sleep(0.3)
                try: #cookies
                    driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()
                    time.sleep(0.7)
                except:
                    pass
                    for o in range(1,50): #price, scroll, product, supermarket, link and name
                        try:

                            prices.append(driver.find_element_by_css_selector(f'#ebx-grid > article:nth-child({o}) > div > span').text.split("€")[0])
                            driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
                            prod.append(f)
                            sup.append(supermarket)
                            links.append(url)
                            names.append(driver.find_element_by_css_selector(f'#ebx-grid > article:nth-child({o}) > div > a.ebx-result-link.ebx-result__title-link.track-click > h1').text)
                        except:
                            prices.append(np.nan)
                            prod.append(f)
                            sup.append(supermarket)
                            links.append(np.nan)
                            names.append(np.nan)

        elif supermarket == 'dia':
            url = f"https://www.dia.es/compra-online/search?text={f}&x=0&y=0"
            driver.get(url)
            time.sleep(1)
            try: #cookies
                driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()
            except:
                pass
            print(f"SCRAPPING {f} from {supermarket}...")
            time.sleep(.5)
            for i in range(1,15):
                try:
                    prices.append(driver.find_element_by_css_selector(f'#productgridcontainer > div.product-list--row > div:nth-child({i}) > div > a > div.column-right > div > p.pricePerKilogram').text.split("€")[0].strip())
                    names.append(driver.find_element_by_css_selector(f'#productgridcontainer > div.product-list--row > div:nth-child({i}) > div > a > div.column-right > span').text)
                    prod.append(f)
                    sup.append(supermarket)
                    links.append(url)
                except:
                    prices.append(np.nan)
                    prod.append(f)
                    sup.append(supermarket)
                    links.append(np.nan)
                    names.append(np.nan)

        elif supermarket == 'eroski':
            url = f"https://supermercado.eroski.es/es/search/results/?q={f}&suggestionsFilter=false"
            driver.get(url)
            time.sleep(1)
            try: #cookies
                driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()
            except:
                pass
            time.sleep(.7)
            print(f"SCRAPPING {f} from {supermarket}...")
            for i in range(1,15):
                try:
                    prices.append(driver.find_element_by_css_selector(f'div.product-item-lineal:nth-child({i}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > p:nth-child(1) > span:nth-child(2)').text)
                except:
                    try:
                        prices.append(driver.find_element_by_css_selector(f'div.product-item-lineal:nth-child({i+1}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(3) > div:nth-child(2) > span:nth-child(2) > span:nth-child(2)').text)
                    except:
                        prices.append(np.nan)
                try:
                    names.append(driver.find_element_by_css_selector(f'#productListZone > div:nth-child({i+1}) > div > div.product-description > div.description-text > h2:nth-child(3) > a').text)
                except:
                    names.append(np.nan)
                prod.append(f)
                sup.append(supermarket)
                links.append(url)


        else:
            print(f"{supermarket} is not in the scrapping list")
    
    frame['price'] = prices
    frame['product'] = prod
    frame['supermarket'] = sup
    frame['link'] = links
    frame['name'] = names

    scrap = pd.DataFrame(frame)
    for i, row in scrap.iterrows():
        if row['price'] == '':
            newprice.append(np.nan)
        else:
            newprice.append(row['price'])

    scrap['price'] = newprice
    scrap.dropna(how='any',inplace=True)
    scrap['price'] = [float((i.replace(",",".").replace("€","").strip())) for i in scrap['price']]
    scrap['name'] = [(i.replace("%","por ciento").strip()) for i in scrap['name']]


    if not os.path.exists(f"../mydata/scraps_{supermarket}"):
        os.makedirs(f"../mydata/scraps_{supermarket}")
    now = str(datetime.now())[:19].replace(":","_")
    scrap.to_csv(f'../mydata/scraps_{supermarket}/{now}.csv', index=False)
    scrap.to_csv(f'../mydata/scraps_{supermarket}/scrap.csv', index=False)
    return print(f"""{supermarket.capitalize()} has been correctly scrapped. NOW it's time to change your environment to predict the prices. Use one that contains fbprophet and run 'predict.py'""")

def scrapall():
    warnings.filterwarnings("ignore")

    data = pd.read_csv("../mydata/cleandata/data.csv")
    data.index=data.date
    data.drop('date',axis=1,inplace=True)

    foods = sorted(list(set(data['product'])))    
    driver = "../driver/chromedriver.exe"
    driver = webdriver.Chrome(driver, options=opciones)

    # prices = []
    # prod = []
    # sup = []
    # links = []
    # names = []
    # newprice = []
    # frame = {}
    # for f in foods:
    #     supermarket = 'carrefour'
    #     print(f"SCRAPPING {f} from {supermarket}...(1/3)")
    #     for i in range(2,4):
    #         url = f"https://www.carrefour.es/?q={f}&page={i}"
    #         driver.get(url)
    #         time.sleep(0.3)
    #         try: #cookies
    #             driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()
    #             time.sleep(0.7)
    #         except:
    #             pass
    #         for o in range(1,50): #price, scroll, product, supermarket, link and name
    #             try:
    #                 prices.append(driver.find_element_by_css_selector(f'#ebx-grid > article:nth-child({o}) > div > span').text.split("€")[0])
    #                 driver.execute_script("window.scrollTo(0, window.scrollY + 300)")
    #                 prod.append(f)
    #                 sup.append(supermarket)
    #                 links.append(url)
    #                 names.append(driver.find_element_by_css_selector(f'#ebx-grid > article:nth-child({o}) > div > a.ebx-result-link.ebx-result__title-link.track-click > h1').text)
    #             except:
    #                 prices.append(np.nan)
    #                 prod.append(f)
    #                 sup.append(supermarket)
    #                 links.append(np.nan)
    #                 names.append(np.nan)
    # print("prices",len(prices))
    # print("prod", len(prod))
    # print("links", len(links))
    # print("sup", len(sup))
    # print(f"names", len(names))


    # frame['price'] = prices
    # frame['product'] = prod
    # frame['supermarket'] = sup
    # frame['link'] = links
    # frame['name'] = names

    # scrap = pd.DataFrame(frame)
    # for i, row in scrap.iterrows():
    #     if row['price'] == '':
    #         newprice.append(np.nan)
    #     else:
    #         newprice.append(row['price'])

    # scrap['price'] = newprice
    # scrap.dropna(how='any',inplace=True)
    # scrap['price'] = [float((i.replace(",",".").replace("€","").strip())) for i in scrap['price']]
    # scrap['name'] = [(i.replace("%","por ciento").strip()) for i in scrap['name']]


    # if not os.path.exists(f"../mydata/scraps_{supermarket}"):
    #     os.makedirs(f"../mydata/scraps_{supermarket}")
    # now = str(datetime.now())[:19].replace(":","_")
    # scrap.to_csv(f'../mydata/scraps_{supermarket}/{now}.csv', index=False)
    # scrap.to_csv(f'../mydata/scraps_{supermarket}/scrap.csv', index=False)
    # print(f"I have saved the scrap from {supermarket}")


    prices = []
    prod = []
    sup = []
    links = []
    names = []
    newprice = []
    frame = {}
    for f in foods:
        supermarket = 'dia'
        url = f"https://www.dia.es/compra-online/search?text={f}&x=0&y=0"
        driver.get(url)
        time.sleep(3)
        try: #cookies
            driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()
        except:
            pass
        print(f"SCRAPPING {f} from dia (2/3)...")
        time.sleep(.5)
        for i in range(1,15):
            try:
                prices.append(driver.find_element_by_css_selector(f'#productgridcontainer > div.product-list--row > div:nth-child({i}) > div > a > div.column-right > div > p.pricePerKilogram').text.split("€")[0].strip())
                names.append(driver.find_element_by_css_selector(f'#productgridcontainer > div.product-list--row > div:nth-child({i}) > div > a > div.column-right > span').text)
                prod.append(f)
                sup.append(supermarket)
                links.append(url)
            except:
                prices.append(np.nan)
                prod.append(f)
                sup.append(supermarket)
                links.append(np.nan)
                names.append(np.nan)
    print("prices",len(prices))
    print("prod", len(prod))
    print("links", len(links))
    print("sup", len(sup))
    print(f"names", len(names))

    frame['price'] = prices
    frame['product'] = prod
    frame['supermarket'] = sup
    frame['link'] = links
    frame['name'] = names

    scrap = pd.DataFrame(frame)
    for i, row in scrap.iterrows():
        if row['price'] == '':
            newprice.append(np.nan)
        else:
            newprice.append(row['price'])

    scrap['price'] = newprice
    scrap.dropna(how='any',inplace=True)
    scrap['price'] = [float((i.replace(",",".").replace("€","").strip())) for i in scrap['price']]
    scrap['name'] = [(i.replace("%","por ciento").strip()) for i in scrap['name']]


    if not os.path.exists(f"../mydata/scraps_{supermarket}"):
        os.makedirs(f"../mydata/scraps_{supermarket}")
    now = str(datetime.now())[:19].replace(":","_")
    scrap.to_csv(f'../mydata/scraps_{supermarket}/{now}.csv', index=False)
    scrap.to_csv(f'../mydata/scraps_{supermarket}/scrap.csv', index=False)
    print(f"I have saved the scrap from {supermarket}")


    prices = []
    prod = []
    sup = []
    links = []
    names = []
    newprice = []
    frame = {}
    for f in foods:
        supermarket = 'eroski'
        url = f"https://supermercado.eroski.es/es/search/results/?q={f}&suggestionsFilter=false"
        driver.get(url)
        time.sleep(1)
        try: #cookies
            driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()
        except:
            pass
        time.sleep(.7)
        print(f"SCRAPPING {f} from eroski (3/3)...\n\n")
        for i in range(1,15):
            try:
                prices.append(driver.find_element_by_css_selector(f'div.product-item-lineal:nth-child({i}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > p:nth-child(1) > span:nth-child(2)').text)
            except:
                try:
                    prices.append(driver.find_element_by_css_selector(f'div.product-item-lineal:nth-child({i+1}) > div:nth-child(1) > div:nth-child(3) > div:nth-child(3) > div:nth-child(2) > span:nth-child(2) > span:nth-child(2)').text)
                except:
                    prices.append(np.nan)
            try:
                names.append(driver.find_element_by_css_selector(f'#productListZone > div:nth-child({i+1}) > div > div.product-description > div.description-text > h2:nth-child(3) > a').text)
            except:
                names.append(np.nan)
            prod.append(f)
            sup.append(supermarket)
            links.append(url)
    
    print(f"I have saved the scrap from {supermarket}")
    return print(f"""All scrappings have been correctly saved. NOW it's time to change your environment to predict the prices. Use one that contains fbprophet and run 'predict.py'""")
scrapall()