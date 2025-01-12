import pyttsx3
import speech_recognition as sr
import keyboard
import os
import re
from datetime import datetime
import langdetect
from deep_translator import GoogleTranslator
from alarm import AlarmTimerApp

class MultilingualVoiceAssistant:
    def __init__(self, 
                 system_utils, 
                 personal_assistant, 
                 imdb_assistant, 
                 groq_assistant, 
                 history_manager): 
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('volume', 1.5)
        self.engine.setProperty('rate', 220)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        
        self.system_utils = system_utils
        self.personal_assistant = personal_assistant
        self.imdb_assistant = imdb_assistant
        self.groq_assistant = groq_assistant
        self.history_manager = history_manager
         
        self.translator = GoogleTranslator()
        
        self.alarm_timer_app = AlarmTimerApp()
        
        self.listening = False
        self.recognizer = sr.Recognizer()

    def detect_language(self, text): 
        try:
            return langdetect.detect(text)
        except:
            return 'en'   

    def translate_to_english(self, text, source_lang=None):
        if source_lang is None:
            source_lang = self.detect_language(text)
        
        try:
            return GoogleTranslator(source=source_lang, target='en').translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text   

    def translate_to_original_language(self, text, target_lang): 
        try:
            return GoogleTranslator(source='en', target=target_lang).translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text   

    def speak(self, text, language='en'): 
        print(text) 
        if language != 'en':
            text = self.translate_to_english(text, language)
        
        self.engine.say(text)
        self.engine.runAndWait()

    def process_query(self, query): 
        original_language = self.detect_language(query)
        
        english_query = self.translate_to_english(query, original_language)
         
        try:
            response = self.handle_query_processing(english_query)
            
            localized_response = self.translate_to_original_language(response, original_language)
             
            self.speak(response, original_language)
             
            self.history_manager.save_interaction(query, response)
            
            return response
        
        except Exception as e:
            error_response = f"Sorry, I encountered an error: {str(e)}"
            localized_error = self.translate_to_original_language(error_response, original_language)
            self.speak(error_response, original_language)
            return error_response

    def handle_query_processing(self, query): 
        
        if "system info" in query:
            info = self.system_utils.get_system_info()
            return "\n".join([f"{k}: {v}" for k, v in info.items()])

        if "internet" in query:
            status = "Connected" if self.system_utils.check_internet_connection() else "Not Connected"
            return f"Internet Connection Status: {status}"

        if "time" in query:
            return self.personal_assistant.get_current_time()

        if "wikipedia" in query:
            topic = query.replace("wikipedia", "").strip()
            return self.personal_assistant.search_wikipedia(topic)

        if "open website" in query:
            url = query.replace("open website", "").strip()
            return self.personal_assistant.open_website(url)

        if "calculate" in query:
            expression = query.replace("calculate", "").strip()
            result = self.personal_assistant.calculate(expression)
            return f"Result: {result}"
        
        if "movie" in query or "web series" in query:
            movie_name = query.replace("search", "").replace("movie", "").replace("web series", "").strip()
            movie_info = self.imdb_assistant.search_movie(movie_name)
            if movie_info:
                return f"I found {movie_info['title']} (IMDb Rating: {movie_info['rating']})"
            else:
                return f"Sorry, I couldn't find information for {movie_name}"
    
        return self.groq_assistant.generate_response(query)