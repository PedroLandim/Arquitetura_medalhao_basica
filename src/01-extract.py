# imports
import pandas as pd

# extração de dados
def extract_data_from_data():
    todos_df = []

    dia_inicial = 10
    for dia in range(dia_inicial, 31):
        try:
            df = pd.read_csv(f'../data/vendas_2026_08_{dia}.csv')
            todos_df.append(df)
        except FileNotFoundError:
            continue

    return pd.concat(todos_df, ignore_index=True)

if __name__ == "__main__":
    df = extract_data_from_data()
    print(df.head())
    print(df.info())
    print(df.isnull().sum())
    print(df['estado'].unique())
    print(df['metodo_pagamento'].unique())
    print(df['produto'].unique())
    print(df['data_venda'].unique())
