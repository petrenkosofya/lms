"""
Pytest configuration and fixtures for e2e tests with Playwright.
"""

import os
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# Allow synchronous Django ORM calls in this environment (Playwright might initialize an event loop)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Import Django user factory for creating test users
from apps.users.tests.factories import UserFactory


@pytest.fixture(scope="session")
def playwright():
    """Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_type(playwright):
    """Browser type (chromium, firefox, webkit)."""
    return playwright.chromium  # Default to chromium


@pytest.fixture(scope="session")
def browser(playwright, browser_type):
    """Browser instance for the test session."""
    browser = browser_type.launch(
        headless=False,
    )
    yield browser
    browser.close()


@pytest.fixture
def browser_context(browser):
    """Browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
        locale="en-US",
    )
    yield context
    context.close()


@pytest.fixture
def page(browser_context):
    """Page object for each test."""
    page = browser_context.new_page()
    page.set_default_timeout(30000)  # 30 seconds
    page.set_default_navigation_timeout(30000)
    yield page
    page.close()


@pytest.fixture
def authenticated_page(page: Page, live_server, django_db_blocker):
    """
    Fixture that provides an authenticated page.

    Creates a test user and logs in via the UI.

    Usage:
        def test_something(authenticated_page, base_url):
            authenticated_page.goto(f"{base_url}/some-page")
    """
    # Create a test user using UserFactory
    # UserFactory sets password to "test123foobar@!" and stores it in raw_password attribute
    # Use django_db_blocker to ensure synchronous access to Django ORM
    with django_db_blocker.unblock():
        user = UserFactory(username="testuser", email="test@example.com")
        password = getattr(user, "raw_password", "test123foobar@!")

    # Navigate to login page
    page.goto(f"{live_server.url}/login/")

    # Fill login form (adjust selectors based on your actual login form)
    # These selectors are examples - update them to match your actual login form
    username_input = page.locator(
        'input[name="username"], input[type="text"][name*="user"], input[id*="username"]'
    ).first
    password_input = page.locator(
        'input[name="password"], input[type="password"]'
    ).first
    submit_button = page.locator(
        'button[type="submit"], input[type="submit"], button:has-text("SIGN IN")'
    ).first

    if username_input.is_visible():
        username_input.fill("testuser")
    if password_input.is_visible():
        password_input.fill(password)
    if submit_button.is_visible():
        submit_button.click()

    # Wait for navigation after login
    page.wait_for_load_state("networkidle")

    return page


@pytest.fixture
def base_url(live_server):
    """Base URL for the test server."""
    return live_server.url


@pytest.fixture(autouse=True)
def setup_test_environment(page: Page):
    """
    Auto-use fixture to set up common test environment.
    Can be used to set cookies, localStorage, etc.
    """
    # Timeouts are already set in the page fixture
    yield

    # Cleanup if needed
    pass
