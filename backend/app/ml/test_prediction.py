from app.ml.train_model import train_prediction_model


def main():
    model = train_prediction_model()

    latest_sensor_data = [
        [
            82.3,
            3.9,
            18.7,
            1520,
        ]
    ]

    prediction = model.predict(latest_sensor_data)

    print(
        f"Predicted next temperature: {prediction[0]:.2f} °C"
    )


if __name__ == "__main__":
    main()