import yfinance as yf
import pandas as pd
from datetime import datetime

def get_commodities_df():
    # Define o ticker
    ticker_symbol = ["GC=F","CL=F","SI=F"]

    dfs= []
    for sym in ticker_symbol:

        # Obtenha dados históricos de mercado dos últimos 30 dias
        historical_data = yf.Ticker(sym).history(period="1d", interval="1m")[['Close']].tail(1)
        historical_data = historical_data.rename(columns={'Close': 'preco'})
        historical_data['ativo'] = sym
        historical_data['moeda'] = 'USD'
        historical_data['hora_request'] = datetime.now()
        historical_data_Final = historical_data[['preco','ativo','moeda','hora_request']]
        dfs.append(historical_data_Final)

    return pd.concat(dfs, ignore_index=True)