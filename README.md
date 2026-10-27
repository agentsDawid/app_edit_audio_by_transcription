# 🎙️ Audio Editor by Transcription

**Edit audio by editing its transcript.**

A Streamlit application for removing unwanted passages from recordings by marking words or phrases in an AI-generated transcript — without manually editing an audio timeline.

![Python](https://img.shields.io/badge/Python-Project-blue?logo=python) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit) ![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai) ![Whisper](https://img.shields.io/badge/Whisper-Transcription-green) ![Pydub](https://img.shields.io/badge/Pydub-Audio-blue) ![FFmpeg](https://img.shields.io/badge/FFmpeg-Media-green)

## Overview

**Audio Editor by Transcription** combines speech-to-text transcription with automated audio processing. Users mark unwanted phrases in the transcript, and the application removes the corresponding audio sections using transcription timestamps.

### Key features

- **Upload or record audio** directly in the browser.
- **Transcribe speech** with OpenAI Whisper.
- **Edit by text** using `[[double brackets]]` around unwanted words or phrases.
- **Automatically trim audio** based on transcription timestamps.
- **Preview and download** the resulting recording.

## How it works

1. Upload an audio file or record a new one.
2. Preview the original recording.
3. Generate a transcript with OpenAI Whisper.
4. Mark unwanted words or phrases with `[[...]]`.
5. Process, listen to, and download the edited audio.

### Editing example

**Original transcript**

```text
Welcome to today's meeting. Hmm, today we will, um, discuss the project.
```

**Marked transcript**

```text
Welcome to today's meeting. [[Hmm,]] today we will, [[um,]] discuss the project.
```

**Expected text after editing**

```text
Welcome to today's meeting. Today we will discuss the project.
```

The audio segments are removed using transcription timestamps. Cutting accuracy depends on speech recognition and word alignment.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| OpenAI Whisper (`whisper-1`) | Speech transcription |
| Pydub | Audio manipulation |
| FFmpeg | Audio decoding and conversion |
| streamlit-audiorecorder | In-browser recording |
| python-dotenv | Environment variable management |

## Getting started

### Requirements

- Conda and Python 3.11
- OpenAI API key
- FFmpeg

### Installation

```bash
git clone https://github.com/agentsDawid/app_edit_audio_by_transcription.git
cd app_edit_audio_by_transcription
conda create -n audio-editor python=3.11 -y
conda activate audio-editor
conda install -c conda-forge ffmpeg -y
python -m pip install streamlit "openai==1.47.0" pydub python-dotenv streamlit-audiorecorder
```

### API configuration

Create a `.env` file in the project directory:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

### Run

```bash
streamlit run audio_editor.py
```

## Use cases

- **Podcasts:** remove filler words and false starts.
- **Interviews:** cut unwanted spoken passages.
- **Presentations:** remove mistakes without rerecording everything.
- **Educational content:** clean up lectures and explanations.

## Limitations and privacy

- Results depend on transcription accuracy and timestamp alignment.
- Overlapping voices, background noise, and short pauses can reduce cutting precision.
- Review the output for unnatural transitions before publishing.
- Transcription requires internet access and uses the OpenAI API; recordings are sent to OpenAI for processing.
- Avoid uploading confidential recordings without appropriate authorization.


**Repository:** [app_edit_audio_by_transcription](https://github.com/agentsDawid/app_edit_audio_by_transcription)
