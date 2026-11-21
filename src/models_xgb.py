from pathlib import Path

import duckdb
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier


MODELS_DIR = Path("models")

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_features():

    con = duckdb.connect()

    features = con.sql("""
    SELECT *
    FROM 'data/processed/features.parquet'
    """).df()

    print(
        f"Features loaded: {len(features):,}"
    )

    return features


def train_model():

    features = load_features()

    print(
        features["y"]
        .value_counts()
    )

    print(
        features["y"]
        .value_counts(normalize=True)
    )

    feature_cols = [

        "elo_white",
        "elo_black",

        "elo_diff",
        "elo_mean",

        "white_games_count",
        "black_games_count",

        "white_form_10",
        "black_form_10",

        "white_form_30",
        "black_form_30",

        "days_since_last_game_white",
        "days_since_last_game_black",

        "h2h_games",
        "h2h_white_score",

        "eco_games",
        "eco_white_score",
        "eco_draw_rate",

        "white_rating_trend_10",
        "black_rating_trend_10",

        "white_rating_trend_30",
        "black_rating_trend_30",

        "white_wins_last10",
        "white_draws_last10",
        "white_losses_last10",

        "black_wins_last10",
        "black_draws_last10",
        "black_losses_last10",

        "white_score_vs_2700",
        "black_score_vs_2700",

        "white_score_as_white",
        "black_score_as_black"
    ]

    X = features[
        feature_cols
    ].copy()

    y = features["y"]

    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    X = X.fillna(0)

    print(
        f"\nX shape: {X.shape}"
    )

    print(
        f"y shape: {y.shape}"
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(
        f"\nTrain rows: {len(X_train):,}"
    )

    print(
        f"Test rows: {len(X_test):,}"
    )

    model = XGBClassifier(

        objective="multi:softmax",

        num_class=3,

        n_estimators=500,

        max_depth=8,

        learning_rate=0.05,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42,

        tree_method="hist",

        n_jobs=-1
    )

    print(
        "\nTraining XGBoost..."
    )

    model.fit(
        X_train,
        y_train
    )

    y_pred = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print(
        "\n" + "=" * 60
    )

    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print(
        "\nClassification Report\n"
    )

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Black Win",
                "Draw",
                "White Win"
            ]
        )
    )

    print(
        "\nConfusion Matrix\n"
    )

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print(
        "\n" + "=" * 60
    )

    model_path = (
        MODELS_DIR /
        "xgboost.joblib"
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        "\nModel saved:"
    )

    print(
        model_path
    )
    importance = pd.DataFrame({

        "feature": feature_cols,

        "importance":
            model.feature_importances_

    })

    importance = importance.sort_values(
        by="importance",
        ascending=False
    )

    print("\nFEATURE IMPORTANCE\n")

    print(
        importance.head(20)
    )

    return model


def main():

    train_model()


if __name__ == "__main__":

    main()