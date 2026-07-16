# Brent Oil Price Change Point Analysis

Bayesian change-point analysis of Brent crude oil prices (1987–2022) — identifying structural breaks in the market and testing how closely they align with major conflicts, sanctions, and OPEC decisions. Includes a Flask + React dashboard for exploring the results interactively.

## Project Structure

```
├── data/                    # raw + cleaned prices, compiled event calendar
├── notebooks/               # eda.ipynb, change_point_model.ipynb
├── src/                     # data loading, EDA, PyMC change-point models
├── tests/                   # pytest
├── reports/                 # Word reports
└── dashboard/
    ├── backend/              # Flask REST API
    └── frontend/             # React + Recharts SPA
```

## Quickstart

```bash
git clone https://github.com/RahemetGisho/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis
python -m venv .venv && .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Run the analysis:**

```bash
jupyter notebook notebooks/eda.ipynb                 # exploratory analysis
jupyter notebook notebooks/change_point_model.ipynb  # Bayesian change-point modeling
pytest tests/ -v                                        # 12 tests
```

**Run the dashboard** (needs two terminals):

```bash
# Terminal 1 — backend
cd dashboard/backend
pip install -r requirements.txt
python app/data/build_data_artifacts.py   # generates data the API serves (~1 min)
python run.py                              # http://localhost:5001

# Terminal 2 — frontend
cd dashboard/frontend
npm install
cp .env.example .env
npm run dev                                # http://localhost:5173
```

Open http://localhost:5173. Full dashboard details, API reference, and screenshots: [`dashboard/README.md`](dashboard/README.md).

## Key Findings

- Price levels are non-stationary (ADF p ≈ 0.29); log returns are stationary but fat-tailed with strong volatility clustering (2008–09, 2014–16, 2020).
- **Mean-shift change point:** 23 Feb 2005 — average price $21.42 → $75.61/barrel (+253%), consistent with the 2003–2008 commodity supercycle.
- **Volatility-shift change point:** 20 Aug 2008 — daily volatility 2.30% → 2.89% (+25%), closely preceding the Lehman Brothers collapse.
- **Markov-switching cross-check:** independently recovers 11 turbulent windows, 3 matching compiled events to within 0–1 day (2008 GFC, 2020 Saudi-Russia price war, 2022 Ukraine invasion).

Every finding is a **temporal association**, not proof of causation — see `reports/Final_Report_Brent_Oil_Change_Point_Analysis.docx` for the full writeup and caveats.
