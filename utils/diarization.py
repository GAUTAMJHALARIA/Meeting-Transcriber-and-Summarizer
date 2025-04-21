from pyannote.audio import Pipeline
import torch
import datetime

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="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")

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def diarize_speakers(wav_path):
    diarization = pipeline(wav_path)
    return diarization

def format_speaker_segments(diarization, transcribed_segments):
    speaker_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speaker_text = ""
        for segment in transcribed_segments:
            if segment["start"] >= turn.start and segment["end"] <= turn.end:
                speaker_text += segment["text"] + " "
        if speaker_text:
            speaker_segments.append({
                "speaker": speaker,
                "start": format_time(turn.start),
                "end": format_time(turn.end),
                "text": speaker_text.strip()
            })
    return speaker_segments
