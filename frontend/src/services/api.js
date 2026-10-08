import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getDashboardOverview = async () => {
  const response = await api.get("/dashboard/overview");
  return response.data;
};

export const getDigitalTwins = async () => {
  const response = await api.get("/digital-twins/");
  return response.data;
};

export const getSensorData = async () => {
  const response = await api.get("/sensor-data/");
  return response.data;
};

export const predictTemperature = async (sensorData) => {
  const response = await api.post("/predictions/", sensorData);
  return response.data;
};

export const detectAnomaly = async (sensorData) => {
  const response = await api.post(
    "/predictions/anomaly",
    sensorData
  );
  return response.data;
};

export const calculateRisk = async (sensorData) => {
  const response = await api.post(
    "/predictions/risk",
    sensorData
  );
  return response.data;
};

export const simulateScenarios = async (
  sensorData,
  scenarios
) => {
  const response = await api.post("/predictions/scenarios", {
    sensor_data: sensorData,
    scenarios,
  });

  return response.data;
};

export const makeDecision = async (scenarioResults) => {
  const response = await api.post(
    "/predictions/decision",
    scenarioResults
  );

  return response.data;
};

export const allocateResources = async (
  riskLevel,
  currentLoad
) => {
  const response = await api.post(
    "/predictions/resource-allocation",
    null,
    {
      params: {
        risk_level: riskLevel,
        current_load: currentLoad,
      },
    }
  );

  return response.data;
};

export const createActionPlan = async (
  riskLevel,
  recommendedAction,
  resourceAllocation
) => {
  const response = await api.post(
    "/predictions/action-plan",
    null,
    {
      params: {
        risk_level: riskLevel,
        recommended_action: recommendedAction,
        resource_allocation: JSON.stringify(
          resourceAllocation
        ),
      },
    }
  );

  return response.data;
};

export const getFeedback = async () => {
  const response = await api.get("/feedback/");
  return response.data;
};

export const getPredictionAccuracy = async () => {
  const response = await api.get("/feedback/accuracy");
  return response.data;
};

export const getLearningStatus = async () => {
  const response = await api.get(
    "/feedback/learning-status"
  );
  return response.data;
};

export default api;