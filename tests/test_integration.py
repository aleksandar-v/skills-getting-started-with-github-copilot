"""Integration tests for multi-endpoint workflows."""

import pytest


class TestIntegrationWorkflows:
    """Test cases for workflows spanning multiple endpoints."""

    def test_signup_then_view_participant_in_activity(self, client):
        """
        Test: Complete workflow - signup and verify in activity list.
        
        AAA Pattern:
        - Arrange: Prepare student email and activity
        - Act: Sign up student, then get activities
        - Assert: Verify student appears in activity participants
        """
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Soccer"

        # Act
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert signup_response.status_code == 200
        assert email in activities[activity]["participants"]

    def test_signup_unregister_and_signup_again_workflow(self, client):
        """
        Test: Complete workflow - signup, unregister, and signup again.
        
        AAA Pattern:
        - Arrange: Prepare student email and activity
        - Act: Sign up, unregister, get activities, sign up again
        - Assert: Verify participant count changes appropriately
        """
        # Arrange
        email = "workflow@mergington.edu"
        activity = "Soccer"

        # Act
        # First signup
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response1 = client.get("/activities")
        count_after_signup = len(response1.json()[activity]["participants"])

        # Unregister
        client.post(f"/activities/{activity}/unregister", params={"email": email})
        response2 = client.get("/activities")
        count_after_unregister = len(response2.json()[activity]["participants"])

        # Signup again
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response3 = client.get("/activities")
        count_after_second_signup = len(response3.json()[activity]["participants"])

        # Assert
        assert count_after_signup > count_after_unregister
        assert count_after_second_signup == count_after_signup
