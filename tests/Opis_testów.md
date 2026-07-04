# Testy

Na etapie wyboru technologii przeprowadzono pięć rodzajów testów. Ich celem było wyłonienie narzędzi, które najlepiej spełniają założenia projektowe pod względem wydajności, skuteczności oraz dokładności działania.

---

## Test 1 – Wykrywanie twarzy na obrazie

Pierwszy test skupiał się na porównaniu skuteczności oraz czasu działania różnych metod wykrywania twarzy. Przeprowadzono analizę dla:

- funkcji wykrywania twarzy z biblioteki **DeepFace**,
- funkcji wykrywania twarzy z biblioteki **Face Recognition**,
- biblioteki **OpenCV (cv2)**.

Badanie polegało na wykryciu maksymalnej liczby twarzy na przygotowanych obrazach w możliwie najkrótszym czasie.

### Warianty testowe

1. Obrazy bez zmiany rozmiaru i bez wyszarzenia.
2. Obrazy po zmianie rozmiaru (resize) bez wyszarzenia.
3. Obrazy bez zmiany rozmiaru po wyszarzeniu.
4. Obrazy po zmianie rozmiaru i wyszarzeniu.

Test przeprowadzono na pięciu obrazach testowych.

### Wyniki

Najlepsze rezultaty osiągnęła biblioteka **OpenCV**, uzyskując najkrótszy czas przetwarzania przy zachowaniu skuteczności wykrywania twarzy.

### Wnioski

Z dalszych testów odrzucono wariant bez zmiany rozdzielczości obrazu, ponieważ przetwarzanie obrazów po zmniejszeniu rozdzielczości było zauważalnie szybsze.

---

## Test 2 – Dobór parametrów modelu wykrywania twarzy

Celem drugiego testu była optymalizacja wybranego modelu poprzez dobór odpowiednich parametrów.

### Analizowane parametry

| Parametr | Opis |
|-----------|------|
| `target_size` | Skalowanie obrazów do rozmiaru 1000x1000 pikseli, a w razie potrzeby do największego możliwego rozmiaru. |
| `margin` | Określenie marginesu wokół wykrywanego obszaru twarzy względem punktu centralnego. |
| `scaleFactor` | Współczynnik zmniejszania obrazu podczas kolejnych iteracji detekcji. |
| `minNeighbors` | Minimalna liczba sąsiadujących detekcji wymagana do uznania obiektu za twarz. |

### Wyniki

Przeprowadzone testy pozwoliły dobrać parametry zapewniające najlepszy kompromis pomiędzy czasem działania a skutecznością wykrywania twarzy.

---

## Test 3 – Wybór narzędzia do porównywania twarzy

Celem trzeciego testu było wyłonienie najbardziej efektywnego narzędzia do porównywania twarzy.

### Zbiór danych

Do testów wykorzystano zbiór danych **Labeled Faces in the Wild (LFW)** dostępny w bibliotece **Scikit-Learn**.

Charakterystyka zbioru:

- ponad 2000 par obrazów,
- zdjęcia rzeczywistych osób,
- zróżnicowane warunki oświetleniowe i jakościowe.

### Porównywane rozwiązania

- DeepFace,
- Face Recognition.

### Kryteria oceny

- skuteczność rozpoznawania,
- dokładność,
- czas działania.

### Wyniki

Na podstawie uzyskanych wyników zdecydowano się na wybór biblioteki **Face Recognition**.

Uzyskane parametry:

| Metryka | Wynik |
|----------|--------|
| Skuteczność wykrywania twarzy | **83%** |
| Dokładność rozpoznawania | **90%** |
| Średni czas analizy jednej twarzy | **580 ms** |

### Wnioski

Biblioteka Face Recognition okazała się rozwiązaniem najbardziej dokładnym oraz najszybszym spośród analizowanych technologii.

---

## Test 4 – Wpływ przygotowania obrazu na skuteczność rozpoznawania

Czwarty test miał na celu sprawdzenie wpływu wstępnej obróbki obrazu na działanie modeli rozpoznawania twarzy.

### Analizowane warianty

- rozpoznawanie twarzy bez przygotowania obrazu,
- rozpoznawanie twarzy po przygotowaniu obrazu.

Porównano rozwiązania dostępne w bibliotekach:

- DeepFace,
- Face Recognition.

### Wyniki

Przygotowanie obrazu przed procesem rozpoznawania pozwoliło skrócić czas działania algorytmów przy zachowaniu wysokiej skuteczności.

### Wnioski

Wybrano bibliotekę **Face Recognition** wraz z wcześniejszym przygotowaniem obrazu.

---

## Test 5 – Testy użytkowników końcowych

Ostatni etap badań obejmował testy gotowej aplikacji przeprowadzone z udziałem użytkowników.

### Grupa testowa

W badaniu uczestniczyło pięć osób:

- osoby noszące okulary,
- osoby nienoszące okularów.

### Wyniki

Potwierdzono, że:

- aplikacja poprawnie identyfikuje użytkowników,
- okulary nie wpływają negatywnie na proces weryfikacji,
- system poprawnie rozpoznaje twarze na zdjęciach wykonanych w różnych odstępach czasu.

---

## Podsumowanie testów

Na podstawie przeprowadzonych analiz wybrano następujący stos technologiczny:

### Wykrywanie twarzy

**OpenCV (cv2)**

Dodatkowo zastosowano wstępne przygotowanie obrazu:

- wyszarzenie obrazu,
- zmniejszenie rozdzielczości.

### Porównywanie twarzy

**Face Recognition**

Powody wyboru:

- wysoka dokładność,
- wysoka skuteczność,
- krótki czas działania.

### Osiągnięte wyniki

| Metryka | Wynik |
|----------|--------|
| Skuteczność wykrywania twarzy | **83%** |
| Dokładność rozpoznawania | **90%** |
| Średni czas przetwarzania jednej twarzy | **580 ms** |

Wyniki potwierdziły, że zastosowane rozwiązanie spełnia założenia projektowe pod względem skuteczności, wydajności oraz komfortu użytkowania.

# Wnioski

Projekt systemu obecności i uwierzytelniania użytkowników oparty na technologii rozpoznawania twarzy osiągnął wszystkie założone cele funkcjonalne i technologiczne. Opracowane rozwiązanie stanowi intuicyjne, praktyczne oraz efektywne narzędzie wspierające zarządzanie obecnością pracowników w organizacjach.

Wykorzystanie bibliotek **OpenCV** oraz **Face Recognition** umożliwiło stworzenie systemu łączącego wysoki poziom bezpieczeństwa z prostotą obsługi. Przeprowadzone testy wykazały, że zastosowane algorytmy pozwalają na skuteczną identyfikację użytkowników przy zachowaniu krótkiego czasu przetwarzania oraz wysokiej dokładności działania.

W ramach procesu badawczego przeprowadzono pięć etapów testów, obejmujących między innymi analizę skuteczności wykrywania twarzy, dobór parametrów przetwarzania obrazu, porównanie dostępnych bibliotek służących do rozpoznawania twarzy oraz weryfikację działania gotowej aplikacji z udziałem użytkowników końcowych. Na podstawie uzyskanych wyników wybrano bibliotekę **OpenCV** do wykrywania twarzy oraz bibliotekę **Face Recognition** do ich porównywania.

Analiza wyników potwierdziła, że zastosowanie wstępnego przygotowania obrazu poprzez:

- wyszarzenie obrazu,
- zmniejszenie rozdzielczości,

znacząco wpływa na skrócenie czasu działania systemu bez zauważalnego spadku skuteczności rozpoznawania.

Najważniejsze osiągnięte parametry systemu:

| Metryka | Wynik |
|----------|--------|
| Skuteczność wykrywania twarzy | **83%** |
| Dokładność rozpoznawania | **90%** |
| Średni czas analizy jednej twarzy | **580 ms** |

Przeprowadzone testy z udziałem użytkowników wykazały, że system:

- poprawnie identyfikuje zarejestrowane osoby,
- zachowuje skuteczność działania niezależnie od noszenia okularów,
- poprawnie rozpoznaje użytkowników na zdjęciach wykonanych w różnych odstępach czasu,
- zapewnia wygodny i intuicyjny proces logowania.

Dodatkową zaletą rozwiązania jest implementacja mechanizmu zarządzania rolami użytkowników. Dzięki podziałowi na role:

- **Prezes**,
- **Technik**,
- **Pracownik**,

możliwe jest dostosowanie zakresu funkcjonalności systemu do obowiązków oraz uprawnień poszczególnych grup użytkowników.

Istotnym elementem projektu jest również moduł raportowania, umożliwiający generowanie raportów w formacie HTML. Rozwiązanie to pozwala na łatwe monitorowanie czasu pracy, obecności pracowników oraz analizę zgromadzonych danych bez konieczności korzystania z dodatkowego oprogramowania.

Zaimplementowane mechanizmy bezpieczeństwa, takie jak:

- logowanie przy użyciu rozpoznawania twarzy,
- ochrona dostępu hasłem,
- rejestracja użytkowników za pomocą kamery,
- ograniczenie wielokrotnych prób logowania,

zwiększają poziom ochrony danych oraz minimalizują ryzyko nieautoryzowanego dostępu do systemu.

Realizacja projektu pozwoliła również zdobyć praktyczne doświadczenie związane z przetwarzaniem obrazu, optymalizacją algorytmów oraz implementacją nowoczesnych metod biometrycznych. Wyniki badań potwierdziły, że odpowiedni dobór technologii oraz ich właściwa konfiguracja mają kluczowy wpływ na skuteczność i wydajność całego systemu.

## Możliwe kierunki rozwoju

W przyszłości aplikacja może zostać rozszerzona o dodatkowe funkcjonalności, takie jak:

- integracja z systemami kadrowo-płacowymi,
- integracja z usługami Active Directory lub Microsoft Entra ID,
- obsługa wielu kamer jednocześnie,
- wykorzystanie nowszych modeli sztucznej inteligencji do rozpoznawania twarzy,
- powiadomienia e-mail o zdarzeniach systemowych,
- generowanie raportów w formatach PDF i Excel,
- integracja z systemami kontroli dostępu do budynków.

## Podsumowanie

Opracowany system stanowi nowoczesne i efektywne rozwiązanie wspierające proces zarządzania obecnością oraz autoryzacją użytkowników. Zastosowanie technologii biometrycznych pozwoliło zminimalizować udział czynników ludzkich w procesie identyfikacji, zwiększyć poziom bezpieczeństwa oraz usprawnić codzienną pracę organizacji. Uzyskane wyniki potwierdzają, że rozwiązanie spełnia założenia projektowe i może stanowić podstawę do dalszego rozwoju oraz wdrożeń w przedsiębiorstwach, placówkach edukacyjnych i instytucjach publicznych.
