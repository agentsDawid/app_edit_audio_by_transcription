import streamlit as st
import openai #import OpenAI
from pydub import AudioSegment
from audiorecorder import audiorecorder
import io
import re
import tempfile
import os
from dotenv import dotenv_values
from hashlib import md5

# Ładowanie zmiennych środowiskowych


# Konfiguracja OpenAI
env = dotenv_values(".env")
if not st.session_state.get("openai_api_key", False):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]

    else:
        st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

# Konfiguracja OpenAI
openai.api_key = st.session_state["openai_api_key"] #os.getenv("OPENAI_API_KEY")

# Konfiguracja strony
st.set_page_config(
    page_title="Edytuj Audio za pomocą Transkrypcji",
    page_icon="🎙️",
    layout="wide"
)

# Tytuł aplikacji
st.title("🎙️ Edytuj Audio za pomocą Transkrypcji")
st.markdown("---")

# Inicjalizacja session state
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'transcription' not in st.session_state:
    st.session_state.transcription = None
if 'transcript_with_timestamps' not in st.session_state:
    st.session_state.transcript_with_timestamps = None
if 'edited_audio' not in st.session_state:
    st.session_state.edited_audio = None
if "note_audio_bytes_md5" not in st.session_state:
    st.session_state["note_audio_bytes_md5"] = None

# Funkcja do transkrypcji audio
def transcribe_audio(audio_bytes, audio_format="mp3"):
    """Transkrybuje audio używając Whisper API"""
    try:
        # Tworzenie tymczasowego pliku
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        # Transkrypcja z timestampami
        with open(tmp_file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        
        # Usuwanie tymczasowego pliku
        os.unlink(tmp_file_path)
        
        return transcript
    except Exception as e:
        st.error(f"Błąd podczas transkrypcji: {str(e)}")
        return None

# Funkcja do wycinania fragmentów z audio
def cut_audio_segments(audio_segment, text_with_markers, words_data):
    # st.write(words_data)
    """Wycina zaznaczone fragmenty z audio"""
    try:
        # Znajdź wszystkie zaznaczone fragmenty [[...]]
        pattern = r'\[\[(.*?)\]\]'
        matches = list(re.finditer(pattern, text_with_markers))
        
        if not matches:
            st.warning("Nie znaleziono żadnych zaznaczonych fragmentów [[...]]")
            return audio_segment
        # Zbierz wyrazy do usunięcia
        phrases_to_remove = [match.group(1).strip() for match in matches]
        # st.write(phrases_to_remove)
        # Znajdź odpowiednie timestampy
        segments_to_remove = []
        
        for phrase in phrases_to_remove:
            phrase_words = phrase.lower().split()
            # st.write(phrase)
            # Szukaj sekwencji słów w danych transkrypcji
            for i in range(len(words_data) - len(phrase_words) + 1):
                # Sprawdź czy sekwencja słów pasuje
                match = True
                for j, word in enumerate(phrase_words):
                    # Użyj notacji atrybutów zamiast słownika
                    word_obj = words_data[i + j]
                    word_text = word_obj.word if hasattr(word_obj, 'word') else word_obj['word']
                    
                    if word_text.lower().strip('.,!?;:') != word.strip('.,!?;:'):
                        match = False
                        break
                
                if match:
                    # Dodaj segment do usunięcia
                    # Użyj notacji atrybutów zamiast słownika
                    start_obj = words_data[i]
                    end_obj = words_data[i + len(phrase_words) - 1]
                    
                    start_time = (start_obj.start if hasattr(start_obj, 'start') else start_obj['start']) * 1000
                    end_time = (end_obj.end if hasattr(end_obj, 'end') else end_obj['end']) * 1000
                    
                    segments_to_remove.append((start_time, end_time))
        
        if not segments_to_remove:
            st.warning("Nie znaleziono pasujących fragmentów w transkrypcji")
            return audio_segment
        
        # Sortuj segmenty według czasu rozpoczęcia
        segments_to_remove.sort()
        
        # Utwórz nowe audio bez zaznaczonych fragmentów
        result_audio = AudioSegment.empty()
        last_end = 0
        
        for start, end in segments_to_remove:
            # Dodaj audio przed wycinanym fragmentem
            if start > last_end:
                result_audio += audio_segment[last_end:start]
            last_end = end
        
        # Dodaj pozostałą część audio
        if last_end < len(audio_segment):
            result_audio += audio_segment[last_end:]
        
        st.success(f"Usunięto {len(segments_to_remove)} fragment(ów)")
        return result_audio
        
    except Exception as e:
        st.error(f"Błąd podczas wycinania audio: {str(e)}")
        return audio_segment
    

#def cut_segments_PYDUB()
#-------------

#-------------
    
# Inicjalizacja danych wczytywanego pliku
def init_file_info():
    st.session_state.file_name = None
    st.session_state.file_size = None
    st.session_state.uploaded_file = None
    # st.session_state.transcription = None
    # st.session_state.edited_audio = None

# Inicjalizacja danych nagranego audio
def init_recorded_info():
    pass

# Wczytanie pliku
def read_files():
    uploaded_file = st.session_state["uploaded_file"]
    if uploaded_file is not None:
        st.session_state.audio_data = uploaded_file.read()
        st.session_state.transcription = None
        st.session_state.edited_audio = None
        st.success("✅ Plik audio załadowany!")
        init_recorded_info()
        
    
# Sekcja 1: Ładowanie/Nagrywanie Audio
st.header("1️⃣ Ładowanie lub Nagrywanie Audio")

col1, col2 = st.columns(2)

with col1: # Wczytanie Audio
    st.subheader("Załaduj plik audio")
    uploaded_file = st.file_uploader(
        "Wybierz plik audio",
        type=['mp3', 'wav', 'ogg', 'm4a', 'flac'],
        help="Obsługiwane formaty: MP3, WAV, OGG, M4A, FLAC",
        accept_multiple_files=False,
        key="uploaded_file",
        on_change=read_files
    )
    if uploaded_file is not None:
        col11, col12 = st.columns(2)

        with col11:
            st.metric("Nazwa pliku", uploaded_file.name)
        with col12:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.metric("Rozmiar", f"{file_size_mb:.2f} MB")
    
with col2: # Nagranie audio
    st.subheader("Lub nagraj audio")
    audio = audiorecorder("🎤 Rozpocznij nagrywanie", "⏹️ Zatrzymaj nagrywanie",key="recorder_data")
    
    if len(audio) > 0:
        # Konwertuj nagranie do bajtów
        audio_bytes = io.BytesIO()
        audio.export(audio_bytes, format="wav")
        st.session_state["note_audio_bytes"] = audio_bytes.getvalue()
        current_md5 = md5(st.session_state["note_audio_bytes"]).hexdigest()
        if st.session_state["note_audio_bytes_md5"] != current_md5:
            st.session_state["note_audio_bytes_md5"] = current_md5
            st.session_state.audio_data = audio_bytes.getvalue()
            st.session_state.transcription = None
            st.session_state.edited_audio = None
            st.success("✅ Audio nagrane!")

# Wyświetlanie załadowanego audio
if st.session_state.audio_data:
    st.markdown("---")
    st.subheader("🔊 Podgląd Audio")
    st.audio(st.session_state.audio_data)

# Sekcja 2: Transkrypcja
if st.session_state.audio_data:
    st.markdown("---")
    st.header("2️⃣ Transkrypcja Audio")
    
    if st.button("🎯 Transkrybuj Audio", type="primary", use_container_width=True):
        with st.spinner("Transkrybuję audio... Proszę czekać..."):
            result = transcribe_audio(st.session_state.audio_data)
            
            if result:
                # Zapisz pełną transkrypcję
                st.session_state.transcription = result.text
                
                # Zapisz dane z timestampami słów
                if hasattr(result, 'words') and result.words:
                    st.session_state.transcript_with_timestamps = result.words
                else:
                    st.warning("Brak danych o timestampach słów")
                    st.session_state.transcript_with_timestamps = []
                
                st.success("✅ Transkrypcja zakończona!")

# Sekcja 3: Edycja Transkrypcji
if st.session_state.transcription:
    st.markdown("---")
    st.header("3️⃣ Edycja Transkrypcji")
    
    st.info("💡 **Instrukcja:** Zaznacz niechciane słowa lub frazy używając podwójnych nawiasów kwadratowych `[[tekst do usunięcia]]`")
    
    # Pole tekstowe do edycji
    edited_text = st.text_area(
        "Transkrypcja (zaznacz fragmenty do usunięcia używając [[...]])",
        value=st.session_state.transcription,
        height=300,
        help="Zaznacz tekst do usunięcia w ten sposób: [[fragment do usunięcia]]"
    )
    
    # Przykład użycia
    with st.expander("📝 Zobacz przykład"):
        st.markdown("""
        **Oryginalny tekst:**
        ```
        Witam wszystkich na dzisiejszym spotkaniu. Hmm, dzisiaj będziemy rozmawiać o projekcie.
        ```
        
        **Po zaznaczeniu fragmentów do usunięcia:**
        ```
        Witam wszystkich na dzisiejszym spotkaniu. [[Hmm,]] dzisiaj będziemy rozmawiać o projekcie.
        ```
        
        **Rezultat:** Audio bez słowa "Hmm,"
        """)

# Sekcja 4: Generowanie Edytowanego Audio
if st.session_state.transcription and st.session_state.transcript_with_timestamps:
    st.markdown("---")
    st.header("4️⃣ Generowanie Edytowanego Audio")
    
    if st.button("✂️ Wytnij Zaznaczone Fragmenty", type="primary", use_container_width=True):
        if '[[' in edited_text and ']]' in edited_text:
            with st.spinner("Wycinam zaznaczone fragmenty... Proszę czekać..."):
                # Załaduj audio do pydub
                audio_segment = AudioSegment.from_file(io.BytesIO(st.session_state.audio_data))
                
                # Wytnij fragmenty
                edited_audio_segment = cut_audio_segments(
                    audio_segment,
                    edited_text,
                    st.session_state.transcript_with_timestamps
                )
                
                # Zapisz do bajtów
                output_buffer = io.BytesIO()
                edited_audio_segment.export(output_buffer, format="mp3")
                st.session_state.edited_audio = output_buffer.getvalue()
        else:
            st.warning("⚠️ Nie znaleziono żadnych zaznaczonych fragmentów [[...]]")

# Sekcja 5: Wynik
if st.session_state.edited_audio:
    st.markdown("---")
    st.header("5️⃣ Edytowane Audio")
    
    st.success("✅ Audio zostało pomyślnie edytowane!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎵 Oryginalne Audio")
        st.audio(st.session_state.audio_data)
    
    with col2:
        st.subheader("✨ Edytowane Audio")
        st.audio(st.session_state.edited_audio)
    
    # Przycisk pobierania
    st.download_button(
        label="⬇️ Pobierz Edytowane Audio",
        data=st.session_state.edited_audio,
        file_name="edytowane_audio.mp3",
        mime="audio/mp3",
        use_container_width=True
    )
    
# Stopka
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🎙️ Aplikacja do edycji audio za pomocą transkrypcji | Powered by Streamlit & OpenAI Whisper</p>
    </div>
    """,
    unsafe_allow_html=True
)
