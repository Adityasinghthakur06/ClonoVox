# VoiceSynth AI

VoiceSynth AI is a comprehensive project that enables voice recording, synthesis, cloning, and similarity checking using AI technologies. This project allows users to record their voice, synthesize speech from text, clone a voice from a sample, and compare the similarity between different voice samples.

## Features

- **Voice Recording**: Record audio using a microphone.
- **Voice Playback**: Play back recorded audio.
- **Text-to-Speech Synthesis**: Synthesize speech from entered text using Google Text-to-Speech.
- **Voice Cloning**: Clone and synthesize a voice using a provided sample.
- **Voice Similarity Checking**: Compare and display the similarity between two voice samples using DeepSpeech.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/VoiceSynthAI.git
   cd VoiceSynthAI
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Download and set up DeepSpeech model:

Download the DeepSpeech model and scorer files from DeepSpeech GitHub Releases.
Place the downloaded files in a directory, e.g., C:/Downloads/deepspeech-0.9.3-models/.
Ensure the paths in the script are correctly set to these files.
Usage
Run the application:

bash
Copy code
python main.py
Use the GUI to interact with the application:

Start Recording: Click the "Start Recording" button to record audio.
Stop Recording: Click the "Stop Recording" button to stop the recording.
Play Recording: Click the "Play Recording" button to play back the recorded audio.
Synthesize Voice: Enter text and click the "Synthesize Voice" button to create speech from text.
Play Synthesized Voice: Click the "Play Synthesized Voice" button to play the synthesized speech.
Load Voice Sample: Click the "Load Voice Sample" button to load a voice sample from a file.
Check Similarity: Click the "Check Similarity" button to select two voice samples and check their similarity.
Requirements
Python 3.6+
Required Python packages (listed in requirements.txt):
tkinter
simpleaudio
SpeechRecognition
gtts
scipy
numpy

Acknowledgments
Mozilla DeepSpeech for the speech recognition model.
Google Text-to-Speech for the text-to-speech functionality.
Pydub for audio processing.
Simpleaudio for audio playback.
