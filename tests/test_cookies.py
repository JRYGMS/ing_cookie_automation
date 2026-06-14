import pytest
from playwright.sync_api import Page

def test_ing_cookies_acceptance(page: Page):
   
    browser_name = page.context.browser.browser_type.name
    print(f'Uruchomiono test na przeglądarce: {browser_name.upper()}')


    cookie_before = [cookie['name'] for cookie in page.context.cookies()]
    print(f'[BADANIE] Ciasteczka przed rozpoczęciem testu: {cookie_before}')

    
    page.get_by_role('button', name='Dostosuj').click()
    page.locator('div:nth-child(2) > .cookie-policy-switch > .cookie-policy-toggle-button > .cookie-policy-toggle-slider > .cookie-policy-slider-thumb').click()    
    page.get_by_role('button', name='Zaakceptuj zaznaczone').click()
    page.wait_for_timeout(1000)

    
    all_cookies = page.context.cookies()
    cookie_names = [cookie['name'] for cookie in all_cookies]
    print(f'[BADANIE] Ciasteczka po zakończeniu testu: {cookie_names}')

    new_cookies = set(cookie_names) - set(cookie_before)
    print(f'[BADANIE] Nowe ciasteczka analityczne: {new_cookies}')

    
    assert len(all_cookies) > 0, "Nie zapisano jakichkolwiek ciasteczek w pamięci" 
    assert 'cookiePolicyGDPR' in cookie_names, "Nie znaleziono ciasteczka analitycznego cookiePolicyGDPR"
    assert 'cookiePolicyGDPR__details' in cookie_names, "Nie znaleziono szczegółów ciasteczka analitycznego cookiePolicyGDPR__details"

    print(f'[WYNIK ANALIZY] Po włączeniu analityki w pamięci znajdują się kluczowe ciasteczka GDPR.')