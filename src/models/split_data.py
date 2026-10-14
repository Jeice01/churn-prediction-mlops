"""Divide os dados em conjuntos de treinamento e teste."""

import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = "data/processed/telco_customer_churn_clean.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["Churn", "customerID"])
    y = df["Churn"].map({"No": 0, "Yes": 1})

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("Treinamento:", X_train.shape)
    print("Teste:", X_test.shape)
    print("Churn no treinamento:", round(y_train.mean() * 100, 2), "%")
    print("Churn no teste:", round(y_test.mean() * 100, 2), "%")


if __name__ == "__main__":
    main()
