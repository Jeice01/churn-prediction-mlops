"""Verificações básicas de qualidade da base Telco Customer Churn."""

import pandas as pd


def main():
    caminho = "data/processed/telco_customer_churn_clean.csv"

    df = pd.read_csv(caminho)

    print("=== RELATÓRIO DE QUALIDADE DOS DADOS ===")
    print(f"Total de registros: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")
    print(f"Clientes únicos: {df['customerID'].nunique()}")
    print(f"IDs duplicados: {df['customerID'].duplicated().sum()}")
    print(f"Valores ausentes: {df.isna().sum().sum()}")

    print("\nDistribuição de churn:")
    print(df["Churn"].value_counts())

    print("\nTipos de dados:")
    print(df.dtypes)


if __name__ == "__main__":
    main()
