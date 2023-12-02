
**button.py**
This file launches a simple UI with a textbox for inputs and a button. All you have to do is write some text into the textbox and push the button, then this message is sent to OpenAI's Text to speech (TTS) endpoint. You can have your message either streamed back (basically it will start playing before the full audio output is done being created), or not streamed (it will not play until the full TTS audio file has been created).

The purpose of this file is to show how much of an advantage streaming provides, plus provide basic code to implement streaming on your own. For some reason OpenAI mentions it on their documentation as something you can do, but provides no working examples, so here's mine for you :)


**narrator.ipynb**
This file allows you to create narrations as seen in this tweet: https://x.com/geepytee/status/1721705524176257296?s=20
All you need is to have an mp4 file in your local directory, and maybe tweak the system prompt a bit.


**streamed_text_plus_streamed_audio.py**
In this file we make use of two different types of streaming.
First, you have to input a message (try: How are you?). Then, this message is sent to gpt-3.5-turbo to generate a response. The response it generates is streamed into TTS (I chunk it so every time there is a period or ?! it sends a request to TTS), and the audio from TTS is streamed back as seen in the button.py file.