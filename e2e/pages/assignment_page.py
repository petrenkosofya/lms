from playwright.sync_api import Page, Locator
from e2e.pages.base_page import BasePage

class AssignmentFormPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title_input = page.locator('#id_assignment-title, input[name="assignment-title"]')
        self.text_input = page.locator('#id_assignment-text, textarea[name="assignment-text"]')
        self.format_dropdown = page.locator('#id_assignment-submission_type, select[name="assignment-submission_type"]')
        self.deadline_date_input = page.locator('#id_assignment-deadline_at_0, input[name="assignment-deadline_at_0"]')
        self.deadline_time_input = page.locator('#id_assignment-deadline_at_1, input[name="assignment-deadline_at_1"]')
        self.assignee_mode_dropdown = page.locator('#id_assignment-assignee_mode, select[name="assignment-assignee_mode"]')
        self.save_button = page.locator('#submit-id-save, input[type="submit"][name="save"], button[type="submit"]:has-text("Save")')
        
    def fill_assignment_details(self, title: str, text: str, submission_type: str, deadline_date: str, deadline_time: str, assignee_mode: str = "off"):
        self.title_input.first.fill(title)
        self.text_input.first.fill(text)
        
        # Scroll if needed handled by playwright usually, but explicitly scrolling to be safe if obscured
        self.format_dropdown.first.scroll_into_view_if_needed()
        self.format_dropdown.first.select_option(submission_type)
        
        self.deadline_date_input.first.scroll_into_view_if_needed()
        self.deadline_date_input.first.fill(deadline_date)
        self.deadline_date_input.first.press("Enter")
        
        self.deadline_time_input.first.fill(deadline_time)
        
        self.assignee_mode_dropdown.first.scroll_into_view_if_needed()
        self.assignee_mode_dropdown.first.select_option(assignee_mode)
        
    def submit(self):
        self.save_button.first.click()
        self.page.wait_for_load_state("networkidle")

class AssignmentDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.edit_button = page.locator('a.btn:has-text("Edit")')
        self.delete_button = page.locator('a.btn:has-text("Delete")')
        
    def get_content_text(self) -> str:
        # Assuming the content is in the body or a specific container, for now page.content() check
        # But better to return text of a specific element if possible.
        # The original test checked page.content(), let's stick to checking visibility of text
        return self.page.content()

    def has_text(self, text: str):
        return self.page.locator(f"text={text}").first.is_visible()

    def has_deadline(self, date_str: str):
         # Using the regex format from the test: text=/01 May 2029/
         return self.page.locator(f"text=/{date_str}/").first.is_visible()



