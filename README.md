<h1 align="center">LLM Experiments 🧪</h1>

<p align="center">
    <a href="https://twitter.com/geepytee">
        <img src="https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40geepytee" alt="Twitter URL">
    </a>
    <a href="mailto:gonzalo@double.bot">
        <img src="https://img.shields.io/badge/Say%20hi%20-2563eb" alt="Say Hi">
    </a>
    <a href="https://www.double.bot">
        <img src="https://img.shields.io/badge/Install%20Double.bot%20-3b82f6" alt="Say Hi">
    </a>
</p>

<p>This is a personal repository with different LLM-based projects I've built. Click on 'Demo video' to see a video demonstration of every one of the projects in action! Also consider installing <a href="https://www.double.bot">Double.bot</a>, this is the AI copilot I use to build these projects.</p>


____

### 1. Button.py <a href="https://x.com/geepytee/status/1723799639000834174?s=20"> <img src="https://img.shields.io/badge/Demo%20video%20-dc2626"> </a>
This file launches a simple UI with a textbox for inputs and a button. All you have to do is write some text into the textbox and push the button, then this message is sent to OpenAI's Text to speech (TTS) endpoint. You can have your message either streamed back (basically it will start playing before the full audio output is done being created), or not streamed (it will not play until the full TTS audio file has been created).

The purpose of this file is to show how much of an advantage streaming provides, plus provide basic code to implement streaming on your own. For some reason OpenAI mentions it on their documentation as something you can do, but provides no working examples, so here's mine for you :)


### 2. narrator.ipynb <a href="https://x.com/geepytee/status/1721705524176257296?s=20"> <img src="https://img.shields.io/badge/Demo%20video%20-dc2626"> </a>
This script takes an mp4 file in your local directory, and generates a narration of the contents in the video.
Make sure to tweak the system prompt for best results.


### 3. streamed_text_plus_streamed_audio.py <a href="https://x.com/geepytee/status/1726884940288229378?s=20"> <img src="https://img.shields.io/badge/Demo%20video%20-dc2626"> </a>
In this file we make use of two different types of streaming.
First, you have to input a message (try: How are you?). Then, this message is sent to gpt-3.5-turbo to generate a response. The response it generates is streamed into TTS (I chunk it so every time there is a period or ?! it sends a request to TTS), and the audio from TTS is streamed back as seen in the button.py file.
