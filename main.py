import pyttsx3
import speech_recognition as sr
import keyboard
import os
from datetime import datetime
from groq_llm import GroqAssistant
from system_utilities import SystemUtilities
from personal_assistant import PersonalAssistant
from imdb_module import IMDbAssistant
from history_manager import HistoryManager
from language import MultilingualVoiceAssistant

class VoiceAssistant:
    def __init__(self):
        # Initialize existing components
        self.system_utils = SystemUtilities()
        self.personal_assistant = PersonalAssistant()
        self.imdb_assistant = IMDbAssistant()
        self.groq_assistant = GroqAssistant()
        self.history_manager = HistoryManager()
        
        # Initialize Multilingual Voice Assistant
        self.multilingual_assistant = MultilingualVoiceAssistant(
            system_utils=self.system_utils,
            personal_assistant=self.personal_assistant,
            imdb_assistant=self.imdb_assistant,
            groq_assistant=self.groq_assistant,
            history_manager=self.history_manager
        )
        
        # Original TTS setup
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('volume', 1.5)
        self.engine.setProperty('rate', 220)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        
        self.listening = False
        self.recognizer = sr.Recognizer()
        
        keyboard.add_hotkey('ctrl+alt+s', self.start_listening)
        keyboard.add_hotkey('ctrl+alt+p', self.pause_listening)

    def speak(self, text):
        print(text) 
        self.engine.say(text)
        self.engine.runAndWait()

    def greet_me(self):
        hour = datetime.now().hour
        greeting = (
            "Good Morning" if 6 <= hour < 12 else
            "Good Afternoon" if 12 <= hour <= 16 else
            "Good Evening"
        )
        self.multilingual_assistant.speak(f"{greeting}! I'm Ziva, your intelligent assistant. Ready to help!")

    def start_listening(self):
        self.listening = True
        print("Listening activated.")

    def pause_listening(self):
        self.listening = False
        print("Listening paused.")

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"Recognized: {query}")
            return query
        except Exception:
            self.speak("Sorry, could you repeat that?")
            return None

    def run(self):
        self.greet_me()
        while True:
            try:
                if self.listening:
                    query = self.take_command()
                    if query:
                        # Use multilingual assistant to process query
                        self.multilingual_assistant.process_query(query)
            except KeyboardInterrupt:
                self.speak("Assistant terminated.")
                break

    def handle_exit(self):
        hour = datetime.now().hour
        farewell = "Good night, take care!" if 21 <= hour or hour < 6 else "Have a great day!"
        self.speak(farewell)
        exit()

def main():
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()