import requests
from datetime import datetime
import pandas as pd

#URL API BITCOIN
url = "https://api.coinbase.com/v2/prices/spot"

# Requisição GET para API
response = requests.get(url)
#print (response.json())
data = response.json()

# Extração dos dados 
preco = float(data['data']['amount'])
ativo = data['data']['base']
moeda = data['data']['currency']
hora_request =  datetime.now()


df = pd.DataFrame([{
    'preco' : preco,
    'ativo' : ativo,
    'moeda' : moeda,
    'hora_request' :  hora_request
}])

# CSV
#df.to_csv('price_biticoin.csv', mode='a',header=False,index=False)

# PARQUET
#df.to_parquet('price_biticoin_Parquet.parquet')

