import pandas as pd
import time
from Get_Bitcoin import get_bitcoin_df
from Get_Commodities import get_commodities_df

valor_bitcoin = get_bitcoin_df()
valor_commodities = get_commodities_df()

while True:
    df = pd.concat([valor_bitcoin,valor_commodities],ignore_index=True)
    print(df)
    time.sleep(60) #Espera 60 segundos antes de coletar novamente