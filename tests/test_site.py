import pytest
from playwright.sync_api import Page, BrowserContext

def test_site_title(page: Page, context: BrowserContext):
    browser_name = page.context.browser.browser_type.name
    print(f'Uruchomiono test na przeglądarce: {browser_name.upper()}')
    
    page.goto("https://www.ing.pl/", wait_until="domcontentloaded", timeout=60000)
    title = page.title()
    print(f'[BADANIE] Tytuł strony: {title}')