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
from e2e.pages.login_page import LoginPage
from e2e.pages.course_page import CourseListPage, CourseDetailPage
from e2e.pages.assignment_page import AssignmentFormPage, AssignmentDetailPage


@pytest.mark.e2e
@pytest.mark.django_db
def test_create_and_verify_course_assignment(page: Page, base_url):
    """Test creating a course assignment and verifying its details."""
    # --- Data Setup ---
    meta_course = MetaCourseFactory(name="Test Course", slug="some-slug")
    semester = SemesterFactory(year=2025, type="autumn")
    # We don't strictly need the ID to be 3 if we look up by name, but keeping it for consistency with original if needed.
    # The original test used ID in URL, but I updated POM to find by text.
    # However, the POM navigation implementation in CourseListPage assumes finding by text is enough.
    _ = CourseFactory(id=3, meta_course=meta_course, semester=semester)

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

    # --- Login ---
    login_page = LoginPage(page)
    login_page.navigate(f"{base_url}/login/")
    login_page.login("test_user", password)

    # --- Navigate to Course ---
    course_list_page = CourseListPage(page)
    course_list_page.go_to_courses()
    course_list_page.go_to_course("Test Course")

    # --- Create Assignment ---
    course_detail_page = CourseDetailPage(page)
    course_detail_page.go_to_add_assignment()

    assignment_form_page = AssignmentFormPage(page)
    assignment_form_page.fill_assignment_details(
        title="Test",
        text="Some text",
        submission_type="online",
        deadline_date="01.05.2029",
        deadline_time="23:59",
        assignee_mode="off"
    )
    assignment_form_page.submit()

    # --- Verify ---
    assignment_detail_page = AssignmentDetailPage(page)
    
    expect(assignment_detail_page.edit_button).to_be_visible()
    expect(assignment_detail_page.delete_button).to_be_visible()
    
    # Using expect with locators is better than `assert x in content`
    expect(page.locator("text=Some text")).to_be_visible()
    expect(page.locator("text=/01 May 2029/")).to_be_visible()
