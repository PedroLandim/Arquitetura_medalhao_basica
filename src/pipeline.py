from extract import extract_data_from_data
from transform import transform_df, check_validation
from load import load_df


def run_pipeline():

    print("Iniciando pipeline...")

    # EXTRACT
    print("\n[1/3] Extraindo dados...")
    df = extract_data_from_data()

    df.to_csv(
        '../data/bronze/todos_csv.csv',
        index=False
    )

    print(f"{len(df)} registros extraídos.")

    # TRANSFORM
    print("\n[2/3] Transformando dados...")
    df = transform_df(df)

    check_validation(df)

    df.to_csv(
        '../data/silver/todos_csv_transformado.csv',
        index=False
    )

    print(f"{len(df)} registros enviados para Silver.")

    # LOAD
    print("\n[3/3] Carregando camada Gold...")
    load_df(df)

    print("\nPipeline finalizado com sucesso! ✅")


if __name__ == "__main__":
    run_pipeline()