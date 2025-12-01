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
from e2e.pages.login_page import LoginPage
from e2e.pages.course_page import CourseListPage, CourseDetailPage


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
    if password != "12345":
        user.set_password("12345")
        user.save()
        password = "12345"

    # Navigate to login page
    login_page = LoginPage(page)
    login_page.navigate(f"{base_url}/login/")
    login_page.login("Aboba", password)

    # Click Courses navigation link
    course_list_page = CourseListPage(page)
    course_list_page.go_to_courses()

    # Assert on courses list page
    expect(page).to_have_url(f"{base_url}/courses/")

    # Click ABOBA course link
    course_list_page.go_to_course("ABOBA")

    # Assert on course detail page URL
    expect(page).to_have_url(f"{base_url}/courses/2025-autumn/2-Abobik/")

    # Assert page title contains course name and semester
    expect(page).to_have_title(re.compile(r"ABOBA, autumn 2025"))

    # Assert Add Assignment button is visible and has correct text
    course_detail_page = CourseDetailPage(page)
    expect(course_detail_page.add_assignment_button).to_be_visible()
    expect(course_detail_page.add_assignment_button).to_contain_text("Add assignment")
