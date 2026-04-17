"""Tests for the activities retrieval endpoint."""

import pytest


class TestGetActivitiesEndpoint:
    """Test cases for the GET /activities endpoint."""

    def test_get_all_activities_returns_200(self, client):
        """
        Test: Getting all activities should return 200 OK.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities
        - Assert: Verify status code is 200
        """
        # Arrange
        # (implicit: client fixture is provided)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_json(self, client):
        """
        Test: Getting all activities should return valid JSON.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities
        - Assert: Verify response is valid JSON and is a dict
        """
        # Arrange
        # (implicit: client fixture is provided)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_get_activities_contains_all_expected_activities(self, client):
        """
        Test: Response should contain all 9 expected activities.
        
        AAA Pattern:
        - Arrange: Define list of expected activity names
        - Act: Get activities from endpoint
        - Assert: Verify all expected activities are present
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer",
            "Basketball",
            "Art Club",
            "Drama Club",
            "Math Olympiad",
            "Debate Club"
        ]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in activities

    def test_activity_structure_is_correct(self, client):
        """
        Test: Each activity should have the correct structure.
        
        AAA Pattern:
        - Arrange: Define expected activity fields
        - Act: Get activities and inspect first one
        - Assert: Verify all required fields are present
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = activities["Chess Club"]

        # Assert
        for field in required_fields:
            assert field in first_activity

    def test_activity_participants_is_a_list(self, client):
        """
        Test: Participants field should be a list.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Get activities from endpoint
        - Assert: Verify participants field is a list for each activity
        """
        # Arrange
        # (implicit: client fixture is provided)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)

    def test_activity_max_participants_is_integer(self, client):
        """
        Test: max_participants should be an integer.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Get activities from endpoint
        - Assert: Verify max_participants is int for each activity
        """
        # Arrange
        # (implicit: client fixture is provided)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0
