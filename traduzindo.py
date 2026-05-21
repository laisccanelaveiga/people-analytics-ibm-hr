import pandas as pd
from deep_translator import GoogleTranslator

tradutor = GoogleTranslator(source='en', target='pt')

df = pd.read_csv('employee.csv')

# 1. Traduz os cabeçalhos (35 chamadas apenas)
colunas_traduzidas = {col: tradutor.translate(col) for col in df.columns}
df.rename(columns=colunas_traduzidas, inplace=True)

# 2. Identifica colunas de texto
colunas_texto = df.select_dtypes(include='object').columns.tolist()

# 3. Traduz apenas os valores únicos de cada coluna de texto
print("Traduzindo valores únicos... Aguarde")

for coluna in colunas_texto:
    valores_unicos = df[coluna].dropna().unique().tolist()
    
    dicionario = {}
    for valor in valores_unicos:
        try:
            dicionario[valor] = tradutor.translate(str(valor))
        except Exception:
            dicionario[valor] = valor  # mantém original se falhar
    
    # 4. Aplica o mapeamento no DataFrame inteiro de uma vez
    df[coluna] = df[coluna].map(dicionario)

df.to_csv('bancotraduzido.csv', index=False)
print("Arquivo traduzido e salvo com sucesso!")
