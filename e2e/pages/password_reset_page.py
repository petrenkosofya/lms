from playwright.sync_api import Page, Locator, expect
from e2e.pages.base_page import BasePage

class PasswordResetPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.forgot_password_link = page.locator('a[href="/password_reset/"]')
        self.password_recovery_heading = page.locator('h4:has-text("Password recovery")')
        self.email_input = page.locator('#id_email, input[name="email"]')
        self.restore_button = page.locator('input[type="submit"][value="Restore password"], button[type="submit"]')
        self.error_message = page.locator('.error-message')

    def go_to_forgot_password(self):
        self.forgot_password_link.first.click()
        self.page.wait_for_load_state("networkidle")

    def fill_email(self, email: str):
        self.email_input.first.fill(email)

    def submit_restore(self):
        self.restore_button.first.click()
        self.page.wait_for_load_state("networkidle")

    def verify_recovery_heading_visible(self):
        expect(self.password_recovery_heading.first).to_be_visible()
        expect(self.password_recovery_heading.first).to_contain_text("Password recovery")

    def verify_error_message(self, text: str):
        expect(self.error_message.first).to_be_visible()
        expect(self.error_message.first).to_contain_text(text)


