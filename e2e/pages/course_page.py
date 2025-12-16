from playwright.sync_api import Page
from e2e.pages.base_page import BasePage

class CourseListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.courses_link = page.locator('a[href="/courses/"]')
    
    def go_to_courses(self):
        self.courses_link.first.click()
        self.page.wait_for_load_state("networkidle")

    def go_to_course(self, course_name: str):
        course_link = self.page.locator(f'a.__course:has-text("{course_name}")')
        course_link.first.click()
        self.page.wait_for_load_state("networkidle")


class CourseDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_assignment_button = page.locator('a.btn:has-text("Add assignment")')
        
    def go_to_add_assignment(self):
        self.add_assignment_button.first.click()
        self.page.wait_for_load_state("networkidle")


