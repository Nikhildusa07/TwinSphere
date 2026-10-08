from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def create_prediction_model() -> Pipeline:
    """
    Create the machine-learning model used by
    the TwinSphere prediction engine.
    """

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                ),
            ),
        ]
    )

    return model