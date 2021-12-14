import pandas as pd
prohibido = {}

def filter (frame, prod):
    df = frame[frame['product'] == f'{prod}']
    for i,row in df.iterrows():
        if any(e in row['Name'].lower() for e in prohibido[f'{prod}']):
            df.drop(i, inplace=True)
    return df

prohibido = {'aceite de girasol':['atún','melva','anchoas','caballa','mayonesa','sardinillas','sardinas','paté','patatas','caballa','salsa','chipirones','caballa','melva','tomates','anchoa','potón','chipirones'],
'aceite de oliva':[],
'ajo':['polvo','perejil','salsa','crema','picado','sazonar','picado','troceado','polvo','perejil','panecillo','pan', 'salsa','tiras','ojos','papel'],
'albaricoque':['confitura','orejón','champú','orejones','mermelada','yogur','barritas','facial','bebida'],
'arroz':[],
'azucar':[],
'berenjena':['calabacín', 'calabaza'],
'calabacin':['crema','hamburguesas','hamburguesa', 'berenjena', 'calabaza'], 
'cebada':[],
'cebolla':['sopa','molida','frasco', 'tortilla', 'morcilla', 'sofrito', 'tomate'],
'cerdo':['cortezas', 'pate', 'paté', 'cepillo'],
'cereza':['bombón','bombones','caramelo','frutos secos'],
'champiñon':['redondo'],
'ciruela':['mermelada','sabor','té','toque','bífidus','redondo'],
'coliflor':['brócoli', 'repollo','lombarda'],
'cordero':['perros','gatos'],
'esparrago':[''],
'fresa':['yogur','batido','sirope','yogolino','mermelada','sabor','gelatina','postre','pastillas','caramelos', 'champú','golosinas'],
'harina de trigo':['pan','corteza','maizena','pipas','palitos','cerveza','tostas','tortillas'],
'judia':[],
'leche entera':[],
'leche entera organica':[],
'lechuga':['endivia'],
'limon':['refresco','fanta','schweppes','zero',],
'maiz':['palomitas','tortitas','harina'],
'malta':['leche','crema','perros'],
'mandarina':['zumo'],
'mantequilla':['palomitas','croissant','magdalenas','galletas','aperitivo'],
'manzana':['sidra','zumo','puré','refresco'],
'melocoton':['néctar','mermelada','yogur'],
'melon':['toallitas','aroma','bebuda','pelo'],
'naranja':['kas','lata','fanta','refresco'],
'nectarina':[],
'pepino':['jabón'],
'pera':[],
'pimiento':[],
'pipas de girasol':[],
'puerro':[],
'queso edam':[],
'queso emmental':[],
'sandia':[],
'suero de leche':[],
'ternera':['perros','menestra'],
'tomate':[],
'uva':[],
'vino':[],
'zanahoria':[]}