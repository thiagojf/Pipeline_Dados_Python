# GetPrices_loop_save.py
# A cada 60s: junta Bitcoin + Commodities e salva/append em um CSV.

import os
import time
import pandas as pd
from Get_Bitcoin import get_bitcoin_df
from Get_Commodities import get_commodities_df

SLEEP_SECONDS = 300
CSV_PATH = "Database\\1_Bronze\\GET_PRICES_BRONZE_DATA.csv"

if __name__ == "__main__":
    # Se quiser garantir cabeçalho na primeira execução, crie o arquivo vazio com header:
    if not os.path.exists(CSV_PATH):
        # escreve cabeçalho apenas uma vez
        cols = ["preco", "ativo", "moeda", "horario_coleta"]
        pd.DataFrame(columns=cols).to_csv(CSV_PATH, index=False)

    while True:
        # Coleta
        valor_bitcoin = get_bitcoin_df()
        valor_commodities = get_commodities_df()

        # Junta tudo
        df = pd.concat([valor_bitcoin, valor_commodities], ignore_index=True)

        # Salva (append sem cabeçalho)
        df.to_csv(CSV_PATH, mode="a", header=False, index=False)

        print("✅ Importado cotações!")
        
        # Espera próximo ciclo
        time.sleep(SLEEP_SECONDS)
