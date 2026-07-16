# Brent Oil Dashboard — Backend (Flask API)

REST API serving precomputed Bayesian change-point analysis results (price
history, PyMC change-point models, Markov-switching regimes, and event
correlation data) to the React frontend in `../frontend`.

## Architecture

The heavy statistical work (MCMC sampling, Markov-switching EM fitting) runs
**offline**, once, via `app/data/build_data_artifacts.py` — not on each
request. The Flask app then just reads and serves the resulting JSON/CSV
artifacts from `app/data/`, cached in memory (`functools.lru_cache`) after
the first read. This is standard production practice for ML-backed APIs:
train/fit offline, serve fast.

```
backend/
├── app/
│   ├── __init__.py        # create_app() factory, blueprint registration, CORS
│   ├── config.py          # environment-driven config (dev/prod/testing)
│   ├── errors.py          # consistent JSON error responses
│   ├── data/
│   │   ├── build_data_artifacts.py  # offline pipeline -> JSON/CSV artifacts
│   │   ├── loader.py                # cached accessors for the artifacts
│   │   ├── prices.csv               # generated
│   │   ├── events.json              # generated
│   │   ├── change_points.json       # generated
│   │   ├── markov_regimes.json      # generated
│   │   └── event_impact.json        # generated
│   └── api/
│       ├── prices.py       # GET /api/v1/prices, /api/v1/prices/summary
│       ├── changepoints.py # GET /api/v1/change-points, /api/v1/regimes
│       ├── events.py       # GET /api/v1/events, /api/v1/events/<id>
│       └── metrics.py      # GET /api/v1/metrics
├── tests/                  # pytest, 17 tests covering every endpoint
├── requirements.txt
├── run.py                  # dev server entry point
└── wsgi.py                 # production entry point (gunicorn wsgi:app)
```

## Setup

```bash
cd dashboard/backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## (Re)generating the data artifacts

Only needed if the underlying analysis changes (new events, refit models).
Takes about a minute — fits both PyMC change-point models and the
Markov-switching model against `../../data/processed/`.

```bash
python app/data/build_data_artifacts.py
```

## Running

```bash
python run.py                    # http://localhost:5001, debug=True
# or, production:
gunicorn -w 2 -b 0.0.0.0:5001 wsgi:app
```

## Testing

```bash
pytest tests/ -v                 # 17 tests
```

## API Reference

All endpoints are prefixed `/api/v1` and return JSON.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/prices?start=&end=&resample=D\|W\|M` | Historical price series, optionally date-filtered and resampled |
| GET | `/prices/summary?start=&end=` | Min/max/mean/latest price for the (optionally filtered) range |
| GET | `/change-points` | PyMC mean-shift and volatility-shift change-point results |
| GET | `/regimes` | Markov-switching turbulent-regime windows |
| GET | `/events?category=&start=&end=` | Event calendar, each merged with its empirical price/volatility impact |
| GET | `/events/categories` | Distinct event categories (for filter UI) |
| GET | `/events/<id>` | Single event detail + impact |
| GET | `/metrics` | Headline KPIs combining price, volatility, and change-point data |

Example:

```bash
curl "http://localhost:5001/api/v1/events?category=Conflict"
curl "http://localhost:5001/api/v1/prices?start=2020-01-01&end=2020-06-01&resample=W"
```
