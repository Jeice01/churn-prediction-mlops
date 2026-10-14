"""Otimiza o limite de classificacao e registra o experimento no MLflow."""

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    fbeta_score,
    make_scorer,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    TunedThresholdClassifierCV,
    train_test_split,
)
from sklearn.pipeline import Pipeline

from src.models.preprocessing import criar_preprocessador
from src.tracking.config import configurar_mlflow


DATA_PATH = "data/processed/telco_customer_churn_clean.csv"


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

    pipeline = Pipeline(
        steps=[
            ("preprocessamento", criar_preprocessador()),
            ("classificador", LogisticRegression(max_iter=1000)),
        ]
    )

    validacao = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    modelo_ajustado = TunedThresholdClassifierCV(
        estimator=pipeline,
        scoring=make_scorer(fbeta_score, beta=2),
        cv=validacao,
    )

    with mlflow.start_run(run_name="logistic-regression-tuned-f2"):
        mlflow.log_params({
            "modelo": "LogisticRegression",
            "max_iter": 1000,
            "test_size": 0.20,
            "random_state": 42,
            "cv_folds": 5,
            "scoring": "f2",
        })

        modelo_ajustado.fit(X_train, y_train)

        previsoes = modelo_ajustado.predict(X_test)
        probabilidades = modelo_ajustado.predict_proba(X_test)[:, 1]

        metricas = {
            "accuracy": accuracy_score(y_test, previsoes),
            "precision": precision_score(y_test, previsoes),
            "recall": recall_score(y_test, previsoes),
            "f1_score": f1_score(y_test, previsoes),
            "f2_score": fbeta_score(y_test, previsoes, beta=2),
            "roc_auc": roc_auc_score(y_test, probabilidades),
        }

        mlflow.log_param(
            "best_threshold",
            round(float(modelo_ajustado.best_threshold_), 6),
        )
        mlflow.log_metrics(metricas)

        mlflow.sklearn.log_model(
            sk_model=modelo_ajustado,
            name="churn-model-tuned",
            input_example=X_train.head(3),
            serialization_format="cloudpickle",
        )

        print("\n=== LIMITE OTIMIZADO ===")
        print(round(modelo_ajustado.best_threshold_, 4))

        print("\n=== RESULTADOS NO TESTE ===")
        print(classification_report(y_test, previsoes, zero_division=0))
        print("ROC-AUC:", round(metricas["roc_auc"], 4))
        print("Matriz de confusao:")
        print(confusion_matrix(y_test, previsoes))

        print("\n=== METRICAS REGISTRADAS NO MLFLOW ===")
        for nome, valor in metricas.items():
            print(f"{nome}: {valor:.4f}")


if __name__ == "__main__":
    main()
