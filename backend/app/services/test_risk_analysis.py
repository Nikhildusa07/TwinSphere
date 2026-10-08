from app.services.risk_analysis_service import calculate_risk_level


def main():
    sensor_data = {
        "temperature": 95.0,
        "vibration": 5.8,
        "power_usage": 27.0,
        "operating_speed": 1850,
    }

    result = calculate_risk_level(sensor_data)

    print("Risk analysis result:")
    print(result)


if __name__ == "__main__":
    main()