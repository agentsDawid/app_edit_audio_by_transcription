# 🎙️ Edytuj Audio za pomocą Transkrypcji

Aplikacja Streamlit do edycji plików audio poprzez zaznaczanie niechcianych fragmentów w transkrypcji.

## 📋 Opis działania

1. **Załaduj lub nagraj audio** - możesz załadować plik audio lub nagrać własny
2. **Odtwórz audio** - sprawdź nagranie przed transkrypcją
3. **Transkrybuj** - kliknij przycisk "Transkrybuj" aby utworzyć transkrypcję tekstu
4. **Zaznacz fragmenty** - zaznacz niechciane słowa/frazy używając `[[ ... ]]`
5. **Wytnij** - kliknij przycisk "Wytnij" aby otrzymać plik audio bez zaznaczonych fragmentów

## 🔧 Instalacja

### Krok 1: Przygotowanie środowiska

Otwórz terminal i wykonaj następujące polecenia:

```bash
# Aktywuj środowisko conda
conda activate od_zera_do_ai

# Dodaj kanał conda-forge
conda config --append channels conda-forge

# Zainstaluj wymagane pakiety
conda install -y streamlit ffmpeg pydub openai==1.47.0 python-dotenv

# Zainstaluj streamlit-audiorecorder przez pip
pip install streamlit-audiorecorder
```

### Krok 2: Konfiguracja klucza OpenAI API

1. Utwórz konto na https://platform.openai.com/
2. Wygeneruj klucz API w sekcji API Keys
3. Otwórz plik `.env` i wpisz swój klucz:

```
OPENAI_API_KEY=sk-twoj-klucz-api-tutaj
```

**WAŻNE:** Nie udostępniaj nigdy swojego klucza API!

## 🚀 Uruchomienie

W terminalu, w katalogu z plikiem `audio_editor.py`, wykonaj:

```bash
streamlit run audio_editor.py
```

Aplikacja otworzy się automatycznie w przeglądarce pod adresem `http://localhost:8501`

## 📖 Instrukcja użytkowania

### Ładowanie audio
- **Opcja 1:** Kliknij "Browse files" i wybierz plik audio (MP3, WAV, OGG, M4A, FLAC)
- **Opcja 2:** Kliknij "🎤 Rozpocznij nagrywanie" aby nagrać własne audio

### Transkrypcja
1. Po załadowaniu audio, kliknij przycisk **"🎯 Transkrybuj Audio"**
2. Poczekaj na zakończenie transkrypcji (może to potrwać kilka sekund)
3. Transkrypcja pojawi się w polu tekstowym

### Edycja transkrypcji
1. W polu tekstowym znajdź fragmenty, które chcesz usunąć z audio
2. Zaznacz je używając podwójnych nawiasów kwadratowych: `[[fragment do usunięcia]]`

**Przykład:**
```
Witam wszystkich na dzisiejszym spotkaniu. [[Hmm,]] dzisiaj [[eee]] będziemy rozmawiać o projekcie.
```

### Generowanie edytowanego audio
1. Kliknij przycisk **"✂️ Wytnij Zaznaczone Fragmenty"**
2. Poczekaj na przetworzenie audio
3. Posłuchaj wyniku i pobierz plik przyciskiem **"⬇️ Pobierz Edytowane Audio"**

## 📦 Zależności

- `streamlit` - interfejs użytkownika
- `streamlit-audiorecorder` - nagrywanie audio
- `openai` (v1.47.0) - API do transkrypcji (Whisper-1)
- `pydub` - obróbka plików audio
- `python-dotenv` - zarządzanie zmiennymi środowiskowymi
- `ffmpeg` - wymagane przez pydub do konwersji audio

## 🔍 Rozwiązywanie problemów

### Błąd: "ffmpeg not found"
Upewnij się, że zainstalowałeś ffmpeg przez conda:
```bash
conda install -y ffmpeg
```

### Błąd: "Invalid API key"
1. Sprawdź czy plik `.env` zawiera prawidłowy klucz API
2. Upewnij się, że klucz zaczyna się od `sk-`
3. Sprawdź czy masz środki na koncie OpenAI

### Aplikacja nie znajduje fragmentów do usunięcia
1. Sprawdź czy używasz podwójnych nawiasów kwadratowych: `[[tekst]]`
2. Upewnij się, że zaznaczony tekst dokładnie odpowiada transkrypcji
3. Model Whisper może nieznacznie różnić się w transkrypcji (np. interpunkcja)

## 💡 Wskazówki

- Im lepsza jakość audio, tym lepsza transkrypcja
- Możesz zaznaczać wiele fragmentów w jednym przebiegu
- Zachowaj oryginalne audio przed edycją
- Testuj na krótkich nagraniach przed długimi plikami

## 🎯 Przykłady użycia

1. **Usuwanie parazytu językowych:** Usuń "eee", "hmm", "no więc" z nagrań
2. **Czyszczenie podcastów:** Wytnij nieudane fragmenty lub kaszlnięcia
3. **Edycja prezentacji:** Usuń pomyłki z nagranych prezentacji
4. **Obróbka wywiadów:** Usuń poufne informacje z nagrań

## 📄 Licencja

Ten projekt jest dostępny dla celów edukacyjnych.

## 🤝 Wsparcie

Jeśli masz problemy:
1. Sprawdź sekcję "Rozwiązywanie problemów"
2. Upewnij się, że wszystkie zależności są zainstalowane
3. Sprawdź logi w terminalu

---

**Autor:** Aplikacja AI
**Wersja:** 1.0
**Data:** 2026
