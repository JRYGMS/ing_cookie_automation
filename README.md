# ING Cookie Policy Automation Projekt automatyzacji testów E2E realizujący zadanie rekrutacyjne polegające na weryfikacji działania mechanizmu zgód cookies na stronie **https://www.ing.pl**. 
## Zakres testu 
Scenariusz testowy 
1. Wejście na stronę ing.pl
2. Otworzenie menu konfiguracji cookies("Dostosuj")
3. Wyrażenie zgody na cookies analityczne
4. Kliknięcie "Zaakceptuj zaznaczone"
5. Weryfikacja zapisania odpowiednich cookies w przeglądarce

--- 

## Cel projektu 
Celem projektu jest automatyzacja weryfikacji działania bannera cookies na stronie ING.pl w ramach zadania rekrutacyjnego. 
Projekt skupia się na: 
* symulacji realnej interakcji użytkownika z UI,
* weryfikacji zmian w stanie cookies,
* uruchamianiu testów w różnych przeglądarkach,
*  integracji z pipeline CI/CD.

--- 

## Wymagania niefunkcjonalne
Powtarzalność testów 
Test został zaprojektowany tak, aby był możliwie deterministyczny w ramach ograniczeń zewnętrznej aplikacji (ING.pl), między innymi poprzez:
* pracę na stanie cookies przed i po akcji,
* unikanie zależności od czasu UI,
* jawne oczekiwanie na elementy DOM.

--- 

## Stos technologiczny 
* **Język:** Python 3.11
* **Framework:** Pytest
* **Automatyzacja UI:** Playwright (Python Sync API)
* **CI/CD:** GitHub Actions (Runner: Ubuntu 22.04)

--- 

## Instrukcja instalacji i uruchomienia (lokalnie) 1. 
**Sklonuj repozytorium:**
```bash
     git clone https://github.com/JRYGMS/ing_cookie_automation.git
     cd ing_cookie_automation
```

**Stwórz i aktywuj środowisko wirtualne:** **Tworzenie środowiska:**

```bash
     #Windows
     python -m venv .venv
     #macOS / Linux
     python3 -m venv .venv
```
**Aktywacja Środowiska:**
```bash
     #Windows (PowerShell)
     .venv\Scripts\activate
     #macOS / Linux
     source .venv\bin\activate
```
**Zainstaluj wymagane biblioteki(Pytest, Playwright oraz pluginy)** 

Biblioteki znajdują się w pliku requirements.txt, dlatego:

```bash
     #Windows
     pip install -r requirements.txt

     #macOS / Linux
     pip3 install -r requirements.txt
```
**Zainstaluj binarne silniki przeglądarek dla Playwright:**
```bash
     #Windows
     python -m playwright install --with-deps

     #macOS / Linux
     python3 -m playwright install --with-deps
```
*Ta komenda automatycznie pobierze Chromium, Firefox, WebKit oraz niezbędne dla nich zależności systemowe.*
**Uruchom testy automatyczne:**
```bash
     pytest
```

--- 
## Testy wieloprzeglądarkowe 
Testy uruchamiane są równolegle w trzech przeglądarkach: 
* Chromium
* Firefox
* WebKit
Wykorzystano mechanizm Playwright fixtures oraz `pytest-xdist` do równoległego wykonania testów

--- 

## Architektura CI/CD & Raport GitHub Actions 
Projekt zawiera pipeline automatyzujący uruchamianie testów w środowisku GitHub Actions. 
Plik workflow: 
`.github/workflows/playwright.yml`

Pipeline: 
* instaluje zależności,
* instaluje przeglądarki Playwright,
* uruchamia testy(pytest + pytest-xdist),
* wykonuje je równolegle.

--- 

## Zachowanie w CI (ważne) W środowisku GitHub Actions testy mogą być oznaczone jako SKIPPED. 
Powód: 
* publiczne adresy IP runnerów mogą być blokowane przez systemy ochrony (np. Imperva/WAF),
* w takim przypadku aplikacja nie zwraca standardowego widoku banera cookies. Testy wykrywają tę sytuację i świadomie wykonują pytest.skip(), aby uniknąć fałszywie negatywnych wyników.

--- 

## Założenia projektu 
* Test dotyczy zewnętrznej aplikacji (ING.pl), nad którą brak kontroli.
* Selektory UI mogą ulegać zmianie wraz z aktualizacją strony.
* Kluczowym elementem testu jest weryfikacja zmian w cookies, a nie implementacja UI.

---

## Struktura projektu
```bash
tests/
  test_ing_cookies.py

conftest.py
requirements.txt
pytest.ini

.github/
  workflows/
    playwright.yml
```

---

## Podsumowanie Projekt realizuje wymagania zadania rekrutacyjnego poprzez:

* automatyzację scenariusza testowego w Playwright,
* weryfikację zmian w cookies po interakcji użytkownika,
* obsługę wielu przeglądarek, * równoległe wykonanie testów,
* integracja z GitHub Actions.

---

## Test z wykorzystaniem Playwright oraz VPN
Po wykonaniu testu za pomocą komendy `playwright codegen https://www.ing.pl` przy użyciu darmowego narzędzia VPN, w widoku strony wyświetla się informacja o podejrzeniu przebywania za granicą oraz prośba o wykonanie testu `CAPCHA`. Z tego względu, test nie może zostać zrealizowany, ponieważ obiekty przewidziane w teście nie zostaną wyświetlone w cyklu testowym. Z tego względu, rezultatem testu jest odpowiedź `SKIPPED`.
