"""
E2E test for staff user login, navigation, and gradebook access.
"""

import pytest
from playwright.sync_api import Page, expect

from apps.courses.tests.factories import (
    CourseFactory,
    MetaCourseFactory,
    SemesterFactory,
)
from apps.users.tests.factories import CuratorFactory


@pytest.mark.e2e
@pytest.mark.django_db
def test_staff_login_navigation_and_gradebook_access(page: Page, base_url):
    """Test staff user login flow, navigation through staff pages, and gradebook access."""
    # Setup test data
    meta_course = MetaCourseFactory(name="Test Course", slug="some-slug")
    semester = SemesterFactory(year=2025, type="autumn")
    course = CourseFactory(id=3, meta_course=meta_course, semester=semester)

    # Create staff user
    user = CuratorFactory(username="test_user", email="test@test.com", is_staff=True)
    password = getattr(user, "raw_password", "12345")
    # Override password if needed
    if password != "12345":
        user.set_password("12345")
        user.save()
        password = "12345"

    # Navigate to login page
    page.goto(f"{base_url}/login/")
    page.wait_for_load_state("networkidle")

    # Fill login form
    username_input = page.locator(
        'input[name="username"], input[type="text"][id*="username"], #id_username'
    ).first
    password_input = page.locator(
        'input[name="password"], input[type="password"], #id_password'
    ).first
    submit_button = page.locator(
        'input[type="submit"], button[type="submit"], button:has-text("Sign in")'
    ).first

    username_input.fill("test_user")
    password_input.fill(password)
    submit_button.click()

    # Wait for navigation after login
    page.wait_for_load_state("networkidle")

    # Assert successful login redirects to student search page
    expect(page).to_have_url(f"{base_url}/staff/student-search/")

    # Resources navigation
    resources_link = page.locator('a[href="/staff/warehouse/"]').first
    resources_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{base_url}/staff/warehouse/")

    # Overlaps navigation
    overlaps_link = page.locator('a[href="/staff/course-participants/"]').first
    overlaps_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{base_url}/staff/course-participants/")

    # Files navigation
    files_link = page.locator('a[href="/staff/exports/"]').first
    files_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{base_url}/staff/exports/")

    # Gradebooks navigation
    gradebooks_link = page.locator('a[href="/staff/gradebooks/"]').first
    gradebooks_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{base_url}/staff/gradebooks/")

    # Courses navigation
    courses_link = page.locator('a[href="/courses/"]').first
    courses_link.click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{base_url}/courses/")

    # Return to Gradebooks
    gradebooks_link = page.locator('a[href="/staff/gradebooks/"]').first
    gradebooks_link.click()
    page.wait_for_load_state("networkidle")

    # Click on Test Course in gradebooks list
    course_link = page.locator(
        'a[href="/staff/gradebooks/2025-autumn/3-some-slug/"], a:has-text("Test Course")'
    ).first
    course_link.click()
    page.wait_for_load_state("networkidle")

    # Assert on gradebook page URL
    expect(page).to_have_url(f"{base_url}/staff/gradebooks/2025-autumn/3-some-slug/")

    # Assert Save button is visible
    save_button = page.locator('#marks-sheet-save, button[type="submit"]:has-text("Save")').first
    expect(save_button).to_be_visible()

    # Assert Download CSV button is visible
    csv_download_button = page.locator(
        'a.marks-sheet-csv-link, a[href="/staff/gradebooks/2025-autumn/3-some-slug/csv/"]'
    ).first
    expect(csv_download_button).to_be_visible()
