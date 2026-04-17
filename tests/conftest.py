"""Pytest configuration and shared fixtures for FastAPI testing."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Provides a test client for making HTTP requests to the FastAPI app.
    
    Returns:
        TestClient: A FastAPI test client for the application.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture: Resets the in-memory activities database before each test.
    
    This ensures test isolation by restoring the initial state of activities
    before each test runs.
    
    Yields:
        None
    """
    # Store the original activities data
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer": {
            "description": "Team soccer practice and matches",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": []
        },
        "Basketball": {
            "description": "Basketball training and inter-school competitions",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and creative expression",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and school play productions",
            "schedule": "Mondays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        },
        "Math Olympiad": {
            "description": "Competitive mathematics training and contests",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        }
    }
    
    # Yield control to the test
    yield
    
    # Reset activities after each test
    activities.clear()
    activities.update(original_activities)
