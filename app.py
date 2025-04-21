import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import os
import json
from pydub import AudioSegment
import ffmpeg_static



# Environment fixes
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_static.__file__)
os.environ["SPEECHBRAIN_CACHE"] = "./.cache"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
os.environ["TRANSFORMERS_CACHE"] = "./.cache/huggingface"
os.environ["HUGGINGFACE_HUB_CACHE"] = "./.cache/huggingface"

# Local modules
from utils.whisper_transcribe import transcribe_audio
from utils.diarization import diarize_speakers, format_speaker_segments
from utils.gemini_utils import generate_summary, extract_topics, extract_actions, highlight_decisions

st.set_page_config(page_title="Smart Meeting Assistant", layout="wide")
st.title("🎷 AI Meeting Transcriber + Smart Insights")

st.sidebar.header("📂 Upload Audio File")
audio_file = st.sidebar.file_uploader("Choose a .mp3 file", type=["mp3"])

@st.cache_resource(show_spinner=False)
def convert_and_save_audio(uploaded_file):
    mp3_path = "temp_input.mp3"
    wav_path = "temp.wav"

    with open(mp3_path, "wb") as f:
        f.write(uploaded_file.read())

    audio = AudioSegment.from_file(mp3_path, format="mp3")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(wav_path, format="wav", codec="pcm_s16le")

    return wav_path

@st.cache_resource(show_spinner=False)
def cached_transcribe_audio(wav_path):
    return transcribe_audio(wav_path)

@st.cache_resource(show_spinner=False)
def cached_diarize_speakers(audio_mapping):
    return diarize_speakers(audio_mapping)

if audio_file:
    st.audio(audio_file, format="audio/wav")

    wav_path = convert_and_save_audio(audio_file)

    with st.spinner("Transcribing with Whisper..."):
        segments, transcribed_segments, duration = cached_transcribe_audio(wav_path)

    with st.spinner("Diarizing Speakers..."):
        diarization = cached_diarize_speakers({"audio": wav_path})
        speaker_segments = format_speaker_segments(diarization, transcribed_segments)

    st.success("✅ Transcription and Diarization complete!")

    if st.checkbox("🔍 Show Transcription + Diarization"):
        with st.expander("View Transcript"):
            for s in speaker_segments:
                st.markdown(f"**{s['speaker']}** [{s['start']} - {s['end']}]: {s['text']}")

        if st.download_button("📁 Download as JSON", json.dumps(speaker_segments, indent=2), file_name="meeting_transcript.json", mime="application/json"):
            st.success("Transcript downloaded!")

    st.header("💡 Generate Meeting Insights")
    full_text = "\n".join([f"{s['speaker']}: {s['text']}" for s in speaker_segments])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Generate Summary"):
            st.markdown(generate_summary(full_text))

        if st.button("📌 Extract Topics"):
            st.markdown(extract_topics(full_text))

    with col2:
        if st.button("✅ Action Items"):
            st.markdown(extract_actions(full_text))

        if st.button("🔦 Highlight Decisions"):
            st.markdown(highlight_decisions(full_text))
