# Carregamento (Load) — Camada Gold

import pandas as pd
from pathlib import Path

# Caminhos
CSV_SILVER_DATA = Path(".") / "Database" / "2_Silver" / "GET_PRICES_SILVER_DATA.csv"
CSV_SILVER_SALES = Path(".") / "Database" / "2_Silver" / "silver_sales_unificado.csv"
CSV_GOLD = Path(".") / "Database" / "3_Gold" / "GET_PRICES_GOLD_DATA.csv"

# Carregando os dados da camada Silver
df_prices = pd.read_csv(CSV_SILVER_DATA, delimiter=",")
df_sales = pd.read_csv(CSV_SILVER_SALES, delimiter=",")

# Garantir que a chave está no mesmo formato (removendo timezone se existir)
df_prices["data_hora_trunc"] = pd.to_datetime(df_prices["data_hora_trunc"]).dt.tz_localize(None)
df_sales["data_hora_trunc"] = pd.to_datetime(df_sales["data_hora_trunc"]).dt.tz_localize(None)

# Merge nas tabelas
merged_df = pd.merge(
    df_prices, df_sales,
    on="data_hora_trunc",
    how="inner"
)

# Converter preco_usd para número
merged_df["preco_usd_num"] = (
    merged_df["preco_usd"]
    .replace(r'[\$,]', '', regex=True)   # raw string evita o warning
    .astype(float)
)

# Converter preco_brl para número
merged_df["preco_brl_num"] = (
    merged_df["preco_brl"]
    .replace(r'[R\$,]', '', regex=True)  # raw string
    .astype(float)
)

# Criar as colunas Total_usd e Total_brl, onde multipliquei a coluna quantide e preco_usd_num que foi formatada acima
merged_df["Total_usd"] = merged_df["quantidade"] * merged_df["preco_usd_num"]

# Criar as colunas Total_usd e Total_brl, onde multipliquei a coluna quantide e preco_brl_num que foi formatada acima
merged_df["Total_brl"] = merged_df["quantidade"] * merged_df["preco_brl_num"]

# Criar os totais formatado como moeda no próprio DataFrame:
merged_df["Total_usd"] = merged_df["Total_usd"].apply(lambda x: f"${x:,.2f}")
merged_df["Total_brl"] = merged_df["Total_brl"].apply(lambda x: f"R${x:,.2f}")

merged_df["data_hora"] = pd.to_datetime(merged_df["data_hora"]).dt.strftime("%d/%m/%Y %H:%M:%S")

# Seleção das colunas desejadas
colunas_final = [
    "produto",
    "transaction_id",
    "quantidade", 
    "tipo_operacao", 
    "cliente_id", 
    "data_hora",
    "preco_usd", 
    "preco_brl",
    "Total_usd",
    "Total_brl"
]

merged_df = merged_df[colunas_final]

# Exportar para camada GOLD
merged_df.to_csv(CSV_GOLD, index=False)

print("✅ Camada GOLD gerada com sucesso!")