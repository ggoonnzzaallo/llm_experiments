import requests, pyaudio, time, pygame, threading, queue, tempfile
import soundfile as sf
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
is_first_audio_played = False  # Flag to check if the first audio has been played
client = OpenAI()

# Queues for audio generation and playback
audio_generation_queue = queue.Queue()
audio_playback_queue = queue.Queue()

# Initialize Pygame Mixer at the start
pygame.mixer.init()

def process_audio_generation_queue():
    while True:
        input_text = audio_generation_queue.get()
        if input_text is None:
            break
        audio_file_path = generate_audio(input_text)
        audio_playback_queue.put(audio_file_path)
        audio_generation_queue.task_done()

def process_audio_playback_queue():
    #time.sleep(10) #Debug Only
    while True:
        audio_file_path = audio_playback_queue.get()
        if audio_file_path is None:
            #print("No audio file path found") #Debug Only
            break
        #print(audio_file_path) #Debug Only
        play_audio(audio_file_path)
        audio_playback_queue.task_done()

# Threads for processing the audio generation and playback queues
audio_generation_thread = threading.Thread(target=process_audio_generation_queue)
audio_generation_thread.start()

audio_playback_thread = threading.Thread(target=process_audio_playback_queue)
audio_playback_thread.start()

def generate_audio(input_text, model='tts-1', voice='alloy'):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": 'Bearer YOUR_API_KEY'  # Replace with your actual API key
    }
    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": "opus",
    }

    with requests.post(url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.opus') as temp_file:
                for chunk in response.iter_content(chunk_size=4096):
                    temp_file.write(chunk)
                #print(temp_file.name) #Debug Only
                return temp_file.name
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

def play_audio(audio_file_path):
    if audio_file_path:
         # Calculate the time elapsed since the start of the script
        elapsed_time = time.time() - start_time
        print(f"Time taken to start playing audio clip: {elapsed_time} seconds")
        #print("Attempting to play audio.") #Debug Only
        with sf.SoundFile(audio_file_path, 'r') as sound_file:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=sound_file.channels, rate=sound_file.samplerate, output=True)
            data = sound_file.read(1024,dtype='int16')
            
            while len(data) > 0:
                stream.write(data.tobytes())
                data = sound_file.read(102,dtype='int16')

            stream.stop_stream()
            stream.close()
            audio.terminate()

def print_w_stream(message):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a friendly AI assistant."},
            {"role": "user", "content": message},
        ],
        stream=True,
        temperature=0, #Set to 0 for benchmarking
        max_tokens=500,
    )

    sentence = ''
    sentences = []
    sentence_end_chars = {'.', '?', '!', '\n'}

    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content is not None:
            for char in content:
                sentence += char
                if char in sentence_end_chars:
                    sentence = sentence.strip()
                    if sentence and sentence not in sentences:
                        sentences.append(sentence)
                        audio_generation_queue.put(sentence)
                        print(f"Queued sentence: {sentence}")  # Logging queued sentence
                    sentence = ''
    return sentences

def cleanup_queues():
    audio_generation_queue.join()  # Wait for audio generation queue to be empty
    audio_generation_queue.put(None)  # Signal the end of audio generation
    audio_playback_queue.join()  # Wait for audio playback queue to be empty
    audio_playback_queue.put(None)  # Signal the end of audio playback

# Prompt the user for input
user_input = input("What do you want to ask the AI? ")
start_time = time.time()  # Record the start time


print_w_stream(user_input)

cleanup_queues()  # Initiate the cleanup process

audio_generation_thread.join()    # Wait for the audio generation thread to finish
audio_playback_thread.join()      # Wait for the audio playback thread to finish
pygame.mixer.quit()               # Close the Pygame mixer