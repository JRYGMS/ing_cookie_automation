import pytest
from playwright.sync_api import Page, BrowserContext

def test_ing_cookies_acceptance(page: Page, context: BrowserContext):

    browser_name = page.context.browser.browser_type.name
    print(f'Uruchomiono test na przeglądarce: {browser_name.upper()}')

    page.add_init_script("delete navigator.__proto__.webdriver;")

    page.goto("https://www.ing.pl/", wait_until="domcontentloaded", timeout=60000)

    cookie_before = [cookie['name'] for cookie in context.cookies()]
    print(f'[BADANIE] Ciasteczka przed rozpoczęciem testu: {cookie_before}')

    try:
        page.get_by_role('button', name='Dostosuj').wait_for(state='visible', timeout=20000)
    except Exception:
        if "incap_ses" in "".join(cookie_before) and not page.get_by_role('button', name='Dostosuj').is_visible():
            print(f'[CI/CD BLOKADA] Imperva Incapsula zablokowała publiczny adres IP Github')
            pytest.skip("Test pominięty z powodu blokady Imperva Incapsula")                   
            return 
        else:
            raise AssertionError("Nie znaleziono przycisku baneru cookies, mimo braku blokady firewall") 

    
    page.get_by_role('button', name='Dostosuj').click()

    
    page.locator('div:nth-child(2) > .cookie-policy-switch > .cookie-policy-toggle-button > .cookie-policy-toggle-slider > .cookie-policy-slider-thumb').click()

    
    page.get_by_role('button', name='Zaakceptuj zaznaczone').click()
    page.wait_for_timeout(1000)

    all_cookies = context.cookies()
    cookie_names = [cookie['name'] for cookie in all_cookies]
    print(f'[BADANIE] Ciasteczka po zakończeniu testu: {cookie_names}')

    new_cookies = set(cookie_names) - set(cookie_before)
    print(f'[BADANIE] Nowe ciasteczka analityczne: {new_cookies}')

    
    assert len(all_cookies) > 0, "Nie zapisano jakichkolwiek ciasteczek w pamięci"

    
    assert 'cookiePolicyGDPR' in cookie_names, "Nie znaleziono ciasteczka analitycznego cookiePolicyGDPR"
    assert 'cookiePolicyGDPR__details' in cookie_names, "Nie znaleziono szczegółów ciasteczka analitycznego cookiePolicyGDPR__details"

    print(f'[WYNIK ANALIZY] Po włączeniu analityki w pamięci znajdują się kluczowe ciasteczka GDPR.')