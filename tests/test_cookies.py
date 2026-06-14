import pytest
from playwright.sync_api import Page, BrowserContext

def check_and_skip_if_blocked(page: Page, context: BrowserContext, browser_name: str):
    """Pomocnicza funkcja weryfikująca blokadę firewall (Imperva) przed testem."""
    cookie_before = [cookie['name'] for cookie in context.cookies()]
    print(f'[BADANIE] Ciasteczka przed rozpoczęciem testu: {cookie_before}')

    try:
        page.get_by_role('button', name='Dostosuj').wait_for(state="visible", timeout=7000)
    except Exception:
        
        if any("incap_ses" in name for name in cookie_before):
            print(f'[CI/CD BLOKADA] Wykryto blokadę Imperva Incapsula na {browser_name}.')
            pytest.skip(f"Test pominięty z powodu blokady anty-botowej na {browser_name}.")
        else:
            raise AssertionError(f"Nie znaleziono baneru cookies na {browser_name}, mimo braku blokady.")

def test_ing_cookies_acceptance(page: Page, context: BrowserContext):
    browser_name = page.context.browser.browser_type.name
    print(f'Uruchomiono test na przeglądarce: {browser_name.upper()}')

    
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")

  
    page.goto("https://www.ing.pl/", timeout=30000)

    
    check_and_skip_if_blocked(page, context, browser_name)

    
    page.get_by_role('button', name='Dostosuj').click()
    page.locator('div:nth-child(2) > .cookie-policy-switch > .cookie-policy-toggle-button > .cookie-policy-toggle-slider > .cookie-policy-slider-thumb').click()    
    page.get_by_role('button', name='Zaakceptuj zaznaczone').click()
    page.wait_for_timeout(1000)


    all_cookies = context.cookies()
    cookie_names = [cookie['name'] for cookie in all_cookies]
    print(f'[BADANIE] Ciasteczka po zakończeniu testu: {cookie_names}')

    new_cookies = set(cookie_names) - set([c['name'] for c in context.cookies() if 'incap_ses' not in c['name']])
    print(f'[BADANIE] Nowe ciasteczka analityczne: {new_cookies}')

    assert len(all_cookies) > 0, "Nie zapisano jakichkolwiek ciasteczek w pamięci" 
    assert 'cookiePolicyGDPR' in cookie_names, "Nie znaleziono ciasteczka analitycznego cookiePolicyGDPR"
    assert 'cookiePolicyGDPR__details' in cookie_names, "Nie znaleziono szczegółów ciasteczka analitycznego cookiePolicyGDPR__details"

    print(f'[WYNIK ANALIZY] Po włączeniu analityki w pamięci znajdują się kluczowe ciasteczka GDPR.')