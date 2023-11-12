from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
import sys

# Import necessary libraries and functions (Same as in your original code)
import requests
import pyaudio
import soundfile as sf
import io
import time
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import pydub
import pygame
load_dotenv()


def streamed_audio(input_text, model='tts-1', voice='alloy'):
    start_time = time.time()
    # OpenAI API endpoint and parameters
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": 'Bearer YOUR_API_KEY',  # Replace with your API key
    }

    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": "opus",
    }

    audio = pyaudio.PyAudio()

    def get_pyaudio_format(subtype):
        if subtype == 'PCM_16':
            return pyaudio.paInt16
        return pyaudio.paInt16

    with requests.post(url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=4096):
                buffer.write(chunk)
            
            buffer.seek(0)

            with sf.SoundFile(buffer, 'r') as sound_file:
                format = get_pyaudio_format(sound_file.subtype)
                channels = sound_file.channels
                rate = sound_file.samplerate

                stream = audio.open(format=format, channels=channels, rate=rate, output=True)
                chunk_size = 1024
                data = sound_file.read(chunk_size, dtype='int16')
                print(f"Time to play: {time.time() - start_time} seconds")

                while len(data) > 0:
                    stream.write(data.tobytes())
                    data = sound_file.read(chunk_size, dtype='int16')

                stream.stop_stream()
                stream.close()
        else:
            print(f"Error: {response.status_code} - {response.text}")

        audio.terminate()

        return f"Time to play: {time.time() - start_time} seconds"

# Example usage
#print(play_text_as_audio("Nuclear energy is clean energy!"))

def not_streamed(input_text, model='tts-1', voice='alloy'):
    start_time = time.time()

    # Initialize Pygame Mixer
    pygame.mixer.init()

    client = OpenAI()

    response = client.audio.speech.create(
        model=model, 
        voice=voice,
        input=input_text,
    )

    response.stream_to_file("output.opus")

    # Load and play the audio file
    pygame.mixer.music.load('output.opus')
    print(f"Time to play: {time.time() - start_time} seconds")
    pygame.mixer.music.play()

    # Loop to keep the script running during playback
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# # Example usage
# print(play_text_as_audio("Nuclear energy is clean energy!"))


def run_streamed():
    input_text = text_box.text()
    streamed_audio(input_text)  # Call the streamed_audio function with input text

def run_not_streamed():
    input_text = text_box.text()
    not_streamed(input_text)  # Call the not_streamed function with input text

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Text to Speech')

layout = QVBoxLayout()

# Caption
caption = QLabel('Text to Speech')
layout.addWidget(caption)

# Textbox
text_box = QLineEdit()
layout.addWidget(text_box)

# Streamed Button
streamed_button = QPushButton('Streamed')
streamed_button.clicked.connect(run_streamed)  # Link button click to streamed_audio function
layout.addWidget(streamed_button)

# Not Streamed Button
not_streamed_button = QPushButton('Not Streamed')
not_streamed_button.clicked.connect(run_not_streamed)  # Link button click to not_streamed function
layout.addWidget(not_streamed_button)

window.setLayout(layout)

window.show()
sys.exit(app.exec_())