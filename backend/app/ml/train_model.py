from app.ml.prediction_model import create_prediction_model
from app.ml.training_data import generate_training_data


def train_prediction_model():
    """
    Generate historical training data and train
    the TwinSphere prediction model.
    """

    X, y = generate_training_data()

    model = create_prediction_model()

    model.fit(X, y)

    return model