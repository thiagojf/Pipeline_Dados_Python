#Transformação (Transform) — Camada Silver

import pandas as pd
import time as dt

# Carregando os dados da camada Bronze para transformação
bronze_data = pd.read_csv('Database\\2_Bronze\\GET_PRICES_BRONZE_DATA.csv', delimiter = ',')

# Carregar o ficheiro CSV para um DataFrame
df = bronze_data

# 🔹 Formatando data/hora
df["horario_coleta"] = pd.to_datetime(df["horario_coleta"]).dt.strftime("%d/%m/%Y %H:%M:%S")

# 🔹 Converter preco para float (mesmo que já pareça número)
df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

# 🔹 Preço em USD formatado
df["preco_usd"] = df["preco"].map(lambda x: f"${x:,.2f}")

# 🔹 Conversão para BRL
cotacao_usd_brl = 5.50
df["preco_brl"] = df["preco"].map(lambda x: f"R${x * cotacao_usd_brl:,.2f}")

#Corrige a ordem correta dos campos
df_final = df[["ativo", "preco_usd", "preco_brl", "horario_coleta"]]

 # Salva (append com cabeçalho)
# Caminho relativo: sobe um nível, entra na pasta Database/Bronze
df_final.to_csv("Database\\Silver\\GET_PRICES_SILVER_DATA.csv", mode="a", header=True, index=False)

print("✅ Transformações executadas com sucesso!")