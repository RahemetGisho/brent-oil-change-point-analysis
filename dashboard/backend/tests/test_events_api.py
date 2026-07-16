def test_list_events(client):
    r = client.get("/api/v1/events")
    assert r.status_code == 200
    body = r.get_json()
    assert body["count"] >= 15
    assert "impact" in body["data"][0]


def test_list_events_filtered_by_category(client):
    r = client.get("/api/v1/events?category=Conflict")
    assert r.status_code == 200
    body = r.get_json()
    assert body["count"] > 0
    assert all(e["category"] == "Conflict" for e in body["data"])


def test_list_events_filtered_by_date_range(client):
    r = client.get("/api/v1/events?start=2020-01-01&end=2022-12-31")
    body = r.get_json()
    assert all("2020" <= e["start_date"][:4] <= "2022" for e in body["data"])


def test_get_event_detail(client):
    r = client.get("/api/v1/events/6")
    assert r.status_code == 200
    body = r.get_json()
    assert body["id"] == 6
    assert "impact" in body
    assert body["impact"]["price_before"] is not None


def test_get_event_not_found(client):
    r = client.get("/api/v1/events/9999")
    assert r.status_code == 404


def test_categories(client):
    r = client.get("/api/v1/events/categories")
    assert r.status_code == 200
    cats = r.get_json()["categories"]
    assert "Conflict" in cats
    assert cats == sorted(cats)
