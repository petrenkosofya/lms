"""
E2E test for password reset flow with invalid email validation.
"""

import pytest
from playwright.sync_api import Page

from e2e.pages.login_page import LoginPage
from e2e.pages.password_reset_page import PasswordResetPage


@pytest.mark.e2e
@pytest.mark.django_db
def test_password_reset_invalid_email_validation(page: Page, base_url):
    """Test password reset form validation with invalid email format."""
    # Navigate to login page
    login_page = LoginPage(page)
    login_page.navigate(f"{base_url}/login/")

    # Click forgot password link
    password_reset_page = PasswordResetPage(page)
    password_reset_page.go_to_forgot_password()

    # Assert password recovery heading is visible
    password_reset_page.verify_recovery_heading_visible()

    # Fill email input with invalid email
    password_reset_page.fill_email("something")

    # Click restore password button
    password_reset_page.submit_restore()

    # Assert error message is visible and contains correct text
    password_reset_page.verify_error_message("Enter a valid email address.")
