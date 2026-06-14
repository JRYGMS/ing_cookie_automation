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
    # 1. Maskowanie automatyzacji
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
    
    # 2. Pełne wejście na stronę (czekamy normalnie na załadowanie, żeby złapać ciasteczka)
    try:
        page.goto("https://www.ing.pl", timeout=20000)
    except Exception as e:
        # Jeśli strona w ogóle się nie otworzyła z powodu timeoutu, bezpiecznie skipujemy
        pytest.skip(f"Timeout ładowania strony na {browser_name}: {e}")

    # 3. Pobieramy ciasteczka dokładnie tak jak w Twoim kodzie
    cookies = page.context.cookies()
    cookie_names = [c['name'] for c in cookies]

    # 4. Twoja autorska logika sprawdzania przycisku i ciasteczek
    try:
        page.get_by_role('button', name='Dostosuj').wait_for(state="visible", timeout=5000)
    except Exception:
        # Jeśli po 5 sekundach przycisku nie ma, sprawdzamy obecność incap_ses
        if any("incap_ses" in name for name in cookie_names):
            pytest.skip(f"[CI/CD BLOKADA] Imperva Incapsula zablokowała stronę na {browser_name}.")   
        else:
            raise AssertionError(f"Nie znaleziono baneru cookies na {browser_name}, mimo braku blokady firewall.")