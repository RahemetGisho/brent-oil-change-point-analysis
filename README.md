# Brent Oil Price Change Point Analysis

Bayesian change point analysis of Brent crude oil prices (1987–2022), studying how major geopolitical events, conflicts, sanctions, and OPEC policy decisions relate to structural shifts in the market. Built for Birhan Energies to support investment, policy, and operational decision-making.

## Project Structure

```
├── .github/workflows/      # CI: unit tests on push/PR
├── .vscode/
├── data/
├── notebooks/
├── reports/                # Task 1 & 2 reports + figures
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
jupyter notebook notebooks/eda.ipynb              # exploratory data analysis
jupyter notebook notebooks/change_point_model.ipynb # Bayesian change point modeling
pytest tests/ -v                                       # run tests
```

## Data

- `data/raw/BrentOilPrices.csv` — daily Brent prices (USD/barrel), 20 May 1987 – 14 Nov 2022.
- `data/processed/key_events.csv` — 17 major events (conflicts, OPEC/OPEC+ decisions, sanctions, economic shocks) with approximate dates, for comparison against detected change points.

## Methodology

1. Load & clean price data (mixed date formats normalized).
2. Exploratory analysis: trend, stationarity (ADF/KPSS), volatility clustering.
3. Compile a structured event dataset.
4. Fit Bayesian change point models (PyMC) — a mean-shift model on price level and a volatility-shift model on log returns — with a discrete-uniform prior over the switch point; sample via MCMC and check convergence (r_hat, trace plots).
5. Cross-validate with an independent Markov-switching model (statsmodels).
6. Compare posterior change-point dates against known events — as **temporal association**, not proof of causation.
