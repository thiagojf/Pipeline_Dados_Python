import pandas as pd
import time
from sqlalchemy import create_engine
from Get_Bitcoin import get_bitcoin_df
from Get_Commodities import get_commodities_df
from dotenv import load_dotenv
import os

#carrega variaveis do .env
load_dotenv()

# Configuração do banco (substituir com seus dados reais)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Criar conexão SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

valor_bitcoin = get_bitcoin_df()
valor_commodities = get_commodities_df()

SLEEP_SECONDS = 60

while True:
    df = pd.concat([valor_bitcoin,valor_commodities],ignore_index=True)
    
    # Salva no banco (append)
    df.to_sql("cotacoes", engine, if_exists="append", index=False)

    print("✅ Cotações inseridas no banco com sucesso!")

    time.sleep(SLEEP_SECONDS) #Espera 60 segundos antes de coletar novamente