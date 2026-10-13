"""Prepara os dados para o projeto de previsão de churn."""

from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw/telco_customer_churn.csv")
PROCESSED_PATH = Path("data/processed/telco_customer_churn_clean.csv")


def tratar_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    mascara = df["TotalCharges"].isna() & (df["tenure"] == 0)

    print("Registros tratados:", mascara.sum())

    df.loc[mascara, "TotalCharges"] = 0

    assert df["TotalCharges"].isna().sum() == 0, (
        "Existem valores ausentes não tratados."
    )

    assert not df["customerID"].duplicated().any(), (
        "Existem IDs de clientes duplicados."
    )

    return df


def main():
    df = pd.read_csv(RAW_PATH)
    df = tratar_total_charges(df)

    PROCESSED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(PROCESSED_PATH, index=False)

    print("Dimensões da base:", df.shape)
    print("Valores ausentes:", df.isna().sum().sum())
    print("Arquivo salvo em:", PROCESSED_PATH)


if __name__ == "__main__":
    main()
