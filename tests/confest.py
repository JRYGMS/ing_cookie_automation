import pytest
from playwright.sync_api import Page, BrowserContext
@pytest.fixture(scope="session")

def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "locale": "pl-PL",
        "timezone_id": "Europe/Warsaw",
        "viewport": {"width": 1920, "height": 1080},
        'extra_http_headers': {
            "Accept-Language": "pl-PL,pl;q=0.9, en-US;q=0.8, en;q=0.7"
        }
    }

def check_incapsula_block(page: Page, context: BrowserContext):
    page.goto("https://www.ing.pl/", wait_until="domcontentloaded", timeout=60000)
    page.add_init_script("delete navigator.__proto__.webdriver;")
    cookies = [cookie['name'] for cookie in context.cookies()]


    try:
        page.get_by_role('button', name='Dostosuj').wait_for(state='visible', timeout=20000)
    except Exception:
        if "incap_ses" in "".join(cookies) and not page.get_by_role('button', name='Dostosuj').is_visible():
            print(f'[CI/CD BLOKADA] Imperva Incapsula zablokowała publiczny adres IP Github')
            pytest.skip("Test pominięty z powodu blokady Imperva Incapsula")