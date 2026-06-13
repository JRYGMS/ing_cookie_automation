import pytest

@pytest.fixture(scope="session")

def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "locale": "pl-PL",
        "timezone_id": "Europe/Warsaw",
        "viewport": {"width": 1920, "height": 1080},
    }