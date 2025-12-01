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
from e2e.pages.login_page import LoginPage
from e2e.pages.staff_page import StaffPage, GradebookPage
from e2e.pages.course_page import CourseListPage


@pytest.mark.e2e
@pytest.mark.django_db
def test_staff_login_navigation_and_gradebook_access(page: Page, base_url):
    """Test staff user login flow, navigation through staff pages, and gradebook access."""
    # Setup test data
    meta_course = MetaCourseFactory(name="Test Course", slug="some-slug")
    semester = SemesterFactory(year=2025, type="autumn")
    _ = CourseFactory(id=3, meta_course=meta_course, semester=semester)

    # Create staff user
    user = CuratorFactory(username="test_user", email="test@test.com", is_staff=True)
    password = getattr(user, "raw_password", "12345")
    if password != "12345":
        user.set_password("12345")
        user.save()
        password = "12345"

    # Navigate to login page
    login_page = LoginPage(page)
    login_page.navigate(f"{base_url}/login/")
    login_page.login("test_user", password)

    # Assert successful login redirects to student search page
    expect(page).to_have_url(f"{base_url}/staff/student-search/")

    staff_page = StaffPage(page)

    # Resources navigation
    staff_page.go_to_resources()
    expect(page).to_have_url(f"{base_url}/staff/warehouse/")

    # Overlaps navigation
    staff_page.go_to_overlaps()
    expect(page).to_have_url(f"{base_url}/staff/course-participants/")

    # Files navigation
    staff_page.go_to_files()
    expect(page).to_have_url(f"{base_url}/staff/exports/")

    # Gradebooks navigation
    staff_page.go_to_gradebooks()
    expect(page).to_have_url(f"{base_url}/staff/gradebooks/")

    # Courses navigation
    course_list_page = CourseListPage(page)
    course_list_page.go_to_courses()
    expect(page).to_have_url(f"{base_url}/courses/")

    # Return to Gradebooks
    staff_page.go_to_gradebooks()

    # Click on Test Course in gradebooks list
    gradebook_page = GradebookPage(page)
    gradebook_page.open_course_gradebook("Test Course")

    # Assert on gradebook page URL
    expect(page).to_have_url(f"{base_url}/staff/gradebooks/2025-autumn/3-some-slug/")

    # Assert Save button is visible
    expect(gradebook_page.save_button).to_be_visible()

    # Assert Download CSV button is visible
    expect(gradebook_page.csv_download_button).to_be_visible()
