# Proces instalacji

## Wymagania wstępne

Przed rozpoczęciem instalacji należy przygotować środowisko pracy.

### 1. Instalacja Python

Zainstaluj najnowszą stabilną wersję języka **Python**, dostępną na oficjalnej stronie.

### 2. Instalacja Microsoft Visual Studio 2022

Zainstaluj **Microsoft Visual Studio 2022**.

Podczas instalacji wybierz komponent:

- **Desktop development with C++**

---

## Instalacja wymaganych pakietów

### 1. Uruchomienie wiersza poleceń

1. Otwórz **Menu Start**.
2. Wpisz `cmd`.
3. Uruchom **Wiersz poleceń**.

### 2. Instalacja narzędzi kompilacyjnych

Wprowadź kolejno poniższe polecenia:

```bash
pip install cmake
pip install dlib
```

### 3. Instalacja bibliotek aplikacji

Następnie zainstaluj wymagane biblioteki:

```bash
pip install PySimpleGUI
pip install opencv-python
pip install face_recognition
pip install numpy
```

---

## Wykorzystane biblioteki i moduły

| Biblioteka / Moduł | Zastosowanie w projekcie |
|-------------------|--------------------------|
| **PySimpleGUI** | Tworzenie interfejsu graficznego (GUI) oraz komunikacja aplikacji z użytkownikiem. |
| **OpenCV (cv2)** | Obsługa kamery, przechwytywanie obrazu, przetwarzanie obrazu oraz wykrywanie twarzy. |
| **face_recognition** | Enkodowanie twarzy użytkownika oraz porównywanie twarzy podczas procesu uwierzytelniania. |
| **dlib** | Biblioteka wykorzystywana przez `face_recognition` do generowania wektorów cech twarzy i przeprowadzania analiz biometrycznych. |
| **NumPy** | Operacje na tablicach danych oraz obsługa enkodowanych danych twarzy wykorzystywanych przez mechanizm rozpoznawania. |
| **json** | Zapis i odczyt danych aplikacji, w tym informacji o logowaniach oraz rejestrach obecności. |
| **os** | Zarządzanie plikami i katalogami, w tym usuwanie tymczasowo zapisanych obrazów twarzy w celach bezpieczeństwa. |
| **time** | Pomiar czasu wykonywania operacji oraz obsługa opóźnień w działaniu aplikacji. |
| **datetime** | Pobieranie i formatowanie aktualnej daty oraz czasu na potrzeby logowania i raportowania. |
| **webbrowser** | Automatyczne otwieranie wygenerowanych raportów HTML w domyślnej przeglądarce internetowej użytkownika. |
