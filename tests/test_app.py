from urllib.parse import quote

from src import app as app_module


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]
    assert activities["Chess Club"]["max_participants"] == 12


def test_signup_activity_success(client):
    email = "newstudent@mergington.edu"
    response = client.post(
        f"/activities/{quote('Chess Club')}/signup?email={quote(email)}"
    )
    assert response.status_code == 200

    body = response.json()
    assert body["message"] == f"Signed up {email} for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]
    assert len(app_module.activities["Chess Club"]["participants"]) == 3


def test_signup_duplicate_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post(
        f"/activities/{quote('Chess Club')}/signup?email={quote(email)}"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert app_module.activities["Chess Club"]["participants"].count(email) == 1


def test_signup_missing_activity_returns_404(client):
    response = client.post(
        f"/activities/{quote('Nonexistent Activity')}/signup?email={quote('x@mergington.edu')}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    email = "michael@mergington.edu"
    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants/{quote(email)}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_400(client):
    email = "notregistered@mergington.edu"
    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants/{quote(email)}"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_remove_from_missing_activity_returns_404(client):
    email = "michael@mergington.edu"
    response = client.delete(
        f"/activities/{quote('No Club')}/participants/{quote(email)}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
