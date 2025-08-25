#!/bin/bash
# run.sh - Orquestração do pipeline ETL Bitcoin & Commodities

echo "🚀 Iniciando pipeline ETL..."

# 1. Coletar Bronze
echo "1️⃣ Coletando dados Bronze..."
python Get_Prices_Bronze_CSV.py

# 2. Transformar para Silver
echo "2️⃣ Transformando para Silver..."
python Get_Prices_Silver_CSV.py

# 3. Gerar Gold
echo "3️⃣ Gerando dados Gold..."
python Get_Prices_Gold_CSV.py

# 4. Gerar Relatório Data Quality (opcional)
echo "4️⃣ Gerando relatórios de Data Quality..."
python data_quality_report.py

echo "✅ Pipeline concluído!"