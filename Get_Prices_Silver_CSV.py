import pandas as pd
import time as dt

# Carregando os dados da camada Bronze para transformação
bronze_data = pd.read_csv('GET_PRICES_BRONZE_DATA.csv', delimiter = ',')

# Carregar o ficheiro CSV para um DataFrame
df = bronze_data

# 🔹 Converter preco para float (mesmo que já pareça número)
df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

# 🔹 Formatando data/hora
df["horario_coleta"] = pd.to_datetime(df["horario_coleta"]).dt.strftime("%d/%m/%Y %H:%M:%S")

# 🔹 Preço em USD formatado
df["preco_usd"] = df["preco"].map(lambda x: f"${x:,.2f}")

# 🔹 Conversão para BRL
cotacao_usd_brl = 5.50
df["preco_brl"] = df["preco"].map(lambda x: f"R${x * cotacao_usd_brl:,.2f}")

#Corrige a ordem correta dos campos
df_final = df[["ativo", "preco_usd", "preco_brl", "horario_coleta"]]

 # Salva (append com cabeçalho)
CSV_PATH = "GET_PRICES_SILVER_DATA.csv"
df_final.to_csv(CSV_PATH, mode="a", header=True, index=False)

print("✅ Cotações inseridas no banco com sucesso!")