def test_metrics_structure(client):
    r = client.get("/api/v1/metrics")
    assert r.status_code == 200
    body = r.get_json()
    for section in ["price", "volatility", "change_points", "counts"]:
        assert section in body


def test_metrics_values_are_sane(client):
    body = client.get("/api/v1/metrics").get_json()
    assert body["price"]["min"] < body["price"]["mean"] < body["price"]["max"]
    assert body["volatility"]["turbulent_regime_pct"] > body["volatility"]["calm_regime_pct"]
    assert body["counts"]["events"] > 0
    assert body["counts"]["trading_days"] > 1000
