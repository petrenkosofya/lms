from playwright.sync_api import Page, Locator
from e2e.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('input[name="username"], input[type="text"][name*="user"], input[id*="username"], #id_username')
        self.password_input = page.locator('input[name="password"], input[type="password"], #id_password')
        self.submit_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("SIGN IN"), button:has-text("Sign in")')

    def login(self, username: str, password: str):
        # Ensure elements are visible before interacting
        if self.username_input.first.is_visible():
             self.username_input.first.fill(username)
        
        if self.password_input.first.is_visible():
            self.password_input.first.fill(password)
            
        if self.submit_button.first.is_visible():
            self.submit_button.first.click()
        
        self.page.wait_for_load_state("networkidle")

