"""Tests for the signup endpoint."""

import pytest


class TestSignupEndpoint:
    """Test cases for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client):
        """
        Test: Successfully signing up a student for an activity.
        
        AAA Pattern:
        - Arrange: Prepare email and activity name
        - Act: Send POST request to signup endpoint
        - Assert: Verify response is 200 and message is correct
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Soccer"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """
        Test: Signing up should add participant to activity's list.
        
        AAA Pattern:
        - Arrange: Define email and activity for signup
        - Act: Sign up student and retrieve activities
        - Assert: Verify participant is in the activity's participant list
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Soccer"

        # Act
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity]["participants"]

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """
        Test: Signing up for a non-existent activity should return 404.
        
        AAA Pattern:
        - Arrange: Define non-existent activity name
        - Act: Send signup request
        - Assert: Verify 404 status and error message
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "NonexistentClub"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student_returns_400(self, client):
        """
        Test: Signing up twice should return 400 (duplicate signup).
        
        AAA Pattern:
        - Arrange: Use existing participant in Chess Club
        - Act: Try to sign up the same student again
        - Assert: Verify 400 status and error message
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_multiple_students_same_activity(self, client):
        """
        Test: Multiple students should be able to sign up for the same activity.
        
        AAA Pattern:
        - Arrange: Define two different students
        - Act: Sign up both students to same activity
        - Assert: Verify both are in the participants list
        """
        # Arrange
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        activity = "Soccer"

        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email1})
        client.post(f"/activities/{activity}/signup", params={"email": email2})
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email1 in activities[activity]["participants"]
        assert email2 in activities[activity]["participants"]

    def test_signup_same_student_different_activities(self, client):
        """
        Test: Same student can sign up for different activities.
        
        AAA Pattern:
        - Arrange: Define one student and two activities
        - Act: Sign up student to both activities
        - Assert: Verify student appears in both activities
        """
        # Arrange
        email = "student@mergington.edu"
        activity1 = "Soccer"
        activity2 = "Basketball"

        # Act
        client.post(f"/activities/{activity1}/signup", params={"email": email})
        client.post(f"/activities/{activity2}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_response_format(self, client):
        """
        Test: Signup response should have correct format.
        
        AAA Pattern:
        - Arrange: Prepare email and activity
        - Act: Send signup request
        - Assert: Verify response format
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Soccer"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
