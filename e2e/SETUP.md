# Quick Setup Guide

## 1. Install Dependencies

```bash
uv sync --extra dev
```

## 2. Install Playwright Browsers

```bash
uv run playwright install
```

Or install only Chromium (faster for CI):
```bash
uv run playwright install chromium
```

## 3. Verify Setup

Run the example test:
```bash
ENV_FILE=.env uv run pytest e2e/tests/test_example.py -v
```

**Note**: Make sure you have a `.env` file with all required environment variables (see README.md in project root for setup instructions).

