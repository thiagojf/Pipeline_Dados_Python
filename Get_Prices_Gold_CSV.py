# Carregamento (Load) — Camada Gold

import pandas as pd
from pathlib import Path
import re

# ----------------------
# Função para limpar valores monetários e converter em float
# ----------------------
def clean_currency_to_float(x):
    if pd.isna(x):
        return 0.0
    x_clean = re.sub(r"[^\d.]", "", str(x))  # Remove tudo que não for dígito ou ponto
    try:
        return float(x_clean)
    except ValueError:
        return 0.0

# ----------------------
# Caminhos dos arquivos
# ----------------------
CSV_SILVER_DATA = Path(".") / "Database" / "2_Silver" / "GET_PRICES_SILVER_DATA.csv"
CSV_SILVER_SALES = Path(".") / "Database" / "2_Silver" / "silver_sales_unificado.csv"
CSV_GOLD = Path(".") / "Database" / "3_Gold" / "GET_PRICES_GOLD_DATA.csv"

# ----------------------
# Carregando os dados
# ----------------------
df_prices = pd.read_csv(CSV_SILVER_DATA, delimiter=",")
df_sales = pd.read_csv(CSV_SILVER_SALES, delimiter=",")

# ----------------------
# Garantir que a chave de merge esteja no mesmo formato (remover timezone se existir)
# ----------------------
df_prices["data_hora_trunc"] = pd.to_datetime(df_prices["data_hora_trunc"]).dt.tz_localize(None)
df_sales["data_hora_trunc"] = pd.to_datetime(df_sales["data_hora_trunc"]).dt.tz_localize(None)

# ----------------------
# Merge das tabelas
# ----------------------
merged_df = pd.merge(
    df_prices, df_sales,
    on="data_hora_trunc",
    how="inner"
)

# ----------------------
# Converter preços para float de forma segura
# ----------------------
merged_df["preco_usd_num"] = merged_df["preco_usd"].apply(clean_currency_to_float)
merged_df["preco_brl_num"] = merged_df["preco_brl"].apply(clean_currency_to_float)

# ----------------------
# Criar os totais
# ----------------------
merged_df["Total_usd"] = merged_df["quantidade"] * merged_df["preco_usd_num"]
merged_df["Total_brl"] = merged_df["quantidade"] * merged_df["preco_brl_num"]

# ----------------------
# Formatar os totais para exibição
# ----------------------
merged_df["total_usd_$"] = merged_df["Total_usd"].apply(lambda x: f"{x:,.2f}")
merged_df["total_brl_R$"] = merged_df["Total_brl"].apply(lambda x: f"{x:,.2f}")

# ----------------------
# Formatar data_hora para exibição
# ----------------------
merged_df["data_hora"] = pd.to_datetime(merged_df["data_hora"]).dt.strftime("%d/%m/%Y %H:%M:%S")

# ----------------------
# Seleção e ordem das colunas finais
# ----------------------
colunas_final = [
    "produto",
    "transaction_id",
    "quantidade", 
    "tipo_operacao", 
    "cliente_id", 
    "data_hora",
    "preco_usd", 
    "preco_brl",
    "total_usd_$",
    "total_brl_R$"
]

merged_df_final = merged_df[colunas_final]

# ----------------------
# Salvar camada GOLD
# ----------------------
merged_df_final.to_csv(CSV_GOLD, index=False)
print("✅ Camada GOLD gerada com sucesso!")