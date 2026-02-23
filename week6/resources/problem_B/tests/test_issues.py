from fastapi.testclient import TestClient
from mini_issues.app.main import app

client = TestClient(app)

def test_filter_by_status_open_only_returns_open():
    r = client.get("/issues", params={"status": "open"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert all(item["status"] == "open" for item in data["items"])

def test_pagination_default_limit_offset_shape():
    r = client.get("/issues")
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"items", "total", "limit", "offset"}
    assert data["limit"] == 20
    assert data["offset"] == 0
    assert data["total"] == 5
    assert len(data["items"]) == 5

def test_pagination_limit_offset():
    r = client.get("/issues", params={"limit": 2, "offset": 1})
    assert r.status_code == 200
    data = r.json()
    assert data["limit"] == 2
    assert data["offset"] == 1
    assert data["total"] == 5
    assert len(data["items"]) == 2
    # default sort desc by created_at (all equal), stable: expect IDs 2 and 3 due to insertion order
    assert [x["id"] for x in data["items"]] == [2, 3]

def test_sort_priority_asc():
    r = client.get("/issues", params={"sort": "priority", "order": "asc"})
    assert r.status_code == 200
    data = r.json()
    prios = [x["priority"] for x in data["items"]]
    assert prios == sorted(prios)

def test_sort_title_desc():
    r = client.get("/issues", params={"sort": "title", "order": "desc"})
    assert r.status_code == 200
    data = r.json()
    titles = [x["title"] for x in data["items"]]
    assert titles == sorted(titles, reverse=True)