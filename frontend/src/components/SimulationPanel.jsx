import { useState } from "react";
import { simulateScenarios } from "../services/api";

function SimulationPanel({ sensorData, onResults }) {
  const [temperatureChange, setTemperatureChange] = useState(0);
  const [vibrationChange, setVibrationChange] = useState(0);
  const [powerUsageChange, setPowerUsageChange] = useState(0);
  const [operatingSpeedChange, setOperatingSpeedChange] = useState(0);

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const runSimulation = async () => {
    if (!sensorData) {
      setError("Current sensor data is not available.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const scenarios = [
        {
          name: "Current Conditions",
          temperature_change: 0,
          vibration_change: 0,
          power_usage_change: 0,
          operating_speed_change: 0,
        },
        {
          name: "Increased Load",
          temperature_change: Number(temperatureChange),
          vibration_change: Number(vibrationChange),
          power_usage_change: Number(powerUsageChange),
          operating_speed_change: Number(operatingSpeedChange),
        },
      ];

      const response = await simulateScenarios(
        sensorData,
        scenarios
      );

      const simulationResults = response.results || [];

      setResults(simulationResults);

      if (onResults) {
        onResults(simulationResults);
      }
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to run simulation."
      );

      if (onResults) {
        onResults([]);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel simulation-panel">
      <div className="panel-header">
        <div>
          <h2>What-If Simulation</h2>

          <p className="chart-subtitle">
            Simulate possible future operating conditions
          </p>
        </div>
      </div>

      <div className="simulation-controls">
        <div>
          <label htmlFor="temperature-change">
            Temperature Change (°C)
          </label>

          <input
            id="temperature-change"
            type="number"
            value={temperatureChange}
            onChange={(event) =>
              setTemperatureChange(event.target.value)
            }
          />
        </div>

        <div>
          <label htmlFor="vibration-change">
            Vibration Change
          </label>

          <input
            id="vibration-change"
            type="number"
            step="0.1"
            value={vibrationChange}
            onChange={(event) =>
              setVibrationChange(event.target.value)
            }
          />
        </div>

        <div>
          <label htmlFor="power-change">
            Power Change
          </label>

          <input
            id="power-change"
            type="number"
            step="0.1"
            value={powerUsageChange}
            onChange={(event) =>
              setPowerUsageChange(event.target.value)
            }
          />
        </div>

        <div>
          <label htmlFor="speed-change">
            Speed Change
          </label>

          <input
            id="speed-change"
            type="number"
            value={operatingSpeedChange}
            onChange={(event) =>
              setOperatingSpeedChange(event.target.value)
            }
          />
        </div>
      </div>

      <button
        className="simulation-button"
        onClick={runSimulation}
        disabled={loading}
      >
        {loading
          ? "Running Simulation..."
          : "Run What-If Simulation"}
      </button>

      {error && (
        <p className="simulation-error">
          {error}
        </p>
      )}

      {results.length > 0 && (
        <div className="simulation-results">
          <h3>Simulation Results</h3>

          {results.map((result, index) => (
            <div
              className="simulation-result"
              key={`${result.scenario}-${index}`}
            >
              <div className="simulation-result-header">
                <strong>{result.scenario}</strong>

                <span
                  className={`risk-badge ${result.risk_level}`}
                >
                  {result.risk_level}
                </span>
              </div>

              <div className="simulation-state">
                <div>
                  <span>Temperature</span>
                  <strong>
                    {result.simulated_state.temperature.toFixed(
                      2
                    )} °C
                  </strong>
                </div>

                <div>
                  <span>Vibration</span>
                  <strong>
                    {result.simulated_state.vibration.toFixed(
                      2
                    )}
                  </strong>
                </div>

                <div>
                  <span>Power</span>
                  <strong>
                    {result.simulated_state.power_usage.toFixed(
                      2
                    )}
                  </strong>
                </div>

                <div>
                  <span>Speed</span>
                  <strong>
                    {result.simulated_state.operating_speed.toFixed(
                      2
                    )}
                  </strong>
                </div>
              </div>

              <div className="simulation-risk">
                <span>Predicted Risk Score</span>
                <strong>{result.risk_score}</strong>
              </div>

              {result.risk_factors.length > 0 && (
                <ul>
                  {result.risk_factors.map(
                    (factor, factorIndex) => (
                      <li key={factorIndex}>
                        {factor}
                      </li>
                    )
                  )}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SimulationPanel;