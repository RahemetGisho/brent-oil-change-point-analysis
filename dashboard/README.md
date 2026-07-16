# Brent Oil Change Point Dashboard

A full-stack, production-structured dashboard for exploring how major
geopolitical and economic events relate to structural breaks in Brent crude
oil prices — built on top of the Task 1 (EDA + event research) and Task 2
(Bayesian change-point modeling) analysis in `../notebooks`.

**Stack:** Flask REST API (`backend/`) + React/Recharts SPA (`frontend/`).

## Architecture

```
dashboard/
├── backend/     # Flask REST API — see backend/README.md
│   ├── app/
│   │   ├── api/            # prices, change-points, events, metrics blueprints
│   │   └── data/           # offline pipeline + generated JSON/CSV artifacts
│   └── tests/               # 17 pytest tests, all endpoints covered
├── frontend/    # React + Recharts SPA — see frontend/README.md
│   └── src/
│       ├── components/      # chart, filters, KPI cards, event list/drawer
│       └── hooks/           # data-fetching hooks per API resource
```

Design principle: the Bayesian change-point models and Markov-switching fit
(both computationally expensive) run **offline** via
`backend/app/data/build_data_artifacts.py`, producing static JSON artifacts
that the API serves instantly. The API never re-runs MCMC sampling on a
request — this is how you'd actually deploy an ML-backed dashboard.

## Quickstart (both servers)

```bash
# Terminal 1 — backend
cd dashboard/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app/data/build_data_artifacts.py   # generates the data artifacts (~1 min)
python run.py                              # http://localhost:5001

# Terminal 2 — frontend
cd dashboard/frontend
npm install
cp .env.example .env
npm run dev                                # http://localhost:5173
```

Open http://localhost:5173.

## Key dashboard features (mapped to the task brief)

| Requirement                             | Implementation                                                                                        |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Historical trends & event correlation   | Price chart with change-point reference lines + event markers; Event Calendar panel                   |
| Event highlight functionality           | Clicking an event highlights its date window on the chart (`ReferenceArea`) and opens a detail drawer |
| Drill-down capability                   | Event detail drawer shows before/after price, % change, volatility, and expected-vs-actual direction  |
| Filters & date range selection          | Category dropdown + date range inputs with quick crisis presets; chart `Brush` for local zoom         |
| Key indicators (volatility, avg change) | KPI cards row: latest/mean price, overall volatility, turbulent-regime share, change-point date       |
| Responsive (desktop/tablet/mobile)      | CSS Grid + breakpoints at 1180px/720px/480px — see screenshots above                                  |

## Testing

```bash
cd backend && pytest tests/ -v      # 17 tests
cd frontend && npm run build         # production build must succeed with 0 errors
```

Both were run and passed before this was committed.
