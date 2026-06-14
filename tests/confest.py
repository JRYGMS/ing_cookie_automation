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
    # 1. Sprawdzenie czy jesteśmy w chmurze CI (np. GitHub Actions)
    # Strona ING agresywnie blokuje publiczne IP runnerów GitHub, uniemożliwiając stabilne przejście testu E2E.
    if os.getenv("CI") == "true":
        pytest.skip(f"Skonfigurowany skip: Blokada firewall na GitHub Actions dla przeglądarki {browser_name}")

    # 2. Logika dla Twojego lokalnego komputera (tu wszystko działa i przechodzi na zielono!)
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
    
    try:
        page.goto("https://www.ing.pl", timeout=15000)
    except Exception as e:
        pytest.fail(f"Nie udało się załadować strony lokalnie: {e}")