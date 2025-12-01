"""
E2E test for password reset flow with invalid email validation.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.django_db
def test_password_reset_invalid_email_validation(page: Page, base_url):
    """Test password reset form validation with invalid email format."""
    # Navigate to login page
    page.goto(f"{base_url}/login/")
    page.wait_for_load_state("networkidle")

    # Click forgot password link
    forgot_password_link = page.locator(
        'a.forgot[href="/password_reset/"], a[href="/password_reset/"]'
    ).first
    forgot_password_link.click()
    page.wait_for_load_state("networkidle")

    # Assert password recovery heading is visible
    password_recovery_heading = page.locator(
        '#reset-password h4, h4:has-text("Password recovery")'
    ).first
    expect(password_recovery_heading).to_be_visible()
    expect(password_recovery_heading).to_contain_text("Password recovery")

    # Fill email input with invalid email
    email_input = page.locator(
        '#id_email, input[name="email"], input[type="text"][id*="email"]'
    ).first
    email_input.fill("something")

    # Click restore password button
    restore_button = page.locator(
        'input[type="submit"][value="Restore password"], #reset-password input[type="submit"], button[type="submit"]'
    ).first
    restore_button.click()
    page.wait_for_load_state("networkidle")

    # Assert error message is visible and contains correct text
    error_message = page.locator(
        '.error-message, #id_email + .error-message, label[for="id_email"] .error-message'
    ).first
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Enter a valid email address.")
