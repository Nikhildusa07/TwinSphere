import { useEffect, useMemo, useState } from "react";

import axios from "axios";

import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

const API_BASE_URL =
    import.meta.env.VITE_API_URL ||
    "https://twinsphere.onrender.com";

function Dashboard() {
    const [dashboard, setDashboard] = useState(null);
    const [sensorHistory, setSensorHistory] = useState([]);
    const [predictionAccuracy, setPredictionAccuracy] = useState(null);

    const [simulationResults, setSimulationResults] = useState([]);
    const [decision, setDecision] = useState(null);

    const [causalAnalysis, setCausalAnalysis] = useState(null);
    const [timeSeriesAnalysis, setTimeSeriesAnalysis] = useState(null);
    const [simulationComparison, setSimulationComparison] = useState(null);
    const [reinforcementLearning, setReinforcementLearning] = useState(null);

    const [loading, setLoading] = useState(true);
    const [analyticsLoading, setAnalyticsLoading] = useState(false);
    const [simulationLoading, setSimulationLoading] = useState(false);
    const [decisionLoading, setDecisionLoading] = useState(false);

    const [simulationInput, setSimulationInput] = useState({
        temperature_change: 0,
        vibration_change: 0,
        power_usage_change: 0,
        operating_speed_change: 0,
    });

    const loadAnalytics = async (digitalTwinId) => {
        if (!digitalTwinId) {
            return;
        }

        try {
            setAnalyticsLoading(true);

            const results = await Promise.allSettled([
                axios.post(
                    `${API_BASE_URL}/predictions/causal-analysis?digital_twin_id=${digitalTwinId}`
                ),

                axios.post(
                    `${API_BASE_URL}/predictions/time-series?digital_twin_id=${digitalTwinId}`
                ),

                axios.get(
                    `${API_BASE_URL}/predictions/simulation-vs-actual`
                ),

                axios.get(
                    `${API_BASE_URL}/predictions/reinforcement-learning?digital_twin_id=${digitalTwinId}`
                ),

                axios.get(
                    `${API_BASE_URL}/action-feedback/accuracy`
                ),
            ]);

            const [
                causalResult,
                timeSeriesResult,
                comparisonResult,
                reinforcementResult,
                accuracyResult,
            ] = results;

            if (causalResult.status === "fulfilled") {
                setCausalAnalysis(causalResult.value.data);
            } else {
                console.error(
                    "Causal analysis error:",
                    causalResult.reason
                );
            }

            if (timeSeriesResult.status === "fulfilled") {
                setTimeSeriesAnalysis(timeSeriesResult.value.data);
            } else {
                console.error(
                    "Time-series analysis error:",
                    timeSeriesResult.reason
                );
            }

            if (comparisonResult.status === "fulfilled") {
                setSimulationComparison(comparisonResult.value.data);
            } else {
                console.error(
                    "Simulation comparison error:",
                    comparisonResult.reason
                );
            }

            if (reinforcementResult.status === "fulfilled") {
                setReinforcementLearning(
                    reinforcementResult.value.data
                );
            } else {
                console.error(
                    "Reinforcement learning error:",
                    reinforcementResult.reason
                );
            }

            if (accuracyResult.status === "fulfilled") {
                setPredictionAccuracy(
                    accuracyResult.value.data
                );
            } else {
                console.error(
                    "Prediction accuracy error:",
                    accuracyResult.reason
                );
            }
        } finally {
            setAnalyticsLoading(false);
        }
    };

    const loadDashboard = async () => {
        try {
            setLoading(true);

            const [
                dashboardResponse,
                sensorResponse,
            ] = await Promise.all([
                axios.get(
                    `${API_BASE_URL}/dashboard/overview`
                ),
                axios.get(
                    `${API_BASE_URL}/sensor-data/`
                ),
            ]);

            const dashboardData = dashboardResponse.data;

            setDashboard(dashboardData);

            const history = [...sensorResponse.data]
                .sort(
                    (a, b) =>
                        new Date(a.recorded_at) -
                        new Date(b.recorded_at)
                )
                .slice(-10);

            setSensorHistory(history);

            await loadAnalytics(
                dashboardData?.digital_twin?.id
            );
        } catch (error) {
            console.error(
                "Dashboard loading error:",
                error
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDashboard();
    }, []);

    const chartData = useMemo(() => {
        return sensorHistory.map((item, index) => ({
            name: `Reading ${index + 1}`,
            temperature: Number(item.temperature),
            vibration: Number(item.vibration),
            power: Number(item.power_usage),
            speed: Number(item.operating_speed),
        }));
    }, [sensorHistory]);

    const handleSimulationInput = (event) => {
        const { name, value } = event.target;

        setSimulationInput((previous) => ({
            ...previous,
            [name]: value,
        }));
    };

    const runSimulation = async () => {
        if (!dashboard?.current_state) {
            return;
        }

        try {
            setSimulationLoading(true);
            setDecision(null);

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
                    temperature_change: Number(
                        simulationInput.temperature_change
                    ),
                    vibration_change: Number(
                        simulationInput.vibration_change
                    ),
                    power_usage_change: Number(
                        simulationInput.power_usage_change
                    ),
                    operating_speed_change: Number(
                        simulationInput.operating_speed_change
                    ),
                },
            ];

            const response = await axios.post(
                `${API_BASE_URL}/predictions/scenarios`,
                {
                    sensor_data: dashboard.current_state,
                    scenarios,
                }
            );

            setSimulationResults(
                response.data.results || []
            );
        } catch (error) {
            console.error(
                "Simulation error:",
                error
            );
        } finally {
            setSimulationLoading(false);
        }
    };

    const generateDecision = async () => {
        if (!simulationResults.length) {
            return;
        }

        try {
            setDecisionLoading(true);

            const response = await axios.post(
                `${API_BASE_URL}/predictions/decision`,
                simulationResults
            );

            setDecision(response.data);
        } catch (error) {
            console.error(
                "Decision error:",
                error
            );
        } finally {
            setDecisionLoading(false);
        }
    };

    const getRiskClass = (riskLevel) => {
        if (!riskLevel) {
            return "risk-unknown";
        }

        const normalizedRisk = String(
            riskLevel
        )
            .trim()
            .toLowerCase();

        return `risk-${normalizedRisk}`;
    };

    const formatRiskLevel = (riskLevel) => {
        if (!riskLevel) {
            return "UNKNOWN";
        }

        return String(riskLevel)
            .trim()
            .toUpperCase();
    };

    const formatNumber = (
        value,
        decimals = 2
    ) => {
        const number = Number(value);

        if (Number.isNaN(number)) {
            return "—";
        }

        return number.toFixed(decimals);
    };

    if (loading) {
        return (
            <div className="dashboard-page">
                <div className="dashboard-loading">
                    Loading TwinSphere dashboard...
                </div>
            </div>
        );
    }

    if (!dashboard) {
        return (
            <div className="dashboard-page">
                <div className="dashboard-error">
                    <h2>Dashboard Error</h2>

                    <p>
                        Unable to load TwinSphere
                        dashboard.
                    </p>

                    <button
                        className="dashboard-button"
                        onClick={loadDashboard}
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    const twin = dashboard.digital_twin;
    const currentState =
        dashboard.current_state;
    const risk = dashboard.risk;
    const learning =
        dashboard.learning_status;

    const evaluatedPredictions =
        predictionAccuracy?.total_predictions ??
        learning.total_predictions ??
        0;

    const accuracyRate =
        predictionAccuracy?.accuracy_rate ??
        learning.accuracy_rate ??
        learning.accuracy ??
        0;

    const averageError =
        predictionAccuracy?.average_error ??
        learning.average_error ??
        0;

    const accuratePredictions =
        predictionAccuracy?.accurate ??
        predictionAccuracy?.accurate_predictions ??
        learning.accurate_predictions ??
        0;

    return (
        <div className="dashboard-page">
            {/* ================= HEADER ================= */}

            <header className="dashboard-header">
                <div>
                    <div className="dashboard-eyebrow">
                        AUTONOMOUS DIGITAL TWIN
                    </div>

                    <h1>TwinSphere</h1>

                    <p>
                        Predictive Decision
                        Intelligence Dashboard
                    </p>
                </div>

                <div className="machine-status">
                    <span className="status-dot"></span>

                    <div>
                        <strong>
                            {twin.name}
                        </strong>

                        <span>
                            {twin.entity_type}
                        </span>
                    </div>
                </div>
            </header>

            {/* ================= SENSOR CARDS ================= */}

            <section className="sensor-grid">
                <div className="metric-card">
                    <span>
                        Temperature
                    </span>

                    <strong>
                        {formatNumber(
                            currentState.temperature,
                            1
                        )}{" "}
                        °C
                    </strong>
                </div>

                <div className="metric-card">
                    <span>
                        Vibration
                    </span>

                    <strong>
                        {formatNumber(
                            currentState.vibration,
                            1
                        )}
                    </strong>
                </div>

                <div className="metric-card">
                    <span>
                        Power Usage
                    </span>

                    <strong>
                        {formatNumber(
                            currentState.power_usage,
                            1
                        )}
                    </strong>
                </div>

                <div className="metric-card">
                    <span>
                        Operating Speed
                    </span>

                    <strong>
                        {formatNumber(
                            currentState.operating_speed,
                            0
                        )}
                    </strong>
                </div>
            </section>

            {/* ================= TWIN + RISK ================= */}

            <section className="two-column-grid">
                <div className="dashboard-card">
                    <div className="card-header">
                        <h2>
                            Digital Twin State
                        </h2>

                        <span className="status-badge normal">
                            {formatRiskLevel(
                                twin.status
                            )}
                        </span>
                    </div>

                    <div className="twin-details">
                        <div>
                            <span>
                                Digital Twin ID
                            </span>

                            <strong>
                                #{twin.id}
                            </strong>
                        </div>

                        <div>
                            <span>
                                Entity Type
                            </span>

                            <strong>
                                {twin.entity_type}
                            </strong>
                        </div>

                        <div>
                            <span>
                                Temperature
                            </span>

                            <strong>
                                {formatNumber(
                                    currentState.temperature,
                                    1
                                )}{" "}
                                °C
                            </strong>
                        </div>

                        <div>
                            <span>
                                Vibration
                            </span>

                            <strong>
                                {formatNumber(
                                    currentState.vibration,
                                    1
                                )}
                            </strong>
                        </div>

                        <div>
                            <span>
                                Power Usage
                            </span>

                            <strong>
                                {formatNumber(
                                    currentState.power_usage,
                                    1
                                )}
                            </strong>
                        </div>

                        <div>
                            <span>
                                Operating Speed
                            </span>

                            <strong>
                                {formatNumber(
                                    currentState.operating_speed,
                                    0
                                )}
                            </strong>
                        </div>
                    </div>
                </div>

                <div className="dashboard-card">
                    <div className="card-header">
                        <h2>
                            Operational Risk
                        </h2>

                        <span
                            className={`status-badge ${getRiskClass(
                                risk.risk_level
                            )}`}
                        >
                            {formatRiskLevel(
                                risk.risk_level
                            )}
                        </span>
                    </div>

                    <div className="risk-score-row">
                        <strong>
                            {risk.risk_score}
                        </strong>

                        <span>
                            Risk Score
                        </span>
                    </div>

                    <h4>
                        Risk Factors
                    </h4>

                    {risk.risk_factors?.length >
                    0 ? (
                        <ul className="risk-list">
                            {risk.risk_factors.map(
                                (
                                    factor,
                                    index
                                ) => (
                                    <li
                                        key={
                                            index
                                        }
                                    >
                                        {factor}
                                    </li>
                                )
                            )}
                        </ul>
                    ) : (
                        <p className="muted-text">
                            No active risk
                            factors.
                        </p>
                    )}
                </div>
            </section>

            {/* ================= HISTORY + PREDICTION ================= */}

            <section className="two-column-grid">
                <div className="dashboard-card chart-card">
                    <div className="card-header">
                        <div>
                            <h2>
                                Sensor History
                            </h2>

                            <p>
                                Recent
                                digital-twin
                                sensor
                                readings
                            </p>
                        </div>
                    </div>

                    <div className="chart-container">
                        {chartData.length >
                        0 ? (
                            <ResponsiveContainer
                                width="100%"
                                height={280}
                            >
                                <LineChart
                                    data={
                                        chartData
                                    }
                                >
                                    <CartesianGrid
                                        strokeDasharray="3 3"
                                        stroke="#334155"
                                    />

                                    <XAxis
                                        dataKey="name"
                                        stroke="#94a3b8"
                                    />

                                    <YAxis
                                        stroke="#94a3b8"
                                    />

                                    <Tooltip
                                        contentStyle={{
                                            background:
                                                "#0f172a",
                                            border:
                                                "1px solid #334155",
                                            borderRadius:
                                                "10px",
                                            color:
                                                "#ffffff",
                                        }}
                                    />

                                    <Line
                                        type="monotone"
                                        dataKey="temperature"
                                        stroke="#38bdf8"
                                        strokeWidth={
                                            3
                                        }
                                        dot
                                    />

                                    <Line
                                        type="monotone"
                                        dataKey="power"
                                        stroke="#a78bfa"
                                        strokeWidth={
                                            2
                                        }
                                        dot
                                    />

                                    <Line
                                        type="monotone"
                                        dataKey="vibration"
                                        stroke="#f59e0b"
                                        strokeWidth={
                                            2
                                        }
                                        dot
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        ) : (
                            <div className="empty-state">
                                No sensor
                                history
                                available.
                            </div>
                        )}
                    </div>
                </div>

                <div className="dashboard-card">
                    <div className="card-header">
                        <h2>
                            Prediction
                            Performance
                        </h2>
                    </div>

                    <div className="prediction-grid">
                        <div>
                            <span>
                                Evaluated
                                Predictions
                            </span>

                            <strong>
                                {
                                    evaluatedPredictions
                                }
                            </strong>
                        </div>

                        <div>
                            <span>
                                Accuracy Rate
                            </span>

                            <strong>
                                {
                                    formatNumber(
                                        accuracyRate,
                                        0
                                    )
                                }
                                %
                            </strong>
                        </div>

                        <div>
                            <span>
                                Average Error
                            </span>

                            <strong>
                                {
                                    formatNumber(
                                        averageError,
                                        2
                                    )
                                }{" "}
                                °C
                            </strong>
                        </div>

                        <div>
                            <span>
                                Accurate
                            </span>

                            <strong>
                                {
                                    accuratePredictions
                                }
                            </strong>
                        </div>
                    </div>
                </div>
            </section>

            {/* ================= CONTINUOUS LEARNING ================= */}

            <section className="dashboard-card learning-card">
                <div className="card-header">
                    <div>
                        <h2>
                            Continuous
                            Learning
                        </h2>

                        <p>
                            {learning.reason}
                        </p>
                    </div>

                    <span
                        className={`status-badge ${
                            learning.retraining_required
                                ? "risk-high"
                                : "normal"
                        }`}
                    >
                        {learning.retraining_required
                            ? "RETRAINING REQUIRED"
                            : "MODEL STABLE"}
                    </span>
                </div>

                <div className="learning-stats">
                    <div>
                        <span>
                            Average Error
                        </span>

                        <strong>
                            {
                                formatNumber(
                                    learning.average_error,
                                    2
                                )
                            }{" "}
                            °C
                        </strong>
                    </div>

                    <div>
                        <span>
                            Retraining
                            Threshold
                        </span>

                        <strong>
                            {
                                formatNumber(
                                    learning.retraining_threshold ??
                                        5,
                                    0
                                )
                            }{" "}
                            °C
                        </strong>
                    </div>

                    <div>
                        <span>
                            Predictions
                            Evaluated
                        </span>

                        <strong>
                            {
                                learning.total_predictions
                            }
                        </strong>
                    </div>
                </div>
            </section>

            {/* ================= ADVANCED INTELLIGENCE ================= */}

            <section className="dashboard-card">
                <div className="card-header">
                    <div>
                        <h2>
                            Advanced Intelligence
                        </h2>

                        <p>
                            Causal analysis,
                            time-series
                            forecasting,
                            simulation
                            validation and
                            reinforcement
                            learning
                        </p>
                    </div>

                    <span
                        className={`status-badge ${
                            analyticsLoading
                                ? "risk-medium"
                                : "normal"
                        }`}
                    >
                        {analyticsLoading
                            ? "ANALYZING"
                            : "READY"}
                    </span>
                </div>

                {analyticsLoading ? (
                    <p className="muted-text">
                        Running advanced
                        intelligence
                        analysis...
                    </p>
                ) : (
                    <div className="decision-result">
                        {/* CAUSAL ANALYSIS */}

                        <div className="decision-item">
                            <span>
                                Strongest
                                Influencing
                                Factor
                            </span>

                            <strong>
                                {causalAnalysis?.strongest_influencing_factor ??
                                    "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Causal
                                Interpretation
                            </span>

                            <p>
                                {causalAnalysis?.interpretation ??
                                    "Causal analysis data is not available."}
                            </p>
                        </div>

                        {/* TIME SERIES */}

                        <div className="decision-item">
                            <span>
                                Temperature
                                Trend
                            </span>

                            <strong>
                                {timeSeriesAnalysis?.trend_direction
                                    ? String(
                                          timeSeriesAnalysis.trend_direction
                                      ).toUpperCase()
                                    : "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Forecasted Next
                                Temperature
                            </span>

                            <strong>
                                {timeSeriesAnalysis?.forecasted_next_temperature !==
                                undefined
                                    ? `${formatNumber(
                                          timeSeriesAnalysis.forecasted_next_temperature,
                                          2
                                      )} °C`
                                    : "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Time-Series
                                Interpretation
                            </span>

                            <p>
                                {timeSeriesAnalysis?.interpretation ??
                                    "Time-series analysis data is not available."}
                            </p>
                        </div>

                        {/* SIMULATION VS ACTUAL */}

                        <div className="decision-item">
                            <span>
                                Simulation vs
                                Actual Accuracy
                            </span>

                            <strong>
                                {simulationComparison?.accuracy_rate !==
                                undefined
                                    ? `${formatNumber(
                                          simulationComparison.accuracy_rate,
                                          0
                                      )}%`
                                    : "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Simulation
                                Average Error
                            </span>

                            <strong>
                                {simulationComparison?.average_error !==
                                undefined
                                    ? `${formatNumber(
                                          simulationComparison.average_error,
                                          2
                                      )} °C`
                                    : "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Simulation
                                Interpretation
                            </span>

                            <p>
                                {simulationComparison?.interpretation ??
                                    "Simulation comparison data is not available."}
                            </p>
                        </div>

                        {/* REINFORCEMENT LEARNING */}

                        <div className="decision-item">
                            <span>
                                RL State
                            </span>

                            <strong>
                                {reinforcementLearning?.state
                                    ? String(
                                          reinforcementLearning.state
                                      ).toUpperCase()
                                    : "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                RL Recommended
                                Action
                            </span>

                            <strong>
                                {reinforcementLearning?.recommended_action ??
                                    "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Estimated Reward
                            </span>

                            <strong>
                                {reinforcementLearning?.estimated_reward !==
                                undefined
                                    ? formatNumber(
                                          reinforcementLearning.estimated_reward,
                                          2
                                      )
                                    : "—"}
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Learning Method
                            </span>

                            <p>
                                {reinforcementLearning?.learning_method ??
                                    "—"}
                            </p>
                        </div>
                    </div>
                )}
            </section>

            {/* ================= WHAT-IF SIMULATION ================= */}

            <section className="dashboard-card simulation-card">
                <div className="card-header">
                    <div>
                        <h2>
                            What-If
                            Simulation
                        </h2>

                        <p>
                            Simulate possible
                            future operating
                            conditions
                        </p>
                    </div>
                </div>

                <div className="simulation-input-grid">
                    <label>
                        Temperature Change
                        (°C)

                        <input
                            type="number"
                            name="temperature_change"
                            value={
                                simulationInput.temperature_change
                            }
                            onChange={
                                handleSimulationInput
                            }
                        />
                    </label>

                    <label>
                        Vibration Change

                        <input
                            type="number"
                            name="vibration_change"
                            value={
                                simulationInput.vibration_change
                            }
                            onChange={
                                handleSimulationInput
                            }
                        />
                    </label>

                    <label>
                        Power Change

                        <input
                            type="number"
                            name="power_usage_change"
                            value={
                                simulationInput.power_usage_change
                            }
                            onChange={
                                handleSimulationInput
                            }
                        />
                    </label>

                    <label>
                        Speed Change

                        <input
                            type="number"
                            name="operating_speed_change"
                            value={
                                simulationInput.operating_speed_change
                            }
                            onChange={
                                handleSimulationInput
                            }
                        />
                    </label>
                </div>

                <button
                    className="dashboard-button primary"
                    onClick={runSimulation}
                    disabled={simulationLoading}
                >
                    {simulationLoading
                        ? "Running Simulation..."
                        : "Run What-If Simulation"}
                </button>

                {simulationResults.length >
                    0 && (
                    <div className="simulation-results">
                        <h3>
                            Simulation
                            Results
                        </h3>

                        {simulationResults.map(
                            (
                                scenario,
                                index
                            ) => (
                                <div
                                    className="scenario-card"
                                    key={
                                        index
                                    }
                                >
                                    <div className="scenario-header">
                                        <h3>
                                            {
                                                scenario.scenario
                                            }
                                        </h3>

                                        <span
                                            className={`status-badge ${getRiskClass(
                                                scenario.risk_level
                                            )}`}
                                        >
                                            {formatRiskLevel(
                                                scenario.risk_level
                                            )}
                                        </span>
                                    </div>

                                    <div className="scenario-values">
                                        <div>
                                            <span>
                                                Temperature
                                            </span>

                                            <strong>
                                                {formatNumber(
                                                    scenario
                                                        .simulated_state
                                                        .temperature,
                                                    2
                                                )}{" "}
                                                °C
                                            </strong>
                                        </div>

                                        <div>
                                            <span>
                                                Vibration
                                            </span>

                                            <strong>
                                                {formatNumber(
                                                    scenario
                                                        .simulated_state
                                                        .vibration,
                                                    2
                                                )}
                                            </strong>
                                        </div>

                                        <div>
                                            <span>
                                                Power
                                            </span>

                                            <strong>
                                                {formatNumber(
                                                    scenario
                                                        .simulated_state
                                                        .power_usage,
                                                    2
                                                )}
                                            </strong>
                                        </div>

                                        <div>
                                            <span>
                                                Speed
                                            </span>

                                            <strong>
                                                {formatNumber(
                                                    scenario
                                                        .simulated_state
                                                        .operating_speed,
                                                    0
                                                )}
                                            </strong>
                                        </div>
                                    </div>

                                    <div className="scenario-risk">
                                        <span>
                                            Predicted
                                            Risk Score
                                        </span>

                                        <strong>
                                            {
                                                scenario.risk_score
                                            }
                                        </strong>
                                    </div>

                                    {scenario
                                        .risk_factors
                                        ?.length >
                                        0 && (
                                        <ul className="risk-list">
                                            {scenario.risk_factors.map(
                                                (
                                                    factor,
                                                    factorIndex
                                                ) => (
                                                    <li
                                                        key={
                                                            factorIndex
                                                        }
                                                    >
                                                        {
                                                            factor
                                                        }
                                                    </li>
                                                )
                                            )}
                                        </ul>
                                    )}
                                </div>
                            )
                        )}
                    </div>
                )}
            </section>

            {/* ================= AUTONOMOUS DECISION ================= */}

            <section className="dashboard-card decision-card">
                <div className="card-header">
                    <div>
                        <h2>
                            Autonomous
                            Decision
                        </h2>

                        <p>
                            Select the safest
                            simulated
                            outcome
                        </p>
                    </div>

                    {decision && (
                        <span
                            className={`status-badge ${getRiskClass(
                                decision.risk_level
                            )}`}
                        >
                            {formatRiskLevel(
                                decision.risk_level
                            )}
                        </span>
                    )}
                </div>

                <button
                    className="dashboard-button primary"
                    onClick={generateDecision}
                    disabled={
                        !simulationResults.length ||
                        decisionLoading
                    }
                >
                    {decisionLoading
                        ? "Generating Decision..."
                        : "Generate Autonomous Decision"}
                </button>

                {!simulationResults.length && (
                    <p className="muted-text">
                        Run a What-If
                        Simulation first.
                    </p>
                )}

                {decision && (
                    <div className="decision-result">
                        <div className="decision-item">
                            <span>
                                Recommended
                                Scenario
                            </span>

                            <strong>
                                {
                                    decision.recommended_scenario
                                }
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Predicted Risk
                                Score
                            </span>

                            <strong>
                                {
                                    decision.risk_score
                                }
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Recommended
                                Action
                            </span>

                            <strong>
                                {
                                    decision.action
                                }
                            </strong>
                        </div>

                        <div className="decision-item">
                            <span>
                                Decision Reason
                            </span>

                            <p>
                                {
                                    decision.reason
                                }
                            </p>
                        </div>
                    </div>
                )}
            </section>

            {/* ================= REFRESH ================= */}

            <div className="dashboard-footer">
                <button
                    className="dashboard-button"
                    onClick={loadDashboard}
                >
                    Refresh Dashboard
                </button>
            </div>
        </div>
    );
}

export default Dashboard;