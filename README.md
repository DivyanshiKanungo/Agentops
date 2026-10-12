# sustainIQ — KAUSHAL PS-04 Backend

FastAPI backend for simulated sustainability telemetry, CSV ingestion, and
consumption analytics. On first startup it creates the SQLite tables and seeds
36 clearly labelled simulated electricity readings across three locations.
Seed data is inserted only once and is labelled with `source_type: "sample"`.
Previously created demo readings labelled `simulated_seed` remain intact and
are also reported as sample provenance.

## Setup

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

The API is available at:
- Health: http://127.0.0.1:8001/health
- Docs: http://127.0.0.1:8001/docs

## Phase 2 data APIs

- `GET /api/v1/locations` and `POST /api/v1/locations`
- `POST /api/v1/readings` creates a manual reading; provide `location_id` or a
  `location_name` (a new named location is created if needed).
- `GET /api/v1/readings` returns a paginated `items`, `total`, `limit`, and
  `offset` response and supports `location_id` and `resource_type` filters.
- `GET /api/v1/readings/{reading_id}` retrieves a single reading.
- `POST /api/v1/upload/csv` requires `location_name`, `resource_type`,
  `quantity`, `unit`, and `recorded_at` columns. Uploads are all-or-nothing;
  invalid files produce a failed batch with row-level errors and import no
  readings.
- `GET /api/v1/upload/{batch_id}` retrieves upload status and counts.
- `GET /locations` and `POST /locations`
- `GET /readings` supports `location_id`, `resource_type`, `start_at`,
  `end_at`, `limit`, and `offset` filters.
- `POST /readings` creates a manual reading.
- `POST /readings/upload` is a compatibility alias for the versioned CSV upload
  and uses the same all-or-nothing policy and required headers.
- `GET /uploads` lists CSV import batches and their accepted/rejected counts.

## Phase 3 analytics APIs

- `GET /api/v1/dashboard/summary` calculates period totals, observed-day
  averages, provenance and comparison with the immediately preceding
  equal-duration period. If that comparison period is absent, its baseline is
  unavailable rather than fabricated.
- `GET /api/v1/telemetry/trends?metric=energy&period=12m` returns ordered
  monthly kWh totals, null-valued missing months, coverage and a derived
  selected-period observed mean. Only interval-consumption readings in kWh are
  aggregated; cumulative readings are not supported.
- `GET /api/v1/analysis` returns explainable preceding-period and peer
  comparisons with source reading evidence. Elevated consumption is not
  treated as proof of wastage or equipment failure.
- `GET /analytics/dashboard` returns period totals, average daily usage,
  preceding-period comparison, daily trend, location breakdown, and findings.
- `GET /analytics/history` returns the daily series for charting.
- `GET /analytics/findings` returns rule-based baseline findings.

Analytics default to electricity and the last seven UTC calendar days. The
baseline is the preceding period of equal length. Average daily consumption is
calculated over days with readings, and each unit is reported separately so
unlike units are never summed together. Findings flag changes of at least 5%
overall and 10% for an individual location.

### CSV example

```csv
location_name,resource_type,quantity,unit,recorded_at
Block A,electricity,840,kWh,2026-10-12T10:00:00Z
```

## Phase 4 relationship graph

- `GET /api/v1/graph?period=12m` builds stable location, reading, and derived
  finding nodes from stored records. Its edges reference only included nodes.

## Phase 5 recommendations and impact

- `GET /api/v1/recommendations` derives explainable actions from analysis
  findings. Optional filters: `location_id`, `category`, `priority`,
  `resource_type`, and reporting period.
- `GET /api/v1/recommendations/{recommendation_id}` retrieves a generated
  recommendation and its evidence.
- `GET /api/v1/impact/summary` reports measured current-versus-baseline
  differences in resource units. Differences are comparisons, not achieved or
  guaranteed savings. No carbon factor or currency rate is assumed.
- Graph recommendations link to their supporting findings. The API does not
  emit projected impact nodes because there is no intervention model or
  defensible savings factor.

## Phase 6 reports and validation

- `GET /api/v1/reports/summary` combines location and resource totals, monthly
  coverage, comparisons, findings, recommendations, impact limitations, and
  data provenance.
- `GET /api/v1/reports/export.csv` exports stored readings and their source
  labels. Optional filters: `resource_type`, `location_id`, `start_date`, and
  `end_date`.
- Run tests with `python -m pytest -q` from the `backend` directory.

## Demo flow

1. Start the backend and open `/docs`.
2. Check `/health`; startup creates tables and idempotently seeds 36 sample
   monthly electricity readings for Block A, Block B, and Library.
3. Browse `/api/v1/readings`, then review dashboard summary, telemetry, and
   analysis.
4. View evidence-based recommendations, impact limitations, and the graph.
5. Generate the report summary or download the CSV export.

Sample readings are simulated, uploaded readings are labelled `uploaded`, and
manual readings are labelled `manual`. Estimates do not claim verified savings,
carbon reductions, or financial outcomes.
