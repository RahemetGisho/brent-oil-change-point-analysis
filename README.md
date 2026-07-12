# Brent Oil Price Change Point Analysis

Bayesian change point analysis of Brent crude oil prices (1987–2022), studying how major geopolitical events, conflicts, sanctions, and OPEC policy decisions relate to structural shifts in the market. Built for Birhan Energies to support investment, policy, and operational decision-making.

## Project Structure

```
├── .github/workflows/      # CI: unit tests on push/PR
├── .vscode/
├── data/
├── notebooks/
├── reports/
├── src/
├── tests/                  # unit tests (pytest)
├── scripts/                # CLI entry points (later tasks)
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
jupyter notebook notebooks/eda.ipynb   # run the EDA
pytest tests/ -v                          # run tests
```

## Data

- `data/raw/BrentOilPrices.csv` — daily Brent prices (USD/barrel), 20 May 1987 – 14 Nov 2022.
- `data/processed/key_events.csv` — 17 major events (conflicts, OPEC/OPEC+ decisions, sanctions, economic shocks) with approximate dates, for comparison against detected change points.

## Methodology

1. Load & clean price data (mixed date formats normalized).
2. Exploratory analysis: trend, stationarity (ADF/KPSS), volatility clustering.
3. Compile a structured event dataset.
4. Fit a Bayesian change point model (PyMC) over log returns; sample the posterior via MCMC and check convergence.
5. Compare posterior change-point dates against known events — as **temporal association**, not proof of causation.

## Key EDA Findings

- Price levels are non-stationary (ADF p ≈ 0.29); log returns are stationary (ADF p < 0.001) and are the appropriate scale for modeling.
- Log returns are fat-tailed with strong volatility clustering (visible around 2008–09, 2014–16, 2020), so the model needs to account for shifts in variance, not just mean.
