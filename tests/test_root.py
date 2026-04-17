"""Tests for the root endpoint."""

import pytest


class TestRootEndpoint:
    """Test cases for the GET / endpoint."""

    def test_root_redirect_to_static_html(self, client):
        """
        Test: Root endpoint should redirect to static HTML.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to root endpoint without following redirects
        - Assert: Verify redirect status and location header
        """
        # Arrange
        # (implicit: client fixture is provided)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_can_be_followed(self, client):
        """
        Test: Root endpoint redirect can be followed to reach the static page.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to root endpoint with redirects enabled
        - Assert: Verify we get a successful response (following the redirect)
        """
        # Arrange
        # (implicit: client fixture is provided)

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        # When we follow redirects, we'd get the HTML content
        assert response.status_code == 200
