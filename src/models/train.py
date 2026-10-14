"""Treina e registra o modelo de previsao de churn no MLflow."""

from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.models.preprocessing import criar_preprocessador
from src.tracking.config import configurar_mlflow


DATA_PATH = Path("data/processed/telco_customer_churn_clean.csv")


def main():
    configurar_mlflow()

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

    modelo = Pipeline(
        steps=[
            ("preprocessamento", criar_preprocessador()),
            ("classificador", LogisticRegression(max_iter=1000)),
        ]
    )

    with mlflow.start_run(run_name="logistic-regression-baseline"):
        mlflow.log_params({
            "modelo": "LogisticRegression",
            "max_iter": 1000,
            "test_size": 0.20,
            "random_state": 42,
            "threshold": 0.50,
        })

        modelo.fit(X_train, y_train)

        previsoes = modelo.predict(X_test)
        probabilidades = modelo.predict_proba(X_test)[:, 1]

        metricas = {
            "accuracy": accuracy_score(y_test, previsoes),
            "precision": precision_score(y_test, previsoes),
            "recall": recall_score(y_test, previsoes),
            "f1_score": f1_score(y_test, previsoes),
            "roc_auc": roc_auc_score(y_test, probabilidades),
        }

        mlflow.log_metrics(metricas)
        mlflow.sklearn.log_model(
            sk_model=modelo,
            name="churn-model",
            input_example=X_train.head(3),
        )

        print("\n=== RESULTADOS DO MODELO ===")
        print(classification_report(y_test, previsoes, zero_division=0))
        print("ROC-AUC:", round(metricas["roc_auc"], 4))
        print("Matriz de confusao:")
        print(confusion_matrix(y_test, previsoes))

        print("\n=== COMPARACAO DE LIMITES ===")
        for limite in [0.50, 0.40, 0.30]:
            previsoes_ajustadas = (probabilidades >= limite).astype(int)
            tn, fp, fn, tp = confusion_matrix(
                y_test, previsoes_ajustadas
            ).ravel()

            recall = tp / (tp + fn)
            precision = tp / (tp + fp)

            print(
                f"Limite: {limite:.2f} | "
                f"Recall: {recall:.2%} | "
                f"Precision: {precision:.2%} | "
                f"FN: {fn} | FP: {fp}"
            )

        print("\n=== METRICAS REGISTRADAS NO MLFLOW ===")
        for nome, valor in metricas.items():
            print(f"{nome}: {valor:.4f}")


if __name__ == "__main__":
    main()
