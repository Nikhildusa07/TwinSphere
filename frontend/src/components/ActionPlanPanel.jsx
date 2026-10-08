import { useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

function ActionPlanPanel({ decision }) {
  const [resourceAllocation, setResourceAllocation] = useState(null);
  const [actionPlan, setActionPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateActionPlan = async () => {
    if (!decision) {
      return;
    }

    try {
      setLoading(true);
      setError("");

      const resourceResponse = await axios.post(
        `${API_BASE_URL}/predictions/resource-allocation`,
        null,
        {
          params: {
            risk_level: decision.risk_level,
            current_load: 100,
          },
        }
      );

      const allocation = resourceResponse.data;

      setResourceAllocation(allocation);

      const actionResponse = await axios.post(
        `${API_BASE_URL}/predictions/action-plan`,
        null,
        {
          params: {
            risk_level: decision.risk_level,
            recommended_action: decision.action,
            resource_allocation: JSON.stringify(
              allocation
            ),
          },
        }
      );

      setActionPlan(actionResponse.data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Unable to generate autonomous action plan."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel action-plan-panel">
      <div className="panel-header">
        <div>
          <h2>Autonomous Action Plan</h2>
          <p>
            Allocate resources and prepare the recommended
            operational response.
          </p>
        </div>
      </div>

      {!decision && (
        <p className="empty-state">
          Generate an autonomous decision first.
        </p>
      )}

      {decision && (
        <button
          className="primary-button"
          onClick={generateActionPlan}
          disabled={loading}
        >
          {loading
            ? "Generating Action Plan..."
            : "Generate Action Plan"}
        </button>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {resourceAllocation && (
        <div className="action-section">
          <h3>Resource Allocation</h3>

          <div className="action-grid">
            <div>
              <span>Current Load</span>
              <strong>
                {resourceAllocation.current_load}%
              </strong>
            </div>

            <div>
              <span>Adjusted Load</span>
              <strong>
                {resourceAllocation.adjusted_load}%
              </strong>
            </div>

            <div>
              <span>Load Reduction</span>
              <strong>
                {resourceAllocation.load_reduction_percent}%
              </strong>
            </div>

            <div>
              <span>Maintenance Priority</span>
              <strong>
                {resourceAllocation.maintenance_priority}
              </strong>
            </div>

            <div>
              <span>Monitoring</span>
              <strong>
                {resourceAllocation.monitoring_level}
              </strong>
            </div>
          </div>

          <p className="action-message">
            {resourceAllocation.resource_action}
          </p>
        </div>
      )}

      {actionPlan && (
        <div className="action-section">
          <div className="panel-header">
            <h3>Recommended Action Plan</h3>

            <span className="risk-badge high">
              {actionPlan.priority}
            </span>
          </div>

          <p className="recommended-action">
            {actionPlan.recommended_action}
          </p>

          <h3>Execution Steps</h3>

          <ol className="action-list">
            {actionPlan.actions.map(
              (action, index) => (
                <li key={index}>
                  {action}
                </li>
              )
            )}
          </ol>
        </div>
      )}
    </div>
  );
}

export default ActionPlanPanel;