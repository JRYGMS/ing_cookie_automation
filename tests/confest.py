import pytest
from playwright.sync_api import Page

@pytest.fixture(autouse=True)
def bypass_and_check_firewall(page: Page, browser_name: str):
    # 1. Maskowanie automatyzacji przed wejściem na stronę
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
    
    # 2. Pełne wejście na stronę (czekamy na załadowanie, żeby Imperva wystawiła ciasteczka)
    try:
        page.goto("https://www.ing.pl", timeout=20000)
    except Exception as e:
        # Jeśli strona w chmurze w ogóle nie odpowiedziała w 20s, bezpiecznie skipujemy
        pytest.skip(f"Timeout ładowania strony na {browser_name}: {e}")

    # 3. Pobranie nazw ciasteczek sesyjnych
    cookies = page.context.cookies()
    cookie_names = [c['name'] for c in cookies]

    # 4. Sprawdzenie obecności baneru oraz ciasteczek blokady
    try:
        page.get_by_role('button', name='Dostosuj').wait_for(state="visible", timeout=5000)
    except Exception:
        # Jeśli po 5 sekundach nie ma przycisku, a mamy ciasteczka incap_ses -> skipujemy w chmurze
        if any("incap_ses" in name for name in cookie_names):
            pytest.skip(f"[CI/CD BLOKADA] Imperva Incapsula zablokowała stronę na {browser_name}.")   
        else:
            # Jeśli przycisku nie ma i nie ma ciasteczek blokady -> to prawdziwy błąd aplikacji lokalnie
            raise AssertionError(f"Nie znaleziono baneru cookies na {browser_name}, mimo braku blokady firewall.")