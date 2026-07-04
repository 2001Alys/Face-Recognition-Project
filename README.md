# Opis projektu

Celem projektu było stworzenie aplikacji wspierającej proces weryfikacji obecności użytkowników poprzez system logowania oparty na technologii rozpoznawania twarzy. Narzędzie zostało zaprojektowane z myślą o zapewnieniu intuicyjności i prostoty obsługi, dzięki czemu może być wykorzystywane w różnych środowiskach, takich jak:

- firmy,
- instytucje edukacyjne,
- organizacje publiczne i prywatne.

Aplikacja posiada przejrzysty oraz przyjazny interfejs graficzny umożliwiający zarówno logowanie, jak i rejestrację użytkowników. W trakcie rejestracji użytkownicy posiadający odpowiednie uprawnienia mogą przypisywać role i poziomy dostępu, dostosowując funkcjonalność systemu do struktury organizacyjnej.

## Metody uwierzytelniania

System umożliwia autoryzację na dwa sposoby:

- logowanie przy użyciu hasła,
- logowanie przy użyciu rozpoznawania twarzy.

W przypadku logowania biometrycznego kamera urządzenia przechwytuje obraz użytkownika w czasie rzeczywistym. Następnie aplikacja:

1. Wykrywa twarz.
2. Przeprowadza wstępną obróbkę obrazu.
3. Enkoduje cechy twarzy.
4. Porównuje je z zapisanymi danymi użytkownika.

Zastosowane algorytmy pozwalają określić, czy dana twarz należy do właściwego użytkownika, zapewniając wysoki poziom bezpieczeństwa.

Dodatkowo aplikacja generuje komunikaty dialogowe informujące użytkownika o przebiegu procesu logowania, rejestracji oraz ewentualnych błędach.

## Raportowanie

System umożliwia generowanie raportów w formacie HTML zawierających informacje dotyczące:

- czasu pracy pracowników,
- obecności,
- historii wejść i wyjść.

Pozwala to na skuteczne monitorowanie aktywności użytkowników oraz efektywne zarządzanie zasobami organizacji.

---

# Instrukcja użytkowania

## Struktura projektu

Program podzielony jest na sześć plików:

```text
gui.py
html_handling.py
gui_camera.py
apka.py
dane_logowania.json
obecnosc.json
```

### gui.py

Plik odpowiedzialny za uruchomienie interfejsu graficznego oraz obsługę:

- logowania,
- autentykacji,
- rejestracji,
- panelu opcji,
- wyszukiwania użytkowników w plikach JSON,
- pobierania zapisanych enkodowań twarzy.

### html_handling.py

Plik zawiera funkcje odpowiedzialne za generowanie raportów HTML prezentujących statystyki obecności pracowników.

### gui_camera.py

Plik odpowiada za:

- obsługę kamery,
- pomiar czasu pracy,
- zapis informacji o obecności do plików JSON.

### apka.py

Plik zawiera funkcje odpowiedzialne za:

- wykrywanie twarzy,
- przygotowanie obrazu do analizy,
- enkodowanie twarzy,
- porównywanie twarzy.

---

## Logowanie do systemu

Po uruchomieniu pliku `gui.py` wyświetlane jest okno logowania.

Okno zawiera:

- pole **Imię i Nazwisko**,
- listę rozwijaną z działami,
- przycisk **Zweryfikuj**.

Po kliknięciu przycisku następuje sprawdzenie danych użytkownika w pliku JSON.

### Możliwe scenariusze

#### Użytkownik nie istnieje

Jeżeli użytkownik nie zostanie odnaleziony:

- wyświetlany jest komunikat o błędzie,
- formularz zostaje wyczyszczony.

#### Użytkownik istnieje

Po poprawnym zweryfikowaniu danych wyświetlane jest okno autentykacji, zawierające:

- pole wpisania hasła,
- przycisk weryfikacji hasła,
- opcję logowania twarzą,
- przycisk powrotu.

W przypadku niepoprawnego hasła:

- wyświetlany jest komunikat błędu,
- pole hasła zostaje wyczyszczone.

---

## Logowanie za pomocą twarzy

Po wybraniu autoryzacji biometrycznej uruchamiane jest okno kamery.

Dostępne są dwa przyciski:

- **Cofnij** – powrót do ekranu logowania,
- **Zrób zdjęcie** – wykonanie fotografii użytkownika.

### Brak wykrytej twarzy

Jeżeli na zdjęciu nie zostanie wykryta twarz:

- system wyświetla komunikat,
- okno kamery pozostaje aktywne,
- użytkownik może wykonać kolejną próbę.

### Brak dostępnej kamery

Jeżeli aplikacja nie wykryje żadnego urządzenia:

- wyświetlany jest komunikat,
- użytkownik zostaje cofnięty do ekranu autoryzacji.

### Poprawna identyfikacja

W przypadku wykrycia i poprawnej identyfikacji twarzy:

- wyświetlany jest komunikat sukcesu,
- użytkownik zostaje przekierowany do panelu opcji.

Na środku okna kamery znajduje się eliptyczne obramowanie wyznaczające obszar, w którym powinna znajdować się twarz.

---

## Panel opcji

Po poprawnym uwierzytelnieniu wyświetlany jest panel opcji.

Dostępne funkcje zależą od przypisanej roli użytkownika.

### Role systemowe

- Prezes
- Pracownik
- Technik

Największy zakres uprawnień posiada rola **Technik**.

---

## Funkcje technika

Panel technika umożliwia:

### Rejestrację wejścia

Opcja zapisuje godzinę rozpoczęcia pracy do pliku .json.

### Rejestrację wyjścia

Opcja zapisuje godzinę zakończenia pracy do pliku .json.

### Statystyki osobiste

Wyświetlane są informacje o czasie pracy użytkownika:

- w bieżącym dniu,
- w bieżącym tygodniu,
- w bieżącym miesiącu.

### Wylogowanie

Przycisk powoduje powrót do okna logowania.

---

## Statystyki wszystkich pracowników

Opcja **Statystyki Wszystkich** generuje raport HTML prezentujący:

### Zbiorcze statystyki

- listę wszystkich pracowników,
- liczbę przepracowanych godzin,
- statystyki dzienne,
- statystyki tygodniowe,
- statystyki miesięczne.

### Szczegółową historię obecności

Raport zawiera również:

- przyjścia pracowników,
- wyjścia pracowników,
- podział na działy,
- sortowanie danych.

---

## Rejestracja użytkownika

Opcja **Zarejestruj** umożliwia dodanie nowego użytkownika do systemu.

Po jej wybraniu otwierane jest okno rejestracji.

Formularz wymaga podania wszystkich niezbędnych danych i zabezpieczony jest przed pozostawieniem pustych pól.

Po poprawnym uzupełnieniu formularza uruchamiane jest okno kamery wykorzystywane do zapisania wzorca twarzy użytkownika.

Proces korzysta z tych samych zabezpieczeń:

- brak twarzy,
- brak kamery,
- poprawne wykrycie twarzy.

Po pomyślnym zakończeniu rejestracji wyświetlany jest komunikat, a dane użytkownika trafiają do plików .json.

### Wynik rejestracji

- Niepowodzenie → powrót do formularza rejestracji.
- Sukces → przekierowanie do ekranu logowania.

---

# Proces rozpoznawania twarzy

## Etap 1 – Przygotowanie obrazu

Obraz jest przygotowywany poprzez:

1. Zmniejszenie rozdzielczości do maksymalnie 1000×1000 pikseli.
2. Analizę obrazu przez bibliotekę OpenCV.
3. Wykrycie twarzy przy użyciu modelu - haarcascade_frontalface_default.

Jeżeli twarz nie zostanie wykryta, aplikacja zwraca odpowiedni komunikat.

Jeżeli wykrytych zostanie kilka twarzy:

- analizowana jest odległość od środka zdjęcia,
- wybierana jest twarz położona najbliżej środka kadru.

Następnie wykryta twarz zostaje wykadrowana i zapisana na dysku.

Średni czas przygotowania obrazu wynosi - do 100 ms.

---

## Etap 2 – Enkodowanie twarzy

Przygotowany obraz poddawany jest analizie przy użyciu biblioteki - Face Recognition.

Biblioteka wykorzystuje wytrenowaną sieć neuronową do analizy charakterystycznych punktów twarzy.

W procesie enkodowania:

- twarz przekształcana jest do wektora cech,
- generowany jest 128-elementowy wektor opisujący cechy biometryczne użytkownika.

---

## Etap 3 – Porównanie twarzy

Program porównuje:

- zapisany wzorzec twarzy,
- aktualnie przechwycony obraz.

Analizowane są odległości pomiędzy cechami twarzy.

Wynik porównania zwracany jest jako wartość logiczna:
True  – twarze należą do tej samej osoby
False – twarze należą do różnych osób

Najbardziej czasochłonną częścią procesu jest enkodowanie twarzy, którego średni czas wykonania wynosi około 1 sekunda.
