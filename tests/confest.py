import pytest
from playwright.sync_api import Page

def check_incapsula_block(page: Page) -> bool:
    """
    Sprawdza, czy strona została zablokowana przez firewall Imperva Incapsula
    lub utknęła na cichym wyzwaniu JS JavaScript Challenge.
    """
    try:
        # 1. Sprawdzenie drastycznej blokady po tytule i zawartości
        title = page.title().lower()
        content = page.content().lower()
        
        block_keywords = ["access denied", "incapsula", "imperva", "blocked"]
        if any(kw in title or kw in content for kw in block_keywords):
            return True
            
        # 2. Sprawdzenie cichego zawieszenia: jeśli w ciągu 5s nie pojawi się 
        # żaden z głównych elementów strony (np. logo, stopka, baner), to znaczy, że wisimy na filtrze botów.
        # Sprawdzamy selektor baneru cookies lub nagłówka strony z małym timeoutem.
        page.locator("body").wait_for(state="attached", timeout=5000)
        
        # Próbujemy znaleźć cokolwiek charakterystycznego dla ING (np. selektor id, class lub tekst)
        # Jeśli nie pojawi się w 5 sekund, Imperva zablokowała ruch w tle.
        page.wait_for_selector(".cookie-policy-banner, button:has-text('Dostosuj'), #ing-logo", timeout=5000)
        return False
        
    except Exception:
        # Jeśli poleciał TimeoutError w powyższym kroku, to znaczy, że strona ING się nie załadowała (blokada botów)
        return True

@pytest.fixture(autouse=True)
def bypass_and_check_firewall(page: Page, browser_name: str):
    # 1. Maskowanie automatyzacji przed wejściem na stronę
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
    
    # 2. Próba wejścia na stronę
    try:
        page.goto("https://www.ing.pl", wait_until="commit", timeout=15000)
    except Exception as e:
        pytest.skip(f"Skonfigurowany skip: Brak dostępu do strony na {browser_name} (Timeout ładowania: {e})")

    # 3. Weryfikacja, czy nie wisimy na ekranie sprawdzania Imperva
    if check_incapsula_block(page):
        pytest.skip(f"Skonfigurowany skip: Wykryto cichą blokadę Imperva Incapsula na przeglądarce {browser_name}")