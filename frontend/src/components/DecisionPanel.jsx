import { useState } from "react";

function DecisionPanel({ scenarioResults }) {
  const [decision, setDecision] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const makeDecision = async () => {
    if (!scenarioResults || scenarioResults.length === 0) {
      setError("Run a simulation before making a decision.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/predictions/decision",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(scenarioResults),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Unable to make decision."
        );
      }

      const data = await response.json();

      setDecision(data);
    } catch (err) {
      console.error(err);
      setError(
        err.message || "Unable to connect to the decision engine."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel decision-panel">
      <div className="panel-header">
        <div>
          <h2>Autonomous Decision</h2>

          <p className="chart-subtitle">
            Select the safest simulated outcome
          </p>
        </div>

        {decision && (
          <span
            className={`risk-badge ${decision.risk_level}`}
          >
            {decision.risk_level}
          </span>
        )}
      </div>

      <button
        className="decision-button"
        onClick={makeDecision}
        disabled={
          loading ||
          !scenarioResults ||
          scenarioResults.length === 0
        }
      >
        {loading
          ? "Analyzing Scenarios..."
          : "Generate Autonomous Decision"}
      </button>

      {error && (
        <p className="decision-error">
          {error}
        </p>
      )}

      {decision && (
        <div className="decision-result">
          <div className="decision-highlight">
            <span>Recommended Scenario</span>

            <strong>
              {decision.recommended_scenario}
            </strong>
          </div>

          <div className="decision-score">
            <span>Predicted Risk Score</span>

            <strong>
              {decision.risk_score}
            </strong>
          </div>

          <div className="decision-action">
            <span>Recommended Action</span>

            <strong>
              {decision.action}
            </strong>
          </div>

          <div className="decision-reason">
            <span>Decision Reason</span>

            <p>
              {decision.reason}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DecisionPanel;