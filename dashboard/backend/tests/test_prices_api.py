def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_list_prices_default(client):
    r = client.get("/api/v1/prices?start=2020-01-01&end=2020-01-10")
    assert r.status_code == 200
    body = r.get_json()
    assert body["resample"] == "D"
    assert body["count"] > 0
    assert set(body["data"][0].keys()) == {"date", "price"}


def test_list_prices_weekly_resample_has_fewer_points(client):
    daily = client.get("/api/v1/prices?start=2020-01-01&end=2020-03-01").get_json()
    weekly = client.get("/api/v1/prices?start=2020-01-01&end=2020-03-01&resample=W").get_json()
    assert weekly["count"] < daily["count"]


def test_list_prices_invalid_resample_returns_400(client):
    r = client.get("/api/v1/prices?resample=invalid")
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_prices_summary(client):
    r = client.get("/api/v1/prices/summary")
    assert r.status_code == 200
    body = r.get_json()
    for key in ["start_date", "end_date", "count", "min", "max", "mean", "latest"]:
        assert key in body
    assert body["min"] <= body["mean"] <= body["max"]


def test_prices_summary_empty_range_returns_404(client):
    r = client.get("/api/v1/prices/summary?start=2099-01-01")
    assert r.status_code == 404
