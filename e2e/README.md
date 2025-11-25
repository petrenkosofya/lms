# E2E Tests with Playwright

End-to-end UI tests using Playwright and pytest.

## Setup

1. Install dependencies:
```bash
uv sync --extra dev
```

2. Install Playwright browsers:
```bash
uv run playwright install
```

Or install only specific browsers:
```bash
uv run playwright install chromium
uv run playwright install firefox
uv run playwright install webkit
```

## Running Tests

**Important**: Tests require environment variables. Use `.env` file or set `ENV_FILE`:

```bash
ENV_FILE=.env uv run pytest e2e/
```

### Run all e2e tests
```bash
ENV_FILE=.env uv run pytest e2e/
```

### Run specific test by name (аналог -Dtest={TEST_ID})
```bash
ENV_FILE=.env uv run pytest e2e/ -k "login"
ENV_FILE=.env uv run pytest e2e/ -k "test_login_page"
```

### Run specific test file
```bash
ENV_FILE=.env uv run pytest e2e/tests/test_example.py
```

### Run specific test function
```bash
ENV_FILE=.env uv run pytest e2e/tests/test_example.py::test_homepage_loads
```

### Run tests by marker
```bash
# Run only smoke tests
ENV_FILE=.env uv run pytest e2e/ -m smoke

# Run only critical tests
ENV_FILE=.env uv run pytest e2e/ -m critical

# Run smoke or critical tests
ENV_FILE=.env uv run pytest e2e/ -m "smoke or critical"
```

### Run tests in headed mode (see browser)
Modify `browser` fixture in `e2e/conftest.py`:
```python
browser = browser_type.launch(
    headless=False,  # Change to False
    slow_mo=0,
)
```

### Run tests with specific browser
To change browser, modify `browser_type` fixture in `e2e/conftest.py`:
```python
@pytest.fixture(scope="session")
def browser_type(playwright):
    return playwright.chromium  # or playwright.firefox, playwright.webkit
```

### Run tests in parallel
```bash
uv run pytest e2e/ -n auto
```

### Run tests with screenshots on failure
Screenshots are automatically saved on test failure. Check `test-results/` directory.

To take manual screenshots in tests:
```python
page.screenshot(path="screenshot.png")
```

### Run tests with video recording
To enable video recording, modify `browser_context` fixture in `e2e/conftest.py`:
```python
context = browser.new_context(
    viewport={"width": 1920, "height": 1080},
    ignore_https_errors=True,
    locale="en-US",
    record_video_dir="test-results/videos/",  # Add this
)
```

## Test Structure

Tests are located in `e2e/tests/` directory. Each test file should:
- Start with `test_` prefix
- Use `@pytest.mark.e2e` marker
- Use appropriate markers (`@pytest.mark.smoke`, `@pytest.mark.critical`)

## Fixtures

### Available fixtures:

- `page: Page` - Playwright page object
- `base_url` - Base URL of the test server (from live_server)
- `live_server` - Django live server fixture (from pytest-django)
- `authenticated_page: Page` - Pre-authenticated page with test user
- `browser_type_launch_args` - Browser launch configuration
- `browser_context_args` - Browser context configuration

## Example Test

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
def test_login(page: Page, base_url):
    page.goto(f"{base_url}/login/")
    page.fill('input[name="username"]', "testuser")
    page.fill('input[name="password"]', "password")
    page.click('button[type="submit"]')
    expect(page).to_have_url(containing="/dashboard/")
```

## Debugging

### Run in debug mode
```bash
PLAYWRIGHT_HEADED=1 PLAYWRIGHT_DEBUG=1 uv run pytest e2e/ -k "test_name"
```

### Use Playwright Inspector
```bash
PLAYWRIGHT_HEADED=1 PLAYWRIGHT_DEBUG=pw:api uv run pytest e2e/ -k "test_name"
```

### Pause execution
Add `page.pause()` in your test code to open Playwright Inspector.

## CI/CD

For CI/CD, ensure browsers are installed:
```bash
uv run playwright install --with-deps chromium
```

Then run tests (set required environment variables):
```bash
ENV_FILE=.env uv run pytest e2e/
```

