from playwright.sync_api import Page, Locator
from e2e.pages.base_page import BasePage

class StaffPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.student_search_link = page.locator('a[href="/staff/student-search/"]')
        self.resources_link = page.locator('a[href="/staff/warehouse/"]')
        self.overlaps_link = page.locator('a[href="/staff/course-participants/"]')
        self.files_link = page.locator('a[href="/staff/exports/"]')
        self.gradebooks_link = page.locator('a[href="/staff/gradebooks/"]')

    def go_to_resources(self):
        self.resources_link.first.click()
        self.page.wait_for_load_state("networkidle")

    def go_to_overlaps(self):
        self.overlaps_link.first.click()
        self.page.wait_for_load_state("networkidle")

    def go_to_files(self):
        self.files_link.first.click()
        self.page.wait_for_load_state("networkidle")

    def go_to_gradebooks(self):
        self.gradebooks_link.first.click()
        self.page.wait_for_load_state("networkidle")

class GradebookPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.save_button = page.locator('#marks-sheet-save, button[type="submit"]:has-text("Save")')
        self.csv_download_button = page.locator('a.marks-sheet-csv-link')

    def open_course_gradebook(self, course_name: str):
        course_link = self.page.locator(f'a:has-text("{course_name}")')
        course_link.first.click()
        self.page.wait_for_load_state("networkidle")

