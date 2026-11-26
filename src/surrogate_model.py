"""
Trains a Scikit-learn Gradient Boosting surrogate model to predict structural stress and
component degradation rapidly without re-running full solver iterations.
"""


import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def train_stress_surrogate(csv_path: str = "data/doe_simulation_dataset.csv"):
    df = pd.read_csv(csv_path)
    features = ["length_mm", "thickness_mm", "fillet_radius_mm", "load_n"]
    target = "max_stress_mpa"

    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(n_estimators=150, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"Surrogate Model Validation -> R2 Score: {r2:.4f} | MAE: {mae:.2f} MPa")
    return model


if __name__ == "__main__":
    train_stress_surrogate()
  
