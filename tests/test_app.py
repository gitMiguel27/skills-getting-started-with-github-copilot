from urllib.parse import quote


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_for_activity(client):
    activity_name = "Chess Club"
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    data = client.get("/activities").json()
    assert email in data[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_from_activity(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    data = client.get("/activities").json()
    assert email not in data[activity_name]["participants"]


def test_signup_invalid_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Activity/signup?email=student@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_activity_returns_404(client):
    response = client.delete("/activities/Unknown%20Activity/signup?email=student@mergington.edu")
    assert response.status_code == 404


def test_unregister_missing_participant_returns_404(client):
    activity_name = "Chess Club"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
