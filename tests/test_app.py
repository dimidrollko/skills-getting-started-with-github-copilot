from urllib.parse import quote

from src.app import activities as activities_data


def get_activity_path(activity_name: str, action: str) -> str:
    encoded_name = quote(activity_name, safe="")
    return f"/activities/{encoded_name}/{action}"


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_names = set(activities_data.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_names


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in activities_data[activity_name]["participants"]
    url = get_activity_path(activity_name, "signup")

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities_data[activity_name]["participants"]


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    url = get_activity_path(activity_name, "signup")

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_existing_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in activities_data[activity_name]["participants"]
    url = get_activity_path(activity_name, "signup")

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_removes_existing_student(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    assert email in activities_data[activity_name]["participants"]
    url = get_activity_path(activity_name, "participants")

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities_data[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    email = "notregistered@mergington.edu"
    assert email not in activities_data[activity_name]["participants"]
    url = get_activity_path(activity_name, "participants")

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
