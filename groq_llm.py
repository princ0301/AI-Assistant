import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

class GroqAssistant:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.system_prompt = """
        You are Ziva, an AI voice assistant with these core characteristics:
        - Be direct, helpful, and empathetic
        - Understand context and nuance quickly
        - Provide precise, actionable responses
        - Maintain a warm, supportive tone
        - Adapt communication style to user's needs

        Response Strategy:
        1. For simple queries: Give a crisp, immediate answer
        2. For complex topics: Offer structured, clear explanation
        3. Avoid unnecessary elaboration
        4. Use natural, conversational language
        5. Show genuine interest in user's context

        Your primary goal is to be genuinely helpful and make the user's life easier.
        """

    def generate_response(self, user_query):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query}
                ],
                model="llama3-70b-8192",
                max_tokens=200,   
                temperature=0.6   
            )
            
            response = chat_completion.choices[0].message.content
            return response.strip()   
        
        except Exception as e:
            return f"Apologies, I'm experiencing a technical difficulty. {str(e)}"