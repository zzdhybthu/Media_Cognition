"""
Usage:
Recognize speech from microphone input.

Installation:
https://pypi.org/project/SpeechRecognition/
https://pypi.org/project/PyAudio/
"""
import speech_recognition as sr
from constants import *


class Audio():
    def __init__(self):
        self.m = sr.Microphone()
        self.r = sr.Recognizer()
        self.audio = None
        self.text = None
    
    def Listen(self):
        with self.m as source:
            print("Adjusting for ambient noise...")
            self.r.adjust_for_ambient_noise(source)
            print("Say something!")
            self.audio = self.r.listen(source, timeout=RECORD_TIME)
            print("Got it! Now to recognize it...")
    
    def Recognize(self):
        try:
            if MODE == "whisper":
                self.prompt = self.r.recognize_whisper(self.audio, language="english")  # "english" or "chinese"
            elif MODE == "sphinx":
                self.prompt = self.r.recognize_sphinx(self.audio, language="en-US")  # en-US
            else:
                print("Invalid mode")
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Whisper; {e}")
    
    @property
    def Prompt(self):
        return self.prompt


if __name__ == "__main__":
    audio = Audio()
    audio.Listen()
    audio.Recognize()
    print(audio.Prompt)
