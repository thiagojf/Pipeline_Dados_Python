# Projeto de Coleta de Cotações — Fast Track Engenharia de dados

Este projeto faz parte da **Fast Track Engenharia de dados** e tem como objetivo coletar, consolidar e salvar cotações em tempo real de **Bitcoin** e de **commodities** selecionadas, utilizando APIs públicas e a biblioteca `yfinance`.

## 📂 Estrutura do Projeto
project/
├── Database/
│ ├── 1_Bronze/
│ ├── 2_Silver/
│ └── 3_Gold/
├── Get_Bitcoin.py
├── Get_Commodities.py
├── Get_Prices_Bronze_CSV.py
├── Get_Prices_Silver_CSV.py
├── Get_Prices_Gold_CSV.py
├── requirements.txt
└── README.md
---

## 📂 Estrutura do Projeto

### **Get_Bitcoin.py**

* Script responsável por coletar a **cotação atual do Bitcoin** em USD.
* Fonte: API pública da **Coinbase**.
* Retorna um **DataFrame padronizado** com as colunas:

  * `ativo` — símbolo do ativo (`BTC-USD`)
  * `preco` — preço atual
  * `moeda` — moeda de cotação (USD)
  * `horario_coleta` — horário local da coleta
* Pode ser executado de forma independente (`python Get_Bitcoin.py`) para teste.

---

### **Get_Commodities.py**

* Script responsável por coletar a **última cotação** de commodities em USD.
* Fonte: **Yahoo Finance** via biblioteca `yfinance`.
* Lista de ativos incluídos por padrão:

  * `GC=F` — Ouro
  * `CL=F` — Petróleo WTI
  * `SI=F` — Prata

* Retorna um **DataFrame padronizado** com as colunas:

  * `ativo` — símbolo do ativo
  * `preco` — preço atual
  * `moeda` — moeda de cotação (USD)
  * `horario_coleta` — horário local da coleta
* Pode ser executado de forma independente (`python Get_Commodities.py`) para teste.

---

### **Get_Prices_Bronze_CSV.py**

* Script orquestrador que combina os resultados de **GetBitcoin** e **GetCommodities**.
* Três variações disponíveis:

  1. **Execução única** — junta e imprime o DataFrame e escreve cabeçalho apenas uma vez.
  2. **Loop** — coleta dos dados a cada 3600 segundos.
  3. **salva/append** em um arquivo CSV consolidado (`GET_PRICES_BRONZE_DATA.csv`).

### **Lista de camadas** 

  1. **1_Bronze**: dados brutos coletados (API Bitcoin, Yahoo Finance, Sales CSVs)
  2. **2_Silver**: dados tratados e formatados (preço em USD/BRL, data truncada)
  3. **3_Gold**: dados consolidados prontos para análise (merge vendas × preços, totais calculados)


---
## 📊 Relatório de Data Quality (DQ)

O projeto inclui um script para geração de **relatórios de qualidade dos dados**, garantindo que os dados das camadas **Silver** e **Gold** estejam consistentes antes de análises.

### Como gerar o relatório:

1. Execute o script:

python data_quality_report.py

2. Os relatórios serão gerados na pasta: Database/4_Reports/\

3. Cada relatório contém:

Tipo de dados de cada coluna\
Número de valores nulos\
Número de duplicados\
Estatísticas básicas (mínimo, máximo, média, desvio padrão) para colunas numéricas\

---

### Como Executar

1. Instalar dependências\
pip install -r requirements.txt

2. Coletar dados brutos (Bronze)\
python Get_Prices_Bronze_CSV.py

3. Transformar dados para Silver\
python Get_Prices_Silver_CSV.py

4. Gerar dados consolidados Gold\
python Get_Prices_Gold_CSV.py

---

## **🚫 Arquivos Ignorados pelo Git**

O projeto inclui um arquivo **`.gitignore`** para evitar que arquivos temporários, dados brutos ou informações sensíveis sejam versionados.  

Principais regras:

- **Sistemas operacionais:** `.DS_Store`, `Thumbs.db`  
- **Python:** `__pycache__/`, arquivos `.pyc`, `.env`  
- **Jupyter:** `/Notebooks_Desenv/`  
- **Logs:** arquivos `.log` ou `.out`  
- **Configurações de IDE:** `.vscode/`, `.idea/`, `.sublime-*`  

Isso mantém o repositório limpo e seguro.

---
### **Notas** 

Todas as datas em UTC e truncadas por hora para facilitar o merge.
Preços em USD e BRL, com colunas numéricas para cálculos e colunas formatadas para visualização.
O pipeline está modularizado em scripts separados para facilitar manutenção e extensibilidade.