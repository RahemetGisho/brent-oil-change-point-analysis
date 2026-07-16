# Brent Oil Dashboard — Frontend (React + Recharts)

Interactive dashboard for exploring the Brent crude oil change-point
analysis: historical price trends, detected change points, and how
compiled geopolitical/economic events correlate with price moves.

## Features

- **Interactive price chart** (Recharts) with the two Bayesian change points
  overlaid as reference lines, event markers as clickable dots, and a brush
  for local zoom.
- **Event highlight** — clicking any event (on the chart or in the list)
  highlights its date window on the chart and opens a drill-down detail
  panel with quantified before/after price and volatility impact.
- **Filters** — date range (with quick presets for major crises), and event
  category.
- **KPI cards** — latest/mean price, overall volatility, turbulent-regime
  share, and the primary change-point date at a glance.
- **Change point & regime panels** — the PyMC model results and the
  Markov-switching cross-validation, in plain business language.
- **Responsive** — tested at desktop (1440px), tablet (834px), and mobile
  (390px) widths; see `../screenshots/`.

## Setup

```bash
cd dashboard/frontend
npm install
cp .env.example .env    # point VITE_API_BASE_URL at your backend if not localhost:5001
```

## Running

```bash
npm run dev              # http://localhost:5173, hot reload
```

Requires the Flask backend (`../backend`) running on the URL set in `.env`
(defaults to `http://localhost:5001/api/v1`).

## Building for production

```bash
npm run build             # outputs to dist/
npm run preview           # serve the production build locally to sanity-check
```

## Project structure

```
frontend/
├── src/
│   ├── api/client.js         # fetch wrapper for the Flask API
│   ├── hooks/                # useAsync + one hook per resource (usePrices, useEvents, ...)
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── KpiCards.jsx
│   │   ├── FilterBar.jsx           # date range + category filters
│   │   ├── PriceChart.jsx          # main Recharts chart w/ change points + event markers
│   │   ├── EventList.jsx           # filterable event list
│   │   ├── EventDetailDrawer.jsx   # drill-down panel
│   │   ├── ChangePointSummary.jsx  # PyMC model result cards
│   │   └── RegimePanel.jsx         # Markov-switching regime table
│   ├── utils/format.js       # currency/date/percent formatting, category colors
│   ├── styles/index.css      # design tokens + component styles
│   └── App.jsx
└── package.json
```

## Charting library

Built with [Recharts](https://recharts.org/en-US/), as recommended — chosen
for its declarative React API and built-in `ReferenceLine`/`ReferenceArea`/
`ReferenceDot`/`Brush` primitives, which map directly onto this dashboard's
requirements (change-point markers, event highlight bands, date-range zoom)
without hand-rolling SVG.
