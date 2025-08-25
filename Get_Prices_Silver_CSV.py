#Transformação (Transform) — Camada Silver

import pandas as pd
import time as dt
from pathlib import Path

# ==============================
#  Formatando data/hora, Conversão para BRL e corrigindo a ordem correta dos campos
# ==============================

# Carregando os dados da camada Bronze para transformação
bronze_data = pd.read_csv('Database\\1_Bronze\\GET_PRICES_BRONZE_DATA.csv', delimiter = ',')

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

# Ajustar a coluna data_hora arredondando para hora
df["horario_coleta"] = pd.to_datetime(df["horario_coleta"], errors="coerce")

# Arredondar para a hora cheia (truncar minutos/segundos)
df["data_hora_trunc"] = df["horario_coleta"].dt.floor("h")

#Corrige a ordem correta dos campos
df_final = df[["ativo", "preco_usd", "preco_brl", "horario_coleta","data_hora_trunc"]]

 # Salva (append com cabeçalho)
# Caminho relativo: sobe um nível, entra na pasta Database/Bronze
df_final.to_csv("Database\\2_Silver\\GET_PRICES_SILVER_DATA.csv", mode="a", header=True, index=False)

# ==============================
# Union dos arquivos de transações bronze_sales_btc_excel.csv e bronze_sales_commodities_sql.csv
# ==============================

# 1. Definir os arquivos de entrada
btc_file = Path(".") / "Database" / "1_Bronze" / "bronze_sales_btc_excel.csv"
commodities_file = Path(".") / "Database" / "1_Bronze" / "bronze_sales_commodities_sql.csv"

# 2. Definir o arquivo de saída
output_file = Path(".") / "Database" / "2_Silver" / "silver_sales_unificado.csv"

# 3. Ler os dois arquivos CSV em DataFrames
df_btc = pd.read_csv(btc_file)
df_commodities = pd.read_csv(commodities_file)

# 4. Renomear colunas para padronizar
df_btc = df_btc.rename(columns={"ativo": "produto"})
df_commodities = df_commodities.rename(columns={"commodity_code": "produto"})

# 5. Concatenar os DataFrames
df_unificado = pd.concat([df_btc, df_commodities], ignore_index=True, sort=False)

# 6. Ajustar a coluna data_hora arredondando para hora
df_unificado["data_hora"] = pd.to_datetime(df_unificado["data_hora"], errors="coerce")

# 6.1. Arredondar para a hora cheia (truncar minutos/segundos)
df_unificado["data_hora_trunc"] = df_unificado["data_hora"].dt.floor("h")

# 7. Salvar o DataFrame unificado em um novo CSV
df_unificado.to_csv(output_file, index=False)

print("✅ Transformações executadas com sucesso!")
print(f"\n✅ Arquivo unificado gerado com sucesso!")