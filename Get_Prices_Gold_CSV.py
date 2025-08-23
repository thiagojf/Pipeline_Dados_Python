# Carregamento (Load) — Camada Gold

import pandas as pd
import time as dt

# Carregando os dados da camada Bronze para transformação
silver_data = pd.read_csv('Database\\2_Silver\\GET_PRICES_SILVER_DATA.csv', delimiter = ',')

# Carregar o ficheiro CSV para um DataFrame
df = silver_data
df_final = df
 # Salva (append com cabeçalho)
# Caminho relativo: sobe um nível, entra na pasta Database/Bronze
#df_final.to_csv("Database\\Silver\\GET_PRICES_SILVER_DATA.csv", mode="a", header=True, index=False)

print(df_final)