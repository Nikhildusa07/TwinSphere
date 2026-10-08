import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function SensorChart({ sensorData }) {
  if (!sensorData || sensorData.length === 0) {
    return (
      <div className="panel">
        <div className="panel-header">
          <h2>Sensor History</h2>
        </div>

        <p className="learning-message">
          No historical sensor data available.
        </p>
      </div>
    );
  }

  const chartData = [...sensorData]
    .slice(-20)
    .reverse()
    .map((item, index) => ({
      name: `Reading ${index + 1}`,
      temperature: Number(item.temperature),
      vibration: Number(item.vibration),
      power: Number(item.power_usage),
    }));

  return (
    <div className="panel sensor-chart-panel">
      <div className="panel-header">
        <div>
          <h2>Sensor History</h2>
          <p className="chart-subtitle">
            Recent digital-twin sensor readings
          </p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart
            data={chartData}
            margin={{
              top: 10,
              right: 20,
              left: 0,
              bottom: 10,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="temperature"
              name="Temperature"
              strokeWidth={2}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="vibration"
              name="Vibration"
              strokeWidth={2}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="power"
              name="Power Usage"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default SensorChart;