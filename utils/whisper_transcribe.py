from faster_whisper import WhisperModel
from pydub import AudioSegment
import wave
import contextlib
import os
import streamlit as st
from tqdm import tqdm

def transcribe_audio(wav_path):
    # Initialize the Whisper model
    model = WhisperModel("base", device="cpu", compute_type="int8")

    # Get duration of WAV
    with contextlib.closing(wave.open(wav_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    # Transcribe with Whisper
    segments, _ = model.transcribe(wav_path, beam_size=5)
    transcribed_segments = []

    with tqdm(total=duration, desc="Transcribing", unit="sec") as pbar:
        last_progress = 0
        for segment in segments:
            transcribed_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })

            current_progress = min(segment.end, duration)
            pbar.update(current_progress - last_progress)
            last_progress = current_progress

    return segments, transcribed_segments, duration