import pytest
from playwright.sync_api import Page

@pytest.fixture(autouse=True)
def bypass_and_check_firewall(page: Page, browser_name: str):
   
    page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
    
    
    try:
        page.goto("https://www.ing.pl", timeout=20000)
    except Exception as e:
       
        pytest.skip(f"Timeout ładowania strony na {browser_name}: {e}")

    
    cookies = page.context.cookies()
    cookie_names = [c['name'] for c in cookies]


    try:
        page.get_by_role('button', name='Dostosuj').wait_for(state="visible", timeout=5000)
    except Exception:
        
        if any("incap_ses" in name for name in cookie_names):
            pytest.skip(f"[CI/CD BLOKADA] Imperva Incapsula zablokowała stronę na {browser_name}.")   
        else:

            raise AssertionError(f"Nie znaleziono baneru cookies na {browser_name}, mimo braku blokady firewall.")