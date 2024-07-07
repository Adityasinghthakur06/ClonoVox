import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Please say something...")

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)  # Listen with a timeout of 5 seconds
            print("Processing...")

            # Save the captured audio to a file for debugging
            with open("captured_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

        try:
            transcription = recognizer.recognize_sphinx(audio)
            print(f"You said: {transcription}")
        except sr.RequestError as e:
            print(f"Sphinx recognition error: {e}")
        except sr.UnknownValueError:
            print("Unable to recognize speech")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_microphone()
