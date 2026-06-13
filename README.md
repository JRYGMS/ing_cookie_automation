# ING Cookie Policy Automation

Projekt automatyzacji testów weryfikujący poprawność działania polityki prywatności oraz ciasteczek GDPR/PDGR na portalu **ING.pl**. 

Skrypt testuje aplikację w sposób asynchroniczny i wieloprzeglądarkowy, badając bezpośredni wpływ interakcji z UI na stan pamięci podręcznej (cookies) przeglądarki.

---

## Kluczowe cechy projektu

* **Multi-browser Support:** Testy uruchamiają się równolegle na trzech silnikach: **Chromium**, **Firefox** oraz **WebKit** (Safari).
* **Deep Cookie Inspection:** Test nie ogranicza się do klikania – pobiera stan ciasteczek przed i po akcji, a następnie za pomocą operacji na zbiorach (`set()`) weryfikuje obecność konkretnych tokenów (np. `cookiePolicyGDPR`).
* **Zrównoleglenie (Parallel Execution):** Wykorzystanie wtyczki `pytest-xdist` pozwala na maksymalne skrócenie czasu wykonania (lokalny test na 16 wątkach trwa nieco ponad **5 sekund**).
* **Odporność CI/CD (Cybersec Aware):** Skrypt posiada wbudowaną logikę detekcji systemów ochrony Enterprise (Imperva Incapsula), co gwarantuje stabilność potoku w chmurze.

---
