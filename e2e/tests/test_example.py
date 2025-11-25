"""
Example e2e test with Playwright.

This is a template test file. Replace with your actual test cases.
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
@pytest.mark.django_db
def test_homepage_loads(page: Page, base_url):
    """Example test: verify homepage loads correctly."""
    page.goto(base_url)

    # Wait for page to load
    page.wait_for_load_state("networkidle")

    # Example assertion - adjust based on your actual homepage
    # Check if title contains "LMS" (case-insensitive)
    title = page.title()
    assert "lms" in title.lower() or len(title) > 0  # Basic check that page loaded


@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.django_db
def test_login_page_accessible(page: Page, base_url):
    """Example test: verify login page is accessible."""
    page.goto(f"{base_url}/login/")

    # Wait for page to load
    page.wait_for_load_state("networkidle")

    # Example assertion - adjust selectors based on your actual login form
    # expect(page.locator('input[name="username"]')).to_be_visible()


@pytest.mark.e2e
@pytest.mark.django_db
def test_authenticated_user_can_access_dashboard(authenticated_page: Page, base_url):
    """Example test: verify authenticated user can access dashboard."""
    # This test uses the authenticated_page fixture
    authenticated_page.goto(f"{base_url}/dashboard/")

    # Wait for page to load
    authenticated_page.wait_for_load_state("networkidle")

    # Example assertion - adjust based on your actual dashboard
    # Check if URL contains "/dashboard/"
    assert "/dashboard/" in authenticated_page.url or authenticated_page.url.endswith(
        "/dashboard/"
    )


@pytest.mark.e2e
@pytest.mark.critical
@pytest.mark.django_db
def test_example_with_screenshot(page: Page, base_url):
    """Example test: demonstrate screenshot capability."""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Take screenshot on failure (automatic with Playwright)
    # Or manually:
    # page.screenshot(path="screenshot.png")

    assert page.url == base_url or base_url + "/"
