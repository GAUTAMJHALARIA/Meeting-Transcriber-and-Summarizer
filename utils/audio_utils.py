from pydub import AudioSegment
import os

def save_and_convert_audio(uploaded_file, output_path="temp.wav"):
    input_path = "temp_input.mp3"
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    audio = AudioSegment.from_file(input_path, format="mp3")
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(output_path, format="wav", codec="pcm_s16le")

    os.remove(input_path)
    return output_path
