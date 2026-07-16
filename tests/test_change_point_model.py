import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from change_point_model import (  # noqa: E402
    build_mean_shift_model,
    build_variance_shift_model,
    sample_model,
    summarize_shift,
)


def _synthetic_mean_shift(n=200, break_at=100, mu1=0.0, mu2=5.0, sigma=0.5, seed=0):
    rng = np.random.default_rng(seed)
    series = np.concatenate(
        [
            rng.normal(mu1, sigma, break_at),
            rng.normal(mu2, sigma, n - break_at),
        ]
    )
    return series


def test_build_mean_shift_model_has_expected_vars():
    series = _synthetic_mean_shift()
    model = build_mean_shift_model(series)
    var_names = {v.name for v in model.free_RVs}
    assert {"tau", "mu1", "mu2", "sigma"}.issubset(var_names)


def test_build_variance_shift_model_has_expected_vars():
    series = _synthetic_mean_shift(mu1=0.0, mu2=0.0, sigma=0.2)
    model = build_variance_shift_model(series)
    var_names = {v.name for v in model.free_RVs}
    assert {"tau", "mu", "sigma1", "sigma2"}.issubset(var_names)


def test_sampler_recovers_known_break_point():
    """On a clean synthetic mean-shift series, the sampler should find tau
    close to the true break point (within a small tolerance)."""
    n, break_at = 200, 100
    series = _synthetic_mean_shift(n=n, break_at=break_at, mu1=0.0, mu2=8.0, sigma=0.3)
    model = build_mean_shift_model(series)
    trace = sample_model(model, draws=300, tune=300, chains=2, random_seed=1)
    tau_samples = trace.posterior["tau"].values.flatten()
    tau_mode = int(np.bincount(tau_samples).argmax())
    assert abs(tau_mode - break_at) <= 5


def test_summarize_shift_returns_expected_keys():
    n, break_at = 150, 75
    series = _synthetic_mean_shift(n=n, break_at=break_at, mu1=0.0, mu2=3.0, sigma=0.3)
    model = build_mean_shift_model(series)
    trace = sample_model(model, draws=200, tune=200, chains=2, random_seed=2)
    result = summarize_shift(trace, "mu1", "mu2")
    for key in [
        "mu1_mean",
        "mu2_mean",
        "absolute_change_mean",
        "pct_change_mean",
        "prob_increase",
    ]:
        assert key in result
    # mu2 (~3.0) should be clearly larger than mu1 (~0.0)
    assert result["mu2_mean"] > result["mu1_mean"]
