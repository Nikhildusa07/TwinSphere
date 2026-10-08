from app.services.anomaly_detection_service import detect_anomalies


def main():
    sensor_data = {
        "temperature": 95.0,
        "vibration": 5.8,
        "power_usage": 27.0,
        "operating_speed": 1850,
    }

    result = detect_anomalies(sensor_data)

    print("Anomaly detection result:")
    print(result)


if __name__ == "__main__":
    main()