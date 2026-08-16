import pandas as pd
from sqlalchemy import create_engine

def faturamento_diario(df):
    df['faturamento'] = df['quantidade'] * df['preco_unitario']
    faturamento_diario = df.groupby('data_venda')['faturamento'].sum().reset_index()
    faturamento_diario.rename(columns={'faturamento': 'faturamento_total'}, inplace=True)
    return faturamento_diario

def venda_produto(df):
    df['faturamento'] = df['quantidade'] * df['preco_unitario']
    faturamento_produto = df.groupby('produto')['faturamento'].sum().reset_index()
    faturamento_produto.rename(columns={'faturamento': 'venda_por_produto'}, inplace=True)
    faturamento_produto['venda_por_produto'] = (faturamento_produto['venda_por_produto'].round(2))
    return faturamento_produto

def vendas_categoria(df):
    df['faturamento'] = df['quantidade'] * df['preco_unitario']
    vendas_categoria = df.groupby('categoria')['faturamento'].sum().reset_index()
    vendas_categoria.rename(columns={'faturamento': 'vendas_por_categoria'}, inplace=True)
    return vendas_categoria

def create_engine_db():
    engine = create_engine('sqlite:///../data/gold/database.db')
    return engine

def load_df(df):
    engine = create_engine_db()

    faturamento_diario_df = faturamento_diario(df)
    vendas_categoria_df = vendas_categoria(df)
    venda_produto_df = venda_produto(df)

    faturamento_diario_df.to_sql(
        'faturamento_diario',
        con=engine,
        if_exists='replace',
        index=False
    )

    vendas_categoria_df.to_sql(
        'vendas_categoria',
        con=engine,
        if_exists='replace',
        index=False
    )

    venda_produto_df.to_sql(
        'venda_produto',
        con=engine,
        if_exists='replace',
        index=False
    )


if __name__ == "__main__":
    df = pd.read_csv('../data/silver/todos_csv_transformado.csv')
    load_df(df)