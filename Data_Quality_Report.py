# data_quality_report.py
import pandas as pd
from pathlib import Path

# Caminho dos arquivos Silver
CSV_SILVER_DATA = Path("Database/2_Silver/GET_PRICES_SILVER_DATA.csv")
CSV_SILVER_SALES = Path("Database/2_Silver/silver_sales_unificado.csv")

# Função para gerar relatório de DQ
def generate_dq_report(df: pd.DataFrame, nome_arquivo: str):
    report = pd.DataFrame({
        "tipo": df.dtypes,
        "nulos": df.isnull().sum(),
        "duplicados": [df.duplicated().sum()] * df.shape[1]
    })

    # Estatísticas apenas para colunas numéricas
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        report.loc[col, "min"] = df[col].min()
        report.loc[col, "max"] = df[col].max()
        report.loc[col, "media"] = df[col].mean()
        report.loc[col, "std"] = df[col].std()

    # Salva CSV
    output_path = Path("Database/4_Reports") / f"{nome_arquivo}_dq_report.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(output_path, index=True)
    print(f"✅ Relatório DQ gerado: {output_path}")

# Carregar dados
df_prices = pd.read_csv(CSV_SILVER_DATA)
df_sales = pd.read_csv(CSV_SILVER_SALES)

# Gerar relatórios
generate_dq_report(df_prices, "GET_PRICES_SILVER_DATA")
generate_dq_report(df_sales, "silver_sales_unificado")