"""Tests for the unregister endpoint."""

import pytest


class TestUnregisterEndpoint:
    """Test cases for the POST /activities/{activity_name}/unregister endpoint."""

    def test_unregister_student_success(self, client):
        """
        Test: Successfully unregistering a student from an activity.
        
        AAA Pattern:
        - Arrange: Use existing participant in Chess Club
        - Act: Send unregister request
        - Assert: Verify response is 200 and message is correct
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]

    def test_unregister_removes_participant_from_activity(self, client):
        """
        Test: Unregistering should remove participant from activity's list.
        
        AAA Pattern:
        - Arrange: Use existing participant
        - Act: Unregister student and check activities
        - Assert: Participant should no longer be in list
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email not in activities[activity]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test: Unregistering from non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Define non-existent activity
        - Act: Send unregister request
        - Assert: Verify 404 status and error message
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "NonexistentClub"

        # Act
        response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered_student_returns_404(self, client):
        """
        Test: Unregistering a student not in the activity returns 404.
        
        AAA Pattern:
        - Arrange: Define activity and student not in it
        - Act: Try to unregister the student
        - Assert: Verify 404 status and error message
        """
        # Arrange
        email = "notstudent@mergington.edu"  # Not in any activity
        activity = "Soccer"

        # Act
        response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_then_signup_again(self, client):
        """
        Test: Student can sign up again after unregistering.
        
        AAA Pattern:
        - Arrange: Prepare student email and activity
        - Act: Sign up, unregister, then sign up again
        - Assert: Verify student is in participants list at the end
        """
        # Arrange
        email = "student@mergington.edu"
        activity = "Soccer"

        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        client.post(f"/activities/{activity}/unregister", params={"email": email})
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity]["participants"]

    def test_unregister_response_format(self, client):
        """
        Test: Unregister response should have correct format.
        
        AAA Pattern:
        - Arrange: Prepare a participant to unregister
        - Act: Send unregister request
        - Assert: Verify response format
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)

    def test_unregister_twice_returns_404_on_second_attempt(self, client):
        """
        Test: Unregistering twice should fail on the second attempt.
        
        AAA Pattern:
        - Arrange: Prepare a participant
        - Act: Unregister once (success), then unregister again (should fail)
        - Assert: First succeeds (200), second fails (404)
        """
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Act
        response1 = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404
