"""
E2E test for creating and verifying a course assignment.
"""

import pytest
from zoneinfo import ZoneInfo
from playwright.sync_api import Page, expect

from apps.courses.tests.factories import (
    CourseFactory,
    MetaCourseFactory,
    SemesterFactory,
)
from apps.users.tests.factories import CuratorFactory


@pytest.mark.e2e
@pytest.mark.django_db
def test_create_and_verify_course_assignment(page: Page, base_url):
    """Test creating a course assignment and verifying its details."""
    meta_course = MetaCourseFactory(name="Test Course", slug="some-slug")
    semester = SemesterFactory(year=2025, type="autumn")
    course = CourseFactory(id=3, meta_course=meta_course, semester=semester)

    user = CuratorFactory(
        username="test_user",
        email="test@example.com",
        is_staff=True,
        time_zone=ZoneInfo("UTC"),
    )
    password = getattr(user, "raw_password", "12345")
    if password != "12345":
        user.set_password("12345")
        user.save()
        password = "12345"

    page.goto(f"{base_url}/login/")
    page.wait_for_load_state("networkidle")

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

    page.wait_for_load_state("networkidle")

    courses_link = page.locator('a[href="/courses/"]').first
    courses_link.click()

    page.wait_for_load_state("networkidle")

    course_link = page.locator(
        'a[href="/courses/2025-autumn/3-some-slug/"], a.__course:has-text("Test Course")'
    ).first
    course_link.click()

    page.wait_for_load_state("networkidle")

    add_assignment_button = page.locator(
        'a[href="/courses/2025-autumn/3-some-slug/assignments/add"], a.btn:has-text("Add assignment")'
    ).first
    add_assignment_button.click()

    page.wait_for_load_state("networkidle")

    title_input = page.locator(
        '#id_assignment-title, input[name="assignment-title"]'
    ).first
    title_input.fill("Test")

    text_input = page.locator(
        '#id_assignment-text, textarea[name="assignment-text"]'
    ).first
    text_input.fill("Some text")

    page.evaluate("window.scrollBy(0, 300)")

    format_dropdown = page.locator(
        '#id_assignment-submission_type, select[name="assignment-submission_type"]'
    ).first
    format_dropdown.select_option("online")

    page.evaluate("window.scrollBy(0, 300)")

    deadline_date_input = page.locator(
        '#id_assignment-deadline_at_0, input[name="assignment-deadline_at_0"]'
    ).first
    deadline_date_input.fill("01.05.2029")
    deadline_date_input.press("Enter")

    deadline_time_input = page.locator(
        '#id_assignment-deadline_at_1, input[name="assignment-deadline_at_1"]'
    ).first
    deadline_time_input.fill("23:59")

    page.evaluate("window.scrollBy(0, 300)")

    assignee_mode_dropdown = page.locator(
        '#id_assignment-assignee_mode, select[name="assignment-assignee_mode"]'
    ).first
    assignee_mode_dropdown.select_option("off")

    save_button = page.locator(
        '#submit-id-save, input[type="submit"][name="save"], button[type="submit"]:has-text("Save")'
    ).first
    save_button.click()

    page.wait_for_load_state("networkidle")

    edit_button = page.locator(
        'a.btn.btn-primary[href*="/edit"], a.btn:has-text("Edit")'
    ).first
    expect(edit_button).to_be_visible()

    delete_button = page.locator(
        'a.btn.btn-danger[href*="/delete"], a.btn:has-text("Delete")'
    ).first
    expect(delete_button).to_be_visible()

    page_content = page.content()
    assert "Some text" in page_content

    deadline_display = page.locator("text=/01 May 2029/").first
    expect(deadline_display).to_be_visible()
