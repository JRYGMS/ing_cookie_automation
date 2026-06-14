# ING Cookie Policy Automation

Projekt automatyzacji testów weryfikujący poprawność działania polityki prywatności oraz ciasteczek GDPR/PDGR na portalu **ING.pl**. 

Skrypt testuje aplikację w sposób synchroniczny i wieloprzeglądarkowy, badając bezpośredni wpływ interakcji z UI na stan pamięci podręcznej (cookies) przeglądarki.

---

## Kluczowe cechy projektu

* **Multi-browser Support:** Testy uruchamiają się równolegle na trzech silnikach: **Chromium**, **Firefox** oraz **WebKit** (Safari).
* **Deep Cookie Inspection:** Test nie ogranicza się do klikania – pobiera stan ciasteczek przed i po akcji, a następnie za pomocą operacji na zbiorach (`set()`) weryfikuje obecność konkretnych tokenów (np. `cookiePolicyGDPR`).
* **Zrównoleglenie (Parallel Execution):** Wykorzystanie wtyczki `pytest-xdist` pozwala na maksymalne skrócenie czasu wykonania (lokalny test na 16 wątkach trwa nieco ponad **5 sekund**).
* **Odporność CI/CD (Cybersec Aware):** Skrypt posiada wbudowaną logikę detekcji systemów ochrony Enterprise (Imperva Incapsula), co gwarantuje stabilność potoku w chmurze.

---
# Stos technologiczny
* **Język:** Python 3.14 (lokalnie), 3.11 (GitHub)
* **Framework:** Pytest
* **Automatyzacja UI:** Playwright (Python Sync API)
* **CI/CD:** GitHub Actions (Runner: Ubuntu 22.04)

  ---

  # Instrukcja instalacji i uruchomienia (lokalnie)

  1. **Sklonuj repozytorium:**
     ```bash
     git clone https://github.com/JRYGMS/ing_cookie_automation.git
     cd ing_cookie_automation
     ```
     
  2. **Stwórz i aktywuj środowisko wirtualne:**
     **Tworzenie środowiska:**
     ```bash
     #Windows
     python -m venv .venv
     #macOS / Linux
     python3 -m venv .venv
     ```
     **Aktywacja Środowiska:**
     ```bash
     #Windows (PowerShell)
     .\.venv\Scripts\activate.ps1
     #macOS / Linux
     source .venv\bin\activate
     ```
     
  3. **Zainstaluj wymagane biblioteki(Pytest, Playwright oraz pluginy)**
     Ze względu na to, że wymagane biblioteki znajdują się w pliku `requirements.txt`, wystarczy wpisać:
     ```bash
     #Windows
     pip install -r requirements.txt

     #macOS / Linux
     pip3 install -r requirements.txt
     ```

  4. **Zainstaluj binarne silniki przeglądarek dla Playwright:**
     ```bash
     #Windows
     python -m playwright install --with-deps

     #macOS / Linux
     python3 -m playwright install --with-deps
     ```
  *Ta komenda automatycznie pobierze Chromium, Firefox, Webkita oraz niezbędne dla nich zależności systemowe.*

  5. **Uruchom testy automatyczne:**
     ```bash
     pytest
     ```

     Konfiguracja pliku  `pytest.ini` automatycznie wykryje testy w folderze `tests/`, dobierze liczbę wątków dla procesora `pytest-xdist` oraz przetestuje 3 przeglądarki równolegle.

---

## Architektura CI/CD & Raport GitHub Actions

W projekcie skonfigurowano w pełni automatyczny pipeline w chmurze **GitHub Actions** (`.github/workflows/playwright.yml`), który uruchamia się przy każdym commicie.

Podczas uruchamiania w publicznej chmurze GitHub Actions, testy celowo zwracają status `3 skipped`. Jest to zdarzenie świadome uwarunkowane określonymi okolicznościami:

  1. **Wyzwalacz:**
     Publiczne adresy IP maszyn wirtualnych GitHub Actions są automatycznie flagowane i blokowane przez zaporę sieciową     Imperva Incapsula, która chroni infrastrukturę banku ING. Zamiast właściwej strony, najprawdopodobniej wyświetlany jest ekran wyzwania (Challenge Page) 
  2. **Detekcja i Reakcja:** Framework za pomocą funkcji `check_and_skip_if_blocked` sprawdza obecność przycisku "Dostosuj". W przypadku wyświetlenia wyjątku PlaywrightTimeoutError bada pamięć podręczną pod kątem obecności ciasteczek `incap_ses`.
  3. **Efekt (status SKIPPED):** Przy wykryciu blokady, test wywołuje funkcję `pytest.skip()`. Zapobiega to oznaczeniu testu na GitHub jako uszkodzonego z przyczyn niezależnych od jakości kodu (False Positives), jednocześnie logując napotkaną barierę bezpieczeństwa banku   
