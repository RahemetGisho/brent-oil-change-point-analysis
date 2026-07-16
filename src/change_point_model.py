"""
change_point_model.py

Bayesian single change point models for Brent oil price analysis, built in PyMC.

Two model variants are provided, motivated by the Task 1 EDA finding that
Brent log returns are roughly zero-mean but highly heteroskedastic:

- build_mean_shift_model: switch-point in the MEAN of a series (used on the
  price level, where a genuine long-run mean shift exists).
- build_variance_shift_model: switch-point in the VOLATILITY of a series
  (used on log returns, where mean is stable but variance regime-shifts).

Both use a discrete-uniform prior over the switch point tau and
pm.math.switch to route each observation to its regime's parameter(s).
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az


@dataclass
class ChangePointResult:
    model: pm.Model
    trace: az.InferenceData
    dates: pd.Series  # date index aligned with the series modeled
    tau_index_mode: int  # most probable switch-point index (0-based)
    tau_date: pd.Timestamp  # corresponding calendar date


def build_mean_shift_model(series: np.ndarray) -> pm.Model:
    """Single change point model for a shift in the MEAN of `series`.

    tau ~ DiscreteUniform(0, n-1)
    mu1, mu2 ~ Normal (regime means)
    sigma ~ HalfNormal (shared observation noise)
    obs ~ Normal(switch(tau >= t, mu1, mu2), sigma)
    """
    n = len(series)
    idx = np.arange(n)
    with pm.Model() as model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n - 1)
        mu1 = pm.Normal("mu1", mu=series.mean(), sigma=series.std() * 2)
        mu2 = pm.Normal("mu2", mu=series.mean(), sigma=series.std() * 2)
        sigma = pm.HalfNormal("sigma", sigma=series.std())
        mu = pm.math.switch(tau >= idx, mu1, mu2)
        pm.Normal("obs", mu=mu, sigma=sigma, observed=series)
    return model


def build_variance_shift_model(series: np.ndarray) -> pm.Model:
    """Single change point model for a shift in the VOLATILITY of `series`.

    tau ~ DiscreteUniform(0, n-1)
    mu ~ Normal (shared mean, e.g. ~0 for log returns)
    sigma1, sigma2 ~ HalfNormal (regime volatilities)
    obs ~ Normal(mu, switch(tau >= t, sigma1, sigma2))
    """
    n = len(series)
    idx = np.arange(n)
    with pm.Model() as model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n - 1)
        mu = pm.Normal("mu", mu=0, sigma=series.std())
        sigma1 = pm.HalfNormal("sigma1", sigma=series.std())
        sigma2 = pm.HalfNormal("sigma2", sigma=series.std())
        sigma = pm.math.switch(tau >= idx, sigma1, sigma2)
        pm.Normal("obs", mu=mu, sigma=sigma, observed=series)
    return model


def sample_model(
    model: pm.Model,
    draws: int = 1500,
    tune: int = 1000,
    chains: int = 4,
    target_accept: float = 0.9,
    random_seed: int = 42,
    cores: int | None = None,
) -> az.InferenceData:
    """Run the NUTS+Metropolis compound sampler and return the trace."""
    import os

    if cores is None:
        cores = max(1, min(chains, os.cpu_count() or 1))
    with model:
        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=cores,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=False,
            return_inferencedata=True,
        )
    return trace


def tau_to_date(trace: az.InferenceData, dates: pd.Series) -> ChangePointResult:
    """Convert the posterior over tau (an integer index) into a calendar date."""
    tau_samples = trace.posterior["tau"].values.flatten()
    mode_idx = int(np.bincount(tau_samples).argmax())
    return mode_idx, dates.iloc[mode_idx]


def summarize_shift(trace: az.InferenceData, param1: str, param2: str) -> dict:
    """Compute the posterior mean shift and percentage change between two regime parameters."""
    p1 = trace.posterior[param1].values.flatten()
    p2 = trace.posterior[param2].values.flatten()
    diff = p2 - p1
    pct_change = 100 * diff / np.abs(p1)
    return {
        f"{param1}_mean": float(p1.mean()),
        f"{param2}_mean": float(p2.mean()),
        "absolute_change_mean": float(diff.mean()),
        "pct_change_mean": float(pct_change.mean()),
        "prob_increase": float((diff > 0).mean()),
    }
