"""
E2E test for user login and course assignment verification.
"""

import re
import pytest
from playwright.sync_api import Page, expect

from apps.courses.tests.factories import (
    CourseFactory,
    MetaCourseFactory,
    SemesterFactory,
    AssignmentFactory,
)
from apps.users.tests.factories import CuratorFactory


@pytest.mark.e2e
@pytest.mark.django_db
def test_user_login_and_course_assignment_verification(page: Page, base_url):
    """Test user login flow and course assignment verification."""
    # Setup test data
    meta_course = MetaCourseFactory(name="ABOBA", slug="Abobik")
    semester = SemesterFactory(year=2025, type="autumn")
    course = CourseFactory(id=2, meta_course=meta_course, semester=semester)
    # Create at least one assignment for the course
    AssignmentFactory(course=course)

    # Create user with staff privileges
    user = CuratorFactory(username="Aboba", email="aboba@test.com", is_staff=True)
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

    username_input.fill("Aboba")
    password_input.fill(password)
    submit_button.click()

    # Wait for navigation after login
    page.wait_for_load_state("networkidle")

    # Click Courses navigation link
    courses_link = page.locator('a[href="/courses/"]').first
    courses_link.click()

    # Wait for navigation to courses list
    page.wait_for_load_state("networkidle")

    # Assert on courses list page
    expect(page).to_have_url(f"{base_url}/courses/")

    # Click ABOBA course link
    course_link = page.locator(
        'a[href="/courses/2025-autumn/2-Abobik/"], a.__course:has-text("ABOBA")'
    ).first
    course_link.click()

    # Wait for navigation to course detail page
    page.wait_for_load_state("networkidle")

    # Assert on course detail page URL
    expect(page).to_have_url(f"{base_url}/courses/2025-autumn/2-Abobik/")

    # Assert page title contains course name and semester
    expect(page).to_have_title(re.compile(r"ABOBA, autumn 2025"))

    # Assert Add Assignment button is visible and has correct text
    add_assignment_button = page.locator(
        'a[href="/courses/2025-autumn/2-Abobik/assignments/add"], a.btn:has-text("Add assignment")'
    ).first
    expect(add_assignment_button).to_be_visible()
    expect(add_assignment_button).to_contain_text("Add assignment")
