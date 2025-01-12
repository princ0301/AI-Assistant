import pyttsx3
import speech_recognition as sr
import keyboard
import os
import sys
import time
import threading
import traceback
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

class VoiceAssistant:
    def __init__(self, groq_api_key=None):
        try:
            self.engine = pyttsx3.init('sapi5')
            self.engine.setProperty('volume', 1.5)
            self.engine.setProperty('rate', 220)
            
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        except Exception as e:
            print(f"Error initializing speech engine: {e}")
            self.engine = None 
            
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.dynamic_energy_threshold = True
        except Exception as e:
            print(f"Error initializing speech recognizer: {e}")
            self.recognizer = None
         
        self.listening = False
        self.stop_flag = False
        self._speech_lock = threading.Lock()
         
        self.groq_client = self.setup_groq_client(groq_api_key)
    
    def setup_groq_client(self, groq_api_key=None):
        if not groq_api_key:
            groq_api_key = os.getenv('GROQ_API_KEY')
         
        if not groq_api_key:
            print("ERROR: No Groq API key found. AI responses will be unavailable.")
            self.speak("Warning: No API key found. AI capabilities are limited.")
            return None
        
        try: 
            client = Groq(api_key=groq_api_key)
             
            test_response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Say hello briefly"}],
                model="llama3-70b-8192",
                max_tokens=50
            )
            print("Groq client successfully initialized.")
            return client
        
        except Exception as e:
            print(f"Failed to set up Groq client: {e}")
            self.speak("Error setting up AI assistant. Functionality will be limited.")
            return None
    
    def speak(self, text):
        def _speak_thread():
            with self._speech_lock:
                print(f"Assistant: {text}")
                try:
                    engine = pyttsx3.init('sapi5')
                    engine.setProperty('volume', 1.5)
                    engine.setProperty('rate', 220)
                    
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
                    
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    print(f"Speech error: {e}")
        
        threading.Thread(target=_speak_thread, daemon=True).start()
    
    def take_command(self):
        
        if not self.recognizer:
            print("Speech recognizer not initialized.")
            return None
        
        try:
            with sr.Microphone() as source:
                print("Listening...") 
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                try: 
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                     
                    query = self.recognizer.recognize_google(audio, language='en-in')
                    print(f"You said: {query}")
                    return query.lower()
                
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                    self.speak("Sorry, I didn't catch that. Could you repeat?")
                    return None
                
                except sr.RequestError:
                    self.speak("Sorry, speech recognition service is unavailable.")
                    return None
                
                except sr.WaitTimeoutError:
                    print("Listening timed out.")
                    return None
        
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def get_ai_response(self, query):
        if not self.groq_client:
            return "AI assistant is not configured. No API key available."
        
        try: 
            full_prompt = f"""
            You are a helpful AI assistant responding to a voice query.
            Provide a concise, clear, and direct response to the following query:
            
            Query: {query}
            
            Response:"""
             
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": full_prompt
                }],
                model="llama3-70b-8192",
                max_tokens=300,
                temperature=0.7
            )
            
            response = chat_completion.choices[0].message.content.strip()
            return response
        
        except Exception as e:
            print(f"AI response generation error: {e}")
            return "Sorry, I encountered an error processing your request."
    
    def setup_shortcuts(self):
        keyboard.add_hotkey('ctrl+alt+s', self.start_listening)
        keyboard.add_hotkey('ctrl+alt+p', self.pause_listening)
        keyboard.add_hotkey('ctrl+alt+q', self.quit_assistant)
    
    def start_listening(self): 
        if not self.listening:
            self.listening = True
            print("Started listening...")
            self.speak("I'm now listening. How can I help you?")
    
    def pause_listening(self): 
        if self.listening:
            self.listening = False
            print("Stopped listening...")
            self.speak("Paused. Press Ctrl+Alt+S to start listening again.")
    
    def quit_assistant(self): 
        self.speak("Goodbye! Shutting down now.")
        self.stop_flag = True
        os._exit(0)
    
    def greet(self): 
        hour = datetime.now().hour
        if 6 <= hour < 12:
            greeting = "Good Morning!"
        elif 12 <= hour < 16:
            greeting = "Good Afternoon!"
        elif 16 <= hour < 21:
            greeting = "Good Evening!"
        else:
            greeting = "Hello!"
        
        self.speak(f"{greeting} I'm your virtual assistant. Press Ctrl+Alt+S to start listening.")
    
    def run(self):
         
        self.greet()
         
        self.setup_shortcuts()
         
        keyboard_thread = threading.Thread(target=keyboard.wait, daemon=True)
        keyboard_thread.start()
         
        while not self.stop_flag:
            try:
                time.sleep(0.1)
                
                if self.listening: 
                    query = self.take_command()
                    
                    if query: 
                        if any(greeting in query for greeting in ["hello", "hi", "hey"]):
                            self.speak("Hello! How can I assist you today?")
                        
                        elif "how are you" in query:
                            self.speak("I'm doing well, thank you for asking!")
                        
                        elif any(time_query in query for time_query in ["what is the time", "current time", "time now"]):
                            current_time = datetime.now().strftime("%I:%M %p")
                            self.speak(f"The current time is {current_time}")
                         
                        else: 
                            if self.groq_client:
                                ai_response = self.get_ai_response(query)
                                self.speak(ai_response)
                            else:
                                self.speak("I understood your query, but I don't have a response configured.")
            
            except KeyboardInterrupt:
                self.quit_assistant()
                break
            except Exception as e:
                print(f"Unexpected error in main loop: {e}")
                traceback.print_exc()

def main(): 
    try: 
        assistant = VoiceAssistant()
        assistant.run()
    
    except Exception as e:
        print(f"Critical error starting assistant: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
