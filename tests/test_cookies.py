import pytest
from playwright.sync_api import Page, BrowserContext

def test_ing_cookies_acceptance(page: Page, context: BrowserContext):

    browser_name = page.context.browser.browser_type.name
    print(f'Uruchomiono test na przeglądarce: {browser_name.upper()}')
    page.goto("https://www.ing.pl/", wait_until="commit", timeout=60000)

    cookie_before = [cookie['name'] for cookie in context.cookies()]
    print(f'[BADANIE] Ciasteczka przed rozpoczęciem testu: {cookie_before}')

    page.get_by_role('button', name='Dostosuj').click()

    page.locator('div:nth-child(2) > .cookie-policy-switch > .cookie-policy-toggle-button > .cookie-policy-toggle-slider > .cookie-policy-slider-thumb').click()

    page.get_by_role('button', name='Zaakceptuj zaznaczone').click()
    page.wait_for_timeout(1000)

    all_cookies = context.cookies()
    cookie_names = [cookie['name'] for cookie in all_cookies]
    print(f'[BADANIE] Ciasteczka po zakończeniu testu: {cookie_names}')

    new_cookies =set(cookie_names) - set(cookie_before)
    print(f'[BADANIE] Nowe ciasteczka: {new_cookies}')

    assert len(all_cookies) > 0, "Nie zapisano jakichkolwiek ciasteczek w pamięci"

    assert 'cookiePolicyGDPR' in new_cookies, (
        "Nie znaleziono ciasteczka analitycznego "
    )
    
    assert 'cookiePolicyGDPR__details' in new_cookies, (
        "Nie znaleziono szczegółów dla ciasteczka analitycznego "
    )

    print(f'[WYNIK ANALIZY] Po włączeniu analityki w pamięci przybyły {list(new_cookies)}')