import requests
from datetime import datetime
import pandas as pd


def get_biticoin_df():
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

        return df