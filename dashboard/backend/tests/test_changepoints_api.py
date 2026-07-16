def test_change_points_structure(client):
    r = client.get("/api/v1/change-points")
    assert r.status_code == 200
    body = r.get_json()
    assert "mean_shift" in body and "variance_shift" in body
    for key in ["tau_date", "pct_change", "prob_increase", "max_rhat", "nearest_event"]:
        assert key in body["mean_shift"]
        assert key in body["variance_shift"]


def test_change_points_convergence_is_good(client):
    """r_hat should be close to 1.0 for both models — a sanity check that
    the committed artifact reflects a converged model, not a broken fit."""
    body = client.get("/api/v1/change-points").get_json()
    assert abs(body["mean_shift"]["max_rhat"] - 1.0) < 0.05
    assert abs(body["variance_shift"]["max_rhat"] - 1.0) < 0.05


def test_regimes_structure(client):
    r = client.get("/api/v1/regimes")
    assert r.status_code == 200
    body = r.get_json()
    for key in ["high_volatility_regime_share", "calm_sigma_pct", "turbulent_sigma_pct", "windows"]:
        assert key in body
    assert body["turbulent_sigma_pct"] > body["calm_sigma_pct"]
    assert len(body["windows"]) > 0
    assert "start_date" in body["windows"][0]
