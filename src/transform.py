# imports
import pandas as pd


def padronizar_estado(df):
    df['estado'] = df['estado'].str.strip().str.upper()
    df.loc[df['estado'] == 'PERNAMBUCO', 'estado'] = 'PE'

def padronizar_metodo_pagamento(df):
    df['metodo_pagamento'] = df['metodo_pagamento'].str.strip().str.capitalize()
    df.loc[df['metodo_pagamento'] == 'Cartão', 'metodo_pagamento'] = 'Cartao'

def padronizar_produto(df):
    df['produto'] = df['produto'].str.strip()
    df.loc[df['produto'] == 'mouse gamer', 'produto'] = 'Mouse Gamer'
    df.loc[(df['produto'] == 'HEADSET USB') | (df['produto'] == 'Headset Usb'), 'produto'] = 'Headset USB'
    df.loc[df['produto'] == 'Webcam full hd', 'produto'] = 'Webcam Full HD'

def padronizar_categoria(df):
    df['categoria'] = df['categoria'].str.strip().str.capitalize()
    df.loc[df['categoria'] == 'Periféricos', 'categoria'] = 'Perifericos'
    df.loc[df['categoria'] == 'Acessórios', 'categoria'] = 'Acessorios'

def padronizar_data_venda(df):
    mascara_ano_primeiro = df['data_venda'].str.match(r'^\d{4}')

    datas = pd.Series(pd.NaT, index=df.index, dtype='datetime64[ns]')

    datas.loc[mascara_ano_primeiro] = pd.to_datetime(
        df.loc[mascara_ano_primeiro, 'data_venda']
        .str.replace('/', '-', regex=False),
        format='%Y-%m-%d',
        errors='coerce'
    )

    mascara_dia_primeiro = ~mascara_ano_primeiro

    datas.loc[mascara_dia_primeiro] = pd.to_datetime(
        df.loc[mascara_dia_primeiro, 'data_venda']
        .str.replace('/', '-', regex=False),
        format='%d-%m-%Y',
        errors='coerce'
    )

    df['data_venda'] = datas

def remover_duplicatas(df):
    qtd_antes = len(df)

    df.drop_duplicates(subset=['id_venda'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)

    qtd_duplicadas = qtd_antes - len(df)
    print(f"Quantidade de duplicatas removidas: {qtd_duplicadas}")

def remover_nulos(df):
    qtd_antes = len(df)
    df.dropna(subset=['quantidade', 'preco_unitario'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    qtd_removida = qtd_antes - len(df)
    print(f"Quantidade de linhas removidas devido a valores nulos: {qtd_removida}")

def transform_type(df):
    df['quantidade'] = df['quantidade'].astype(int)
    df['preco_unitario'] = df['preco_unitario'].astype(float)

def transform_df(df):
    padronizar_estado(df)
    padronizar_metodo_pagamento(df)
    padronizar_produto(df)
    padronizar_categoria(df)
    padronizar_data_venda(df)
    remover_duplicatas(df)
    remover_nulos(df)
    transform_type(df)

    return df

def check_validation(df):

    # ID_VENDA
    if df['id_venda'].duplicated().any():
        print("Existem duplicatas na coluna 'id_venda'.")
    elif df['id_venda'].isnull().any():
        print("Existem valores nulos na coluna 'id_venda'.")
    else:
        print("Não existem duplicatas ou valores nulos na coluna 'id_venda'. ✅")

    # PRODUTO
    if df['produto'].isnull().any() or df['produto'].eq('').any():
        print("Existem valores nulos ou vazios na coluna 'produto'.")
    else:
        print("Não existem valores nulos ou vazios na coluna 'produto'. ✅")

    # QUANTIDADE
    if df['quantidade'].isnull().any():
        print("Existem valores nulos na coluna 'quantidade'.")
    elif (df['quantidade'] <= 0).any():
        print("Existem valores zero ou negativos na coluna 'quantidade'.")
    elif (df['quantidade'] % 1 != 0).any():
        print("Existem valores não inteiros na coluna 'quantidade'.")
    else:
        print("Todos os valores de 'quantidade' são inteiros positivos e não nulos. ✅")

    # PRECO UNITARIO
    if not pd.api.types.is_numeric_dtype(df['preco_unitario']):
        print("Existem valores não numéricos na coluna 'preco_unitario'.")
    elif df['preco_unitario'].isnull().any():
        print("Existem valores nulos na coluna 'preco_unitario'.")
    elif (df['preco_unitario'] <= 0).any():
        print("Existem valores zero ou negativos na coluna 'preco_unitario'.")
    else:
        print("Todos os valores de 'preco_unitario' são números positivos e não nulos. ✅")

    # DATA VENDA
    if not pd.api.types.is_datetime64_any_dtype(df['data_venda']):
        print("A coluna 'data_venda' não está no formato datetime.")
    elif df['data_venda'].isnull().any():
        print("Existem datas inválidas ou nulas na coluna 'data_venda'.")
    else:
        print("A coluna 'data_venda' está no formato correto e não possui datas inválidas. ✅")

if __name__ == "__main__":

    df = pd.read_csv('../data/bronze/todos_csv.csv')
    df = transform_df(df)
    df.to_csv('../data/silver/todos_csv_transformado.csv', index=False)


