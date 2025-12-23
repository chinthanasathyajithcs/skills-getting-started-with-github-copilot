import pytest


def test_get_activities_ok(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data
    assert "participants" in data["Tennis Club"]


def test_signup_adds_participant(client):
    email = "newstudent@mergington.edu"
    activity = "Tennis Club"

    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert f"Signed up {email} for {activity}" in res.json()["message"]

    # Verify participant now listed
    res2 = client.get("/activities")
    assert email in res2.json()[activity]["participants"]


def test_signup_duplicate_rejected(client):
    activity = "Basketball Team"
    existing = "james@mergington.edu"

    res = client.post(f"/activities/{activity}/signup", params={"email": existing})
    assert res.status_code == 400
    assert res.json()["detail"] == "Student already signed up for this activity"


def test_delete_removes_participant(client):
    activity = "Art Club"
    email = "isabella@mergington.edu"

    # Ensure present
    res0 = client.get("/activities")
    assert email in res0.json()[activity]["participants"]

    # Remove
    res = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert res.status_code == 200
    assert f"Removed {email} from {activity}" in res.json()["message"]

    # Verify gone
    res2 = client.get("/activities")
    assert email not in res2.json()[activity]["participants"]


def test_delete_nonexistent_participant_404(client):
    activity = "Drama Club"
    email = "notregistered@mergington.edu"
    res = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert res.status_code == 404
    assert res.json()["detail"] == "Student not registered for this activity"


def test_signup_activity_not_found_404(client):
    res = client.post("/activities/Unknown Activity/signup", params={"email": "x@y.com"})
    assert res.status_code == 404
    assert res.json()["detail"] == "Activity not found"


def test_delete_activity_not_found_404(client):
    res = client.delete("/activities/Unknown Activity/participants", params={"email": "x@y.com"})
    assert res.status_code == 404
    assert res.json()["detail"] == "Activity not found"