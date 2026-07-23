from urllib.parse import quote


def test_get_activities_returns_all_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    activity_data = client.get("/activities").json()[activity]
    assert email in activity_data["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Programming Class"
    email = "emma@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity(client):
    # Arrange
    activity = "Gym Class"
    email = "john@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    activity_data = client.get("/activities").json()[activity]
    assert email not in activity_data["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity = "Gym Class"
    email = "missing@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
