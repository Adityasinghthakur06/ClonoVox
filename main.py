import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import wave
import simpleaudio as sa
import speech_recognition as sr
from gtts import gTTS
import numpy as np
from scipy.spatial.distance import cosine
import subprocess

recognizer = sr.Recognizer()
mic = sr.Microphone()
audio_data = None  # To store the recorded audio data
recording_thread = None
stop_flag = threading.Event()
voice_sample_path = ""

# Path to DeepSpeech model and binary
DEEPSPEECH_BIN = "C:/Downloads/deepspeech-0.9.3-models/deepspeech.exe"
MODEL_PATH = "C:/Downloads/deepspeech-0.9.3-models/deepspeech-0.9.3-models.pbmm"
SCORER_PATH = "C:/Downloads/deepspeech-0.9.3-models/deepspeech-0.9.3-models.scorer"


def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def start_recording():
    global recording_thread
    global stop_flag
    global audio_data

    if recording_thread is not None and recording_thread.is_alive():
        messagebox.showerror("Error", "Recording already in progress.")
        return

    stop_flag.clear()
    recording_thread = threading.Thread(target=record_voice)
    recording_thread.start()
    print("Recording thread started.")


def stop_recording():
    global stop_flag
    global recording_thread

    if recording_thread is not None and recording_thread.is_alive():
        stop_flag.set()
        recording_thread.join()  # Wait for the thread to finish
        print("Recording stopped.")
    else:
        messagebox.showinfo("Info", "No active recording to stop.")


def record_voice():
    global audio_data

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            while not stop_flag.is_set():
                audio_data = recognizer.listen(source, timeout=1, phrase_time_limit=None)
                if not stop_flag.is_set():
                    print("Recording complete.")
                    break
        except sr.WaitTimeoutError:
            if not stop_flag.is_set():
                print("Listening timed out while waiting for phrase to start.")

    if audio_data:
        save_audio_file(audio_data)
        print("Audio saved.")


def save_audio_file(audio, filename="recorded_audio.wav"):
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    print(f"Audio file saved as {filename}.")


def play_recording():
    if os.path.exists("recorded_audio.wav"):
        play_audio("recorded_audio.wav")
    else:
        messagebox.showerror("Error", "No recording found. Please record first.")


def synthesize_speech():
    text = text_entry.get()
    if not text:
        messagebox.showerror("Error", "Please enter text to synthesize.")
        return

    if voice_sample_path:
        audio_output = clone_and_synthesize_voice(text)
        play_audio(audio_output)
    else:
        create_wav_from_text(text, "output.wav")
        play_audio("output.wav")


def create_wav_from_text(text, wav_path):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")

    with wave.open(wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        with open("temp.mp3", "rb") as mp3_file:
            wav_file.writeframesraw(mp3_file.read())

    os.remove("temp.mp3")


def clone_and_synthesize_voice(text):
    create_wav_from_text(text, "cloned_output.wav")
    return "cloned_output.wav"


def load_voice_sample():
    global voice_sample_path
    voice_sample_path = filedialog.askopenfilename()


def threaded_load_voice_sample():
    threading.Thread(target=load_voice_sample).start()


def check_similarity():
    voice1 = filedialog.askopenfilename(title="Select first voice sample")
    voice2 = filedialog.askopenfilename(title="Select second voice sample")

    def calculate_and_display_similarity():
        similarity = calculate_similarity(voice1, voice2)
        result_label.config(text=f"Similarity: {similarity * 100:.2f}%")

    threading.Thread(target=calculate_and_display_similarity).start()


def extract_features(audio_path):
    try:
        result = subprocess.run(
            [DEEPSPEECH_BIN, "--model", MODEL_PATH, "--scorer", SCORER_PATH, "--audio", audio_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        features = result.stdout.decode('utf-8')
        return np.array([float(x) for x in features.split() if x.replace('.', '', 1).isdigit()])
    except subprocess.CalledProcessError as e:
        print(f"Error in subprocess: {e}")
        print(f"Subprocess stderr: {e.stderr.decode('utf-8')}")
        messagebox.showerror("Subprocess Error", f"An error occurred in subprocess: {e.stderr.decode('utf-8')}")
        return np.array([])
    except FileNotFoundError:
        print("DeepSpeech executable not found. Please check the path.")
        messagebox.showerror("File Not Found", "DeepSpeech executable not found. Please check the path.")
        return np.array([])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return np.array([])


def calculate_similarity(voice1_path, voice2_path):
    features1 = extract_features(voice1_path)
    features2 = extract_features(voice2_path)
    similarity = 1 - cosine(features1, features2)
    return similarity


app = tk.Tk()
app.title("AI Voice Synthesizer")
app.geometry("400x500")

text_entry = tk.Entry(app, width=50)
text_entry.pack(pady=10)

start_record_button = tk.Button(app, text="Start Recording", command=start_recording)
start_record_button.pack(pady=10)

stop_record_button = tk.Button(app, text="Stop Recording", command=stop_recording)
stop_record_button.pack(pady=10)

play_record_button = tk.Button(app, text="Play Recording", command=play_recording)
play_record_button.pack(pady=10)

load_button = tk.Button(app, text="Load Voice Sample", command=threaded_load_voice_sample)
load_button.pack(pady=10)

synthesize_button = tk.Button(app, text="Synthesize Voice", command=synthesize_speech)
synthesize_button.pack(pady=10)

play_synthesized_button = tk.Button(app, text="Play Synthesized Voice", command=synthesize_speech)
play_synthesized_button.pack(pady=10)

similarity_button = tk.Button(app, text="Check Similarity", command=check_similarity)
similarity_button.pack(pady=10)

result_label = tk.Label(app, text="")
result_label.pack(pady=10)

app.mainloop()
