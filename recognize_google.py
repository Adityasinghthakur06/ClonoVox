import speech_recognition as sr

def verify_recognizer():
    recognizer = sr.Recognizer()
    methods = dir(recognizer)
    print("Available methods in Recognizer:")
    for method in methods:
        print(method)

if __name__ == "__main__":
    verify_recognizer()
