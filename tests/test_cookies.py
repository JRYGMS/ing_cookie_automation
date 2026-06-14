import pytest
from playwright.sync_api import Page, BrowserContext, TimeoutError as PlaywrightTimeoutError


def check_and_skip_if_blocked(page: Page, context: BrowserContext, browser_name: str):
    """Wykrywa blokadę anty-bot (np. Imperva Incapsula) i pomija test tylko w uzasadnionym przypadku."""
    cookies_before = {cookie["name"] for cookie in context.cookies()}
    print(f"[DEBUG] Cookies przed testem: {cookies_before}")

    try:
        page.get_by_role("button", name="Dostosuj").wait_for(state="visible", timeout=7000)
        return  

    except PlaywrightTimeoutError as e:
        cookies_after = {cookie["name"] for cookie in context.cookies()}
        is_blocked = any("incap_ses" in c for c in cookies_after)

        if is_blocked:
            print(f"[CI/CD BLOKADA] Wykryto Incapsula na {browser_name}.")
            pytest.skip(f"Test pominięty z powodu blokady anty-botowej na {browser_name}.")
        raise e


def test_ing_cookies_acceptance(page: Page, context: BrowserContext):
    browser_name = page.context.browser.browser_type.name
    print(f"Uruchomiono test na przeglądarce: {browser_name.upper()}")

    page.goto("https://www.ing.pl/", timeout=30000)

    check_and_skip_if_blocked(page, context, browser_name)

    cookies_before = {cookie["name"] for cookie in context.cookies()}

    page.get_by_role("button", name="Dostosuj").click()

   
    page.locator("div:nth-child(2) > .cookie-policy-switch > .cookie-policy-toggle-button > .cookie-policy-toggle-slider").click()

    
    accept_button = page.get_by_role("button", name="Zaakceptuj zaznaczone")
    accept_button.click()


    accept_button.wait_for(state="hidden", timeout=7000)

    cookies_after = {cookie["name"] for cookie in context.cookies()}
    new_cookies = set(cookies_after) - set(cookies_before)

    print(f"[DEBUG] Cookies po teście: {cookies_after}")
    print(f"[DEBUG] Nowe cookies: {new_cookies}")

    assert new_cookies, "Brak cookies po interakcji z bannerem"
    assert "cookiePolicyGDPR" in new_cookies, "Brak cookiePolicyGDPR po akceptacji cookies"
    assert "cookiePolicyGDPR__details" in new_cookies, "Brak cookiePolicyGDPR__details po akceptacji cookies"

    print("[OK] Cookies GDPR zostały poprawnie zapisane.")