## DATA INTEGRATION PROJECT

## **Topic:**
Compiling data on past and ongoing armed conflicts with commodity prices.

## **Project Goal:**
The goal of the project is to present two heterogeneous datasets—concerning armed conflicts and commodity prices—and to find relationships in seemingly unrelated data. The project analyzes how commodity prices may be linked to the intensity of armed conflicts based on historical data
	
# Project Description
The project is based on two datasets:
- Armed conflicts: https://www.prio.org/data/4
  
	Contains information about past and ongoing conflicts, their locations, durations, intensities, and involved parties.

- Commodity prices: https://www.worldbank.org/en/research/commodity-markets
  
 	Selected dataset with prices of individual commodities for each year in the range 1960–2025.
  
## **Funkcjonalności**
Projekt integruje dane o konfliktach zbrojnych i cenach surowców, oferując rozbudowane narzędzia analityczne i wizualizacyjne. Poniżej przedstawiono kluczowe funkcjonalności systemu:

- **1. Panel główny (dashboard)**
	- Prezentuje podsumowanie liczby lat z danymi o surowcach i konfliktach, najnowsze dostępne lata oraz zakres danych historycznych.
	- Agreguje statystyki z obu zbiorów danych i umożliwia szybki przegląd stanu bazy
		
- **2. Dashboard surowców**
	- Lista dostępnych surowców (np. ropa, gaz, metale, produkty rolne) oraz wizualizacja ich cen w czasie.
	- Dynamiczne pobieranie danych dla wybranego surowca do wykresów i analiz
		
- **3. Dashboard konfliktów**
	- Statystyki konfliktów zbrojnych według roku, typu i poziomu intensywności.
	- Graficzna reprezentacja danych 
		
- **4. REST API dla dashboardów**
	- API do pobierania danych o surowcach i konfliktach, wykorzystywane przez frontend do dynamicznych wizualizacji
	
- **5. Tabele i zestawienia**
	- Przeglądanie tabel z danymi o surowcach, konfliktach lub ich połączonych zestawieniach (join), np. po roku.
	- Możliwość wyboru wyświetlanych kolumn
	- wyszukiwanie po nazwie
		
- **6. Eksport danych**
	- Możliwość wyboru zakresu danych do eksportu.
	- Eksport zarówno do formatu JSON, jak i XML – użytkownik decyduje o formacie wyjściowym.
	- Eksport obejmuje zarówno surowe dane z tabel, jak i dane połączone (np. join po roku).
	
- **6. Korelacje i wizualizacje**
	- dynamiczne generowanie wykresów cen surowców na tle liczby konfliktów na przestrzeni lat
	- Automatyczne generowanie heatmapy korelacji między liczbą i intensywnością konfliktów a cenami wybranych surowców.
		
- **7. Obsługa użytkowników**
	- Rejestracja, logowanie i wylogowywanie użytkowników.
	- Dostęp do kluczowych funkcji wymaga autoryzacji (widoki zabezpieczone loginem)
	- Panel admina dostępny pod adresem http://127.0.0.1:8000/admin/
		
- **8. Transakcje z kontrolą poziomu izolacji**
	- Mechanizmy transakcyjne z możliwością ustawiania poziomu izolacji, trybu tylko do odczytu oraz limitu czasu na wykonanie zapytań.
	
	
### **Technologie**
- **Backend:** Django (Python)
- **Frontend:** JavaScript (szablony Django)
- **Baza danych:** PostgreSQL
- **API:** Django REST Framework (REST API)
- **Uwierzytelnianie:** Django Auth (system użytkowników i sesji), Django Admin Panel (zarządzanie danymi przez administratorów)
- **ORM:** Django ORM
- **Zarządzanie zależnościami:** pip, requirements.txt
	
### **Uruchomienie projektu**
**1. Rozpakuj pobrany folder zip** 
*( lub sklonuj projekt z github https://github.com/jagfoljersolen/Integration_Project )*
	
	git clone https://github.com/jagfoljersolen/Integration_Project.git
	cd Integration_Project
		
**2. Utwórz i aktywuj wirtualne środowisko**
		
	python -m venv venv
	source venv/bin/activate 	# Linux/macOS
	venv\Scripts\activate 		# Windows
		
**3. Zainstaluj zależności**
		
	pip install -r requirements.txt
		
**4. Skonfiguruj bazę danych:**	

    *Zaloguj się do PostgreSQL (np. poleceniem w terminalu):*

    	psql -U postgres

    *Utwórz bazę danych:*

    	CREATE DATABASE integration_db;

    *Utwórz użytkownika z hasłem:*

    	CREATE USER db_user WITH PASSWORD 'integration';

    *Przyznaj uprawnienia użytkownikowi do bazy:*

    	GRANT ALL PRIVILEGES ON DATABASE integration_db TO db_user;

    *Wyjdź z psql:*

    	\q

    *Upewnij się, że w pliku settings.py masz następującą konfigurację:*

		DATABASES = {
		'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'integration_db',
		'USER': 'db_user',
		'PASSWORD': 'integration',
		'HOST': 'localhost',
		'PORT': '5432',
		}
		}

   		
**5. Wykonaj migracje:**
   		
   	python manage.py migrate
   		
**6. Zainicjalizuj bazę danych**
   	
   	python manage.py import_commodity_with_units data/commodity_with_units.csv
	python manage.py import_conflicts data/conflicts.csv --batch-size 1000
		
**7. (Opcjonalnie) Utwórz konto administratora**
		
	python manage.py createsuperuser
		
**8. Uruchom serwer**
		
	python manage.py runserver
		
**9. Uruchom aplikację w przeglądarce**
	
	http://127.0.0.1:8000/
		
	
   		
		
	

	
	
		
		
