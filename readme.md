# TwinSphere

> **Autonomous Digital Twin & Predictive Decision Intelligence**
>
> A full-stack prototype for monitoring an industrial machine, exploring
> what-if operating conditions, and turning sensor readings into risk-aware
> recommendations.

TwinSphere pairs a **React dashboard** with a **FastAPI service**. It stores
digital-twin and sensor records in a SQLAlchemy-supported database, then
computes temperature estimates, threshold-based anomalies, operational risk,
scenario outcomes, and action recommendations.

> **Important:** TwinSphere is a prototype, not a validated industrial control
> or safety system. Its model is trained on generated example data, and its
> thresholds and recommendations have not been certified for real equipment.
> Do not use it to control machinery or replace an operator's judgment.

## At a glance

| Area | Implementation |
| --- | --- |
| Frontend | React 19, Vite 8, Recharts |
| Backend | Python 3.10+, FastAPI, Pydantic, SQLAlchemy |
| Prediction | scikit-learn pipeline: `StandardScaler` + `RandomForestRegressor` |
| Storage | Database URL configured with `DATABASE_URL`; SQLAlchemy models create their tables on API startup |
| API reference | FastAPI Swagger UI at `/docs` and ReDoc at `/redoc` |
| Local web app | Vite dev server at `http://localhost:5173` |
| Local API | Uvicorn at `http://127.0.0.1:8000` |

## What the dashboard shows

The supplied frontend screenshot is a **visual example**, not a promise of
seeded or live readings. It shows:

- Current temperature, vibration, power usage, and operating speed.
- The selected twin's stored status and a separately computed operational
  risk summary.
- Recent sensor history and prediction-feedback performance.
- Additional dashboard sections for analytics, what-if scenarios, decisions,
  reinforcement-learning recommendations, and action planning.

The screenshot's example readings are **82.3 °C**, vibration **3.9**, power
usage **18.7**, and operating speed **1520**. With the code's current
thresholds, 82.3 °C contributes 15 points and the other three readings
contribute none, so the calculated risk is **15 / medium**, with elevated
temperature as the risk factor. The displayed twin status (`normal`) is a
stored status field; it is not the same thing as the calculated risk level.
The screenshot's prediction-performance figures are not project defaults and
cannot be independently verified from the screenshot.

## Why TwinSphere?

Operational teams often have to translate separate sensor values into a
decision. TwinSphere brings a small set of those steps into one prototype:

1. Store readings against a named digital twin.
2. See the latest recorded condition and its history.
3. Flag threshold exceedances and calculate a rule-based risk score.
4. Compare possible changed conditions before choosing an action.
5. Record predicted-versus-actual outcomes to summarize prediction error.

This is useful as a learning, demonstration, or extension project: it shows
how an API, a simple data model, analytical services, and a dashboard can fit
together without claiming to be a production predictive-maintenance platform.

## Capabilities and how they work

### Sensor-to-dashboard flow

The backend accepts readings with `digital_twin_id`, `temperature`,
`vibration`, `power_usage`, and `operating_speed`. It stores readings with a
recorded timestamp and updates the digital twin's current state. The dashboard
loads the overview and sensor history from the API.

### Temperature prediction

`POST /predictions/` builds and fits a model for the request using 1,000
deterministically generated synthetic records. The target is a generated
next-temperature value based on the input features plus noise. The pipeline is
a `StandardScaler` followed by a 100-tree random forest (`random_state=42`).
This is a reproducible demonstration model, **not a model trained on the
machine's stored sensor history**; it is rebuilt when the prediction endpoint
is called.

### Anomaly detection and risk

Anomaly checks compare sensor values to fixed upper thresholds:

| Reading | Anomaly threshold |
| --- | ---: |
| Temperature | > 90 °C |
| Vibration | > 5 |
| Power usage | > 25 |
| Operating speed | > 1800 |

Risk is computed separately using tiered rules. The score adds points for
elevated or high readings; levels are `low` (under 15), `medium` (15–29),
`high` (30–59), and `critical` (60 or more). These are application rules, not
calibrated failure probabilities.

### What-if simulation and recommendations

The simulation endpoints apply caller-supplied changes to the four readings.
Scenario simulation calculates a risk result for each changed state. Separate
services can select a recommended action, allocate resources, and create an
action plan from risk and scenario information. They are decision-support
logic; the API does not itself actuate machinery.

### Historical analysis and feedback

The API includes historical causal analysis, a linear temperature trend and
next-step forecast, a recommendation endpoint named reinforcement learning,
and comparisons of predicted and actual temperatures. Feedback records support
an average absolute error summary and a learning-status check. The learning
status endpoint reports whether the average error exceeds its configurable
threshold; it does **not** automatically retrain or deploy a model.

## Architecture

```mermaid
flowchart LR
    Operator[Operator] --> UI[React + Vite dashboard]
    UI -->|HTTP / JSON| API[FastAPI]
    API --> TwinAPI[Digital twin and sensor routes]
    API --> Analytics[Prediction, risk, simulation, and feedback services]
    TwinAPI --> DB[(SQLAlchemy database)]
    Analytics --> DB
    Analytics -->|JSON results| UI
```

## Project layout

```text
TwinSphere/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route modules
│   │   ├── db/           # SQLAlchemy engine and session dependency
│   │   ├── ml/           # Synthetic data and prediction pipeline
│   │   ├── models/       # Digital twin, sensor, and feedback tables
│   │   ├── schemas/      # API request and response models
│   │   └── services/    # Risk, simulation, analytics, and decision logic
│   ├── requirements.txt
│   └── test_db.py        # Database connection smoke check
├── frontend/
│   ├── src/
│   │   ├── components/  # Dashboard and feature panels
│   │   └── services/    # Axios API helpers
│   ├── package.json
│   └── package-lock.json
└── readme.md
```

## Prerequisites

- Python **3.10 or newer**. The source uses Python 3.10 type syntax.
- Node.js **20.19+**, **22.13+**, or **24+**, matching the Vite version recorded
  in the lockfile.
- npm, included with Node.js.
- A database supported by SQLAlchemy. SQLite is convenient for a local
  demonstration; PostgreSQL is also supported when configured with a valid
  SQLAlchemy URL and the included PostgreSQL driver.

## Local setup and use

The following are instructions for running the app yourself; **the project was
not started as part of preparing this README**.

### 1. Configure the backend

In PowerShell, from the repository root:

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create or update `backend/.env` (it is ignored by Git) with a `DATABASE_URL`.
For a local SQLite file named `twinsphere.db` in the backend directory:

```dotenv
DATABASE_URL=sqlite:///./twinsphere.db
```

Alternatively, configure a PostgreSQL connection using the SQLAlchemy
`postgresql+psycopg2://user:password@host:port/database` URL form. Keep real
credentials in your local environment file or secret manager; do not commit
them.

### 2. Start the API

Run from the `backend` directory with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Visit
`http://127.0.0.1:8000/docs` for interactive API documentation or
`http://127.0.0.1:8000/health` for its health endpoint. On startup,
`app.main` creates the declared database tables. It does **not** seed a
digital twin or sensor readings.

### 3. Create a twin and add readings

Before the dashboard can show its overview, create at least one digital twin.
In Swagger UI (`/docs`), use `POST /digital-twins/` with:

```json
{
  "name": "Factory Machine 01",
  "entity_type": "Industrial Machine",
  "temperature": 75.0,
  "vibration": 3.0,
  "power_usage": 17.0,
  "operating_speed": 1450,
  "status": "normal"
}
```

Record the returned `id`, then use `POST /sensor-data/` with that ID:

```json
{
  "digital_twin_id": 1,
  "temperature": 82.3,
  "vibration": 3.9,
  "power_usage": 18.7,
  "operating_speed": 1520
}
```

Replace `1` with the actual ID returned by your API. Add more readings to
populate the history chart and to satisfy historical analytics, which require
at least two or three records depending on the endpoint.

### 4. Start the frontend

Open a **second** PowerShell terminal at the repository root:

```powershell
cd frontend
npm ci
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`). The
frontend currently calls the API at `http://127.0.0.1:8000`; the backend CORS
configuration permits the default Vite origins `localhost:5173` and
`127.0.0.1:5173`.

### 5. Explore the API

Useful endpoints include:

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | API health response |
| `GET` | `/dashboard/overview` | Latest twin state, risk, and learning status |
| `GET`, `POST` | `/digital-twins/` | List or create digital twins |
| `GET`, `POST` | `/sensor-data/` | List or record sensor readings |
| `POST` | `/predictions/` | Predict next temperature |
| `POST` | `/predictions/anomaly` | Check threshold exceedances |
| `POST` | `/predictions/risk` | Calculate rule-based operational risk |
| `POST` | `/predictions/scenarios` | Simulate multiple changed states |
| `POST` | `/predictions/decision` | Recommend an action from scenario results |
| `POST` | `/predictions/causal-analysis?digital_twin_id={id}` | Analyze historical sensor factors (requires at least 2 records) |
| `POST` | `/predictions/time-series?digital_twin_id={id}` | Analyze and forecast temperature (requires at least 3 records) |
| `GET` | `/predictions/reinforcement-learning?digital_twin_id={id}` | Get the action-selection result for the latest sensor record |
| `GET` | `/predictions/simulation-vs-actual` | Compare stored feedback with actual outcomes |
| `POST`, `GET` | `/feedback/` | Submit or list action feedback |
| `GET` | `/feedback/accuracy` | Summarize prediction errors from feedback |
| `GET` | `/feedback/learning-status` | Check the error threshold and retraining recommendation |

The complete request/response schemas and remaining prediction routes are
available in Swagger UI.

## Testing and verification

No project checks were run while writing this README, in accordance with the
request not to run the project. To check it locally:

### Frontend static checks

From `frontend/`:

```powershell
npm run lint
npm run build
```

These run ESLint and create the production bundle; neither command starts the
development server.

### Backend service smoke scripts

From `backend/`, with the backend dependencies installed:

```powershell
python -m app.services.test_risk_analysis
python -m app.services.test_anomaly_detection
python -m app.services.test_simulation
python -m app.services.test_scenario_simulation
python -m app.services.test_decision_engine
python -m app.services.test_resource_allocation
python -m app.services.test_action_planning
python -m app.ml.test_prediction
```

These checked-in `test_*.py` modules are executable smoke/demo scripts, not a
configured pytest or unittest suite. `backend/test_db.py` is a separate
database-connection smoke check and requires `DATABASE_URL` to be set. For an
end-to-end manual check, start the API, create a twin and sensor readings as
above, then inspect `/dashboard/overview` and try the prediction endpoints in
`/docs`.

## Comparison with common alternatives

This is a **capability and scope comparison**, not a benchmark. No competing
products were installed or measured, and no claim of superior accuracy,
performance, or reliability is implied.

| Approach | Typical strength | TwinSphere's distinction | Trade-off |
| --- | --- | --- | --- |
| Spreadsheet or manual monitoring | Flexible, familiar, low setup | Combines records, a live API, and a dashboard with computed risk and scenario tools | Requires local app and database setup; rules and model need validation |
| Threshold-only monitoring | Clear, easy-to-explain alerts | Adds trend, prediction, scenario, and action/feedback workflows alongside fixed thresholds | More moving parts; the synthetic prediction model is not a validated plant model |
| General-purpose dashboard | Broad visualization and data-source integrations | Focuses this prototype on digital-twin records and predictive decision-support endpoints | Not a replacement for mature observability, asset, or industrial monitoring platforms |
| Commercial industrial digital-twin / predictive-maintenance platforms | Often offer production integrations, asset workflows, and vendor support | TwinSphere is a small, inspectable full-stack codebase suited to experimentation | Does not include demonstrated PLC/SCADA integration, deployment operations, model governance, or certified safety controls |

Choose TwinSphere for a local prototype or an educational starting point. For
operational deployment, first validate the model and thresholds against
representative, labeled equipment data and add security, monitoring, and
appropriate industrial safety controls.

## Known limitations and integration notes

- **Synthetic prediction training data:** Generated records are used instead
  of fitting from the saved sensor history. Prediction output is illustrative,
  not a performance guarantee.
- **Fixed rules:** Anomaly and risk thresholds are constants in the backend;
  they are not configured per machine or learned from feedback.
- **No seed data:** Create a digital twin and post readings before the main
  dashboard overview can load.
- **History prerequisites:** Causal analysis needs at least two records;
  time-series analysis needs at least three. Some analytics can therefore be
  unavailable for a newly created twin.
- **Local-only API URL:** Frontend requests use a hard-coded
  `http://127.0.0.1:8000` base URL. A different deployment requires updating
  the frontend and backend CORS origins.
- **Feedback URL mismatch in dashboard:** The backend feedback router is
  mounted at `/feedback`, and the shared frontend API helper uses that path.
  `Dashboard.jsx` also contains a request to `/action-feedback/accuracy`,
  which does not match the backend route and can make that dashboard analytics
  request fail. The backend's actual accuracy endpoint is
  `/feedback/accuracy`.
- **Not an actuator:** Recommendations and action plans are returned as data;
  this code does not operate physical equipment.
- **No authentication shown:** The current API does not configure user
  authentication or authorization. Do not expose it publicly without adding
  appropriate access controls.

## License

No license file is currently present in the repository. Check with the
project owner before redistributing or reusing the code.