# Plan Prezentacji: System Odporności Komunikacji na Zakłócenia

## Slajd 1: Tytuł
**"Odporna Komunikacja Krytyczna: System Anti-Jamming dla Służb Państwowych"**
- Podtytuł: Interconnective, robust and adaptive communication system
- Data, autor, kontekst

## Slajd 2: Dlaczego komunikacja jest krytyczna?
**Współczesne zagrożenia dla komunikacji:**
- Przykłady z Ukrainy - jamming GPS i komunikacji wojskowej
- Incydenty w Polsce - zakłócenia systemów nawigacyjnych
- Statystyki: wzrost ataków na infrastrukturę komunikacyjną o 300% w ostatnich 3 latach
- Konsekwencje: paraliż służb ratunkowych, chaos w transporcie, zagrożenie obronności

## Slajd 3: Kto jest zagrożony? - grupa docelowa
**Kluczowe systemy wymagające ochrony:**
- **Policja** - 383 jednostki organizacyjne
- **Wojsko** - dowodzenie taktyczne i operacyjne - tu komunikacja jest szczególnie istotna, bo najgroźniejsza broń to rzołnierze z radjostacją
- **Energetyka** - 19 elektrowni, 46 elektrociepłowni, 14 operatorów systemowych
- **Kontrola lotów** - 47 lotnisk
- **Kolej** - 20,000 km linii

## Slajd 4: Obecny stan techniczny - fragmentacja (stan zastany)
**Co mamy obecnie:**
- **Systemy analogowe** - nieszyfrowane, publiczne pasma
- **DMR / TETRA** - wdrażanie w wybranych regionach policji (Warszawa, Kraków) - TETRA ma dwa tryby: TMO i DMO, co sprawia, że nawet w przypadkach padnięcia infrastruktury, komunikacja jest możliwa jeden do jednego.
- **Brak interoperacyjności** między służbami
- **Podatność na jamming** - łatwe do zakłócenia
- jak sobie radzi wojsko? - wojskowe systemy komunikacji (np. STANAG 4677) - ale nie są one interoperacyjne z cywilnymi służbami

## Slajd 5: zidentyfikowane Problem do rozwiązania
**Główne wyzwania:**
- **Wykrywanie zakłóceń** w czasie rzeczywistym
- **Automatyczne przełączanie** na systemy zapasowe
- **Interoperacyjność** między służbami w kryzysie
- **DUAL USE** - wykorzystanie istniejącej infrastruktury
- **Decentralizacja** z możliwością centralizacji

## Slajd 6: Stan prawny i regulacyjny
**Podstawy prawne i wymogi zgodności:**
- **Ustawa o zarządzaniu kryzysowym** - wymóg interoperacyjności
- **Dyrektywa NIS2** - ochrona infrastruktury krytycznej
- **Krajowy System Cyberbezpieczeństwa (KSC)** - wymogi dla podmiotów kluczowych
- **Rozporządzenie UKE** - przydzielenie częstotliwości dla służb
- **NATO STANAG 4677** - standardy komunikacji wojskowej
- **Wymagania KSC/NIS2 dla systemów krytycznych**:
  - Security by design - projektowanie z uwzględnieniem odporności
  - Obowiązkowe audyty bezpieczeństwa (co 2 lata)
  - Procedury reagowania na incydenty (zgłoszenie w 24h)
  - Zarządzanie ryzykiem i łańcuchem dostaw
- **Różnicowanie wymogów**: cywilne instytucje (pełne KSC/NIS2) vs. wojsko/policja (częściowe wyłączenia)
**System jako element infrastruktury krytycznej ICT:**
- **Klasyfikacja według KSC/NIS2**:
  - Instytucje cywilne (energetyka, ATC, administracja) - pełne wymogi KSC/NIS2
  - Służby mundurowe/wojsko - częściowe wyłączenia NIS2, ale stosowanie analogicznych standardów
- **Wymagania techniczne dla podmiotów kluczowych**:
  - **Zarządzanie ryzykiem**: systematyczna analiza cyberzagrożeń, środki proporcjonalne do ryzyka
  - **Security by design**: odporność projektowana od początku (spread spectrum, frequency hopping)
  - **Audyt i certyfikacja**: audyty co 2 lata, testy penetracyjne, cyber stress-testy
  - **Zarządzanie łańcuchem dostaw**: weryfikacja dostawców, certyfikaty Common Criteria/ISO 27001
- **Procedury operacyjne**:
  - Wyznaczenie CSIRT liaiona i zespołu reagowania
  - Szkolenia personelu i utrzymanie świadomości bezpieczeństwa
  - Plany ciągłości działania (BCP/DR)
- **Sankcje za niezgodność**: do 10 mln EUR (NIS2) lub 200,000 zł (KSC) + odpowiedzialność za szkody kaskadowe
- ryzyko dług technologiczny - wdrażać najpierw tam gdzie mamy nowy sprzęt

## Slajd 7: Architektura rozwiązania
**Wielopoziomowa struktura i wykorzystanie istniejących zasobów:**
- **Poziom państwowy** - centralna koordynacja (RCB)
- **Poziom wojewódzki** - 16 regionalnych centrów
- **Poziom służbowy** - autonomiczne sieci organizacyjne
- **Zasada**: decentralizacja + centralizacja w kryzysie
- **Integracja istniejących rozwiązań**:
  - Wykorzystanie mobilnych centrów łączności (MCC-1) jako gotowych węzłów komunikacyjnych
  - Włączenie ruchomych kancelarii tajnych jako odpornych na zakłócenia punktów logowania i szyfrowania
  - Integracja z wojskowymi systemami backup'owymi (różne standardy dla wojska vs. policji)
- **Moduły LoRa** na infrastrukturze krytycznej dla wielofunkcyjnego monitoringu

na infra krytycznych były by moduuly lora 

## Slajd 8: System główny - TETRA zgodny z KSC/NIS2
**Trunked Terrestrial Radio jako fundament spełniający wymogi bezpieczeństwa:**
- **Zasięg**: 5-50 km (w zależności od topografii)
- **Szyfrowanie**: AES-256, klucze rotowane co 24h (zgodność z wymogami KSC)
- **Przepustowość**: 12.5 kHz kanały, 2 sloty czasowe
- **Koszty**: 2,000-5,000 zł za radiotelefon, 50,000-200,000 zł za stację bazową
- **Czas wdrożenia**: 18-24 miesiące dla województwa
- **Wbudowane zabezpieczenia NIS2**:
  - Redundancja kanałów komunikacyjnych
  - Systemy wykrywania włamań (IDS/IPS)
  - Segmentacja sieci na strefy bezpieczeństwa
  - Monitoring i logowanie wszystkich aktywności
  - Procedury backup'u i disaster recovery

## Slajd 9: Backup #1 - Komunikacja satelitarna
**Niezależny od infrastruktury naziemnej:**
- **Technologia**: LEO (Starlink Gov), MEO (SES), GEO (Eutelsat)
- **Zasięg**: globalny, opóźnienia 20-600ms
- **Koszty**: 500-2,000 USD/miesiąc za terminal
- **Przepustowość**: 100 Mbps-1 Gbps
- **Odporność**: trudna do zakłócenia, wymaga zaawansowanego jammingu

## Slajd 10: Backup #2 - LoRa Mesh
**Lokalna, rozproszona komunikacja i wielofunkcyjny monitoring:**
- **Zasięg**: 2-15 km w terenie otwartym
- **Przepustowość**: 0.3-50 kbps (dane, teksty, telemetria)
- **Koszty**: 50-200 zł za moduł
- **Topologia**: mesh - każdy węzeł retransmituje
- **Funkcje pokojowe**:
  - Zbieranie danych telemetrycznych, meteorologicznych, środowiskowych
  - Monitoring jakości powietrza, poziomu wód, sejsmiki
  - Wsparcie dla IoT w infrastrukturze krytycznej
- **Funkcje bezpieczeństwa**:
  - Detekcja i triangulacja źródeł jammingu poprzez analizę RSSI z wielu punktów
  - Obsługa dodatkowych częstotliwości (433MHz, 868MHz, 915MHz) dla redundancji
  - Automatyczne raportowanie anomalii spektralnych
  - LoRa można wykożystać też później w systemach wczesnego ostrzegania np w sytuacji wojny, nalotów itp.   

## Slajd 11: System detekcji AI/ML - zgodny z wymogami cyberbezpieczeństwa
**Inteligentne wykrywanie z pełną dokumentacją incydentów:**
- **Monitoring ciągły (pokój + kryzys)**: RSSI, BER, czas odpowiedzi, spektrum RF
- **Algorytmy ML z audytem**: 
  - Transparentne modele uczenia maszynowego
  - Regularne testy penetracyjne i stress-testy
  - Dokumentacja wszystkich decyzji automatycznych
- **Zarządzanie incydentami zgodnie z KSC/NIS2**:
  - Automatyczne wykrywanie i klasyfikacja incydentów
  - Zgłoszenie poważnych incydentów do CSIRT w 24h
  - Pełna dokumentacja i procedury eskalacji
  - Powiadomienia użytkowników o środkach zaradczych
- **TRYB POKOJOWY**: podstawowe wymogi KSC dla podmiotów publicznych
- **TRYB KRYZYSOWY**: wzmocnione standardy NATO dla operacji wojskowych
- **Reakcja kryzysowa**: automatyczne przełączanie z zachowaniem compliance

## Slajd 12: Iteracyjne wdrożenie - strategia redukcji ryzyka
**Stopniowe budowanie odporności z ciągłymi korzyściami:**

**POZIOM 1 (6-12 miesięcy): Podstawa monitoringu**
- Wdrożenie sieci LoRa Mesh w województwie podkarpackim
- Instalacja systemu AI/ML do detekcji jammerów
- Integracja z istniejącymi MCC-1 w regionie
- *Korzyść*: Wykrywanie zakłóceń, zbieranie telemetrii, pierwsza warstwa ochrony

**POZIOM 2 (12-18 miesięcy): Wzmocnienie komunikacji**
- Rozbudowa sieci TETRA dla służb w pilotażowym województwie
- Włączenie ruchomych kancelarii tajnych do sieci logowania
- Satelitarny backup dla kluczowych obiektów energetycznych
- *Korzyść*: Odporna komunikacja służb, bezpieczne logowanie operacji

**POZIOM 3 (18-30 miesięcy): Skalowanie regionalne**
- Rozszerzenie na 3-5 województw
- Pełna integracja z systemami wojskowymi (różne standardy backup)
- Zaawansowane funkcje triangulacji i neutralizacji jammingu
- *Korzyść*: Ochrona regionalna, interoperacyjność wojsko-cywil

**POZIOM 4 (30-48 miesięcy): Pokrycie krajowe**
- Ogólnopolska sieć zintegrowanych systemów
- Automatyczne przełączanie między poziomami backup
- Pełna funkcjonalność AI w wykrywaniu i przeciwdziałaniu zagrożeniom
- *Korzyść*: Krajowa odporność, autonomiczne reagowanie na zagrożenia

## Slajd 13: Integracja z systemami wojskowymi - compliance międzysektorowe
**Wykorzystanie sprawdzonych rozwiązań z zachowaniem zgodności prawnej:**
- **Mobilne Centra Łączności (MCC-1)**:
  - Certyfikowane systemy szyfrowania zgodne z NATO STANAG
  - Dokumentowane procedury bezpieczeństwa i audytu
  - Integracja respektująca różne wymogi compliance (wojskowe vs. cywilne)
- **Ruchome Kancelarie Tajne**:
  - Logowanie zgodne z wymogami KSC (pełna dokumentacja incydentów)
  - Szyfrowanie kwantowe (QKD) dla najwyższego poziomu bezpieczeństwa
  - Procedury eskalacji do odpowiednich CSIRT-ów
- **Różnicowanie standardów z uwzględnieniem prawa**:
  - **WOJSKO**: NATO standards + krajowe wymogi bezpieczeństwa narodowego
  - **POLICJA/PSP**: KSC + procedury cywilne + interoperacyjność z 112
  - **ENERGETYKA**: pełne NIS2 + standardy SCADA + protokoły IEC
- **Automatyczne zarządzanie compliance**:
  - Systemy automatycznego raportowania incydentów
  - Różne poziomy dostępu w zależności od klasyfikacji bezpieczeństwa
  - Dokumentacja wszystkich przełączeń trybu pracy dla audytu

## Slajd 14: Koszty, finansowanie
**Realny budżet z uwzględnieniem wymogów prawnych:**
- **POZIOM 1 (Monitoring + podstawowe compliance)**: 65 mln zł
  - LoRa Mesh (20 mln) + AI/ML (20 mln) + MCC-1 (10 mln) + **systemy compliance** (15 mln)
- **POZIOM 2 (Komunikacja + pełne KSC)**: +120 mln zł
  - TETRA (60 mln) + satelity (30 mln) + kancelarie (10 mln) + **audyty i certyfikacje** (20 mln)
- **POZIOM 3 (Skalowanie + NIS2)**: +230 mln zł
  - Regiony + wojsko + **pełne systemy zarządzania incydentami** (30 mln dodatkowe)
- **POZIOM 4 (Krajowe + ciągłe compliance)**: +170 mln zł
  - Finalizacja + **ongoing audyty, szkolenia, aktualizacje** (20 mln/rok)
- **RAZEM**: 585 mln zł (0,12% budżetu państwa)
- **Koszty operacyjne compliance**: 15-20 mln zł/rok (audyty, certyfikacje, szkolenia, CSIRT)
- **Potencjalne kary za niezgodność**: do 10 mln EUR - **ROI compliance widoczny natychmiast**

## Slajd 15: Następne kroki / podsumowanie
**Plan działania - iteracyjne budowanie odporności:**
- **Q2 2025**: Finalizacja koncepcji, wybór lokalizacji pilotażowej
- **Q3 2025**: Start Poziomu 1 - wdrożenie LoRa Mesh + AI/ML w woj. podkarpackim
- **Q4 2025**: Integracja z MCC-1, pierwsze testy triangulacji jammerów
- **Q1-Q2 2026**: Ewaluacja Poziomu 1, start Poziomu 2 (TETRA + satelity)
- **Q3-Q4 2026**: Włączenie ruchomych kancelarii tajnych, testy z wojskiem
- **2027-2028**: Poziomy 3-4, skalowanie krajowe
- **Kluczowe**: Każdy poziom przynosi korzyści, system samofinansuje kolejne etapy
