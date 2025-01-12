import os
import json
from datetime import datetime

class HistoryManager:
    def __init__(self, base_dir='assistant_history'):
        
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
         
        self.query_dir = os.path.join(self.base_dir, 'queries')
        self.response_dir = os.path.join(self.base_dir, 'responses')
        self.context_file = os.path.join(self.base_dir, 'context.json')
         
        os.makedirs(self.query_dir, exist_ok=True)
        os.makedirs(self.response_dir, exist_ok=True)
         
        if not os.path.exists(self.context_file):
            with open(self.context_file, 'w') as f:
                json.dump({
                    'previous_query': None,
                    'previous_response': None,
                    'conversation_history': []
                }, f, indent=4)

    def save_interaction(self, query, response):
         
        try: 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
             
            query_filename = os.path.join(self.query_dir, f'{timestamp}_query.txt')
            with open(query_filename, 'w', encoding='utf-8') as f:
                f.write(query)
             
            response_filename = os.path.join(self.response_dir, f'{timestamp}_response.txt')
            with open(response_filename, 'w', encoding='utf-8') as f:
                f.write(response)
             
            self._update_context(query, response)
            
        except Exception as e:
            print(f"Error saving interaction history: {e}")

    def _update_context(self, query, response):
        try: 
            with open(self.context_file, 'r') as f:
                context = json.load(f)
                
            context['previous_query'] = query
            context['previous_response'] = response
            
            context['conversation_history'].append({
                'query': query,
                'response': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            context['conversation_history'] = context['conversation_history'][-20:]
             
            with open(self.context_file, 'w') as f:
                json.dump(context, f, indent=4)
        
        except Exception as e:
            print(f"Error updating context: {e}")

    def get_previous_context(self):
        try:
            with open(self.context_file, 'r') as f:
                context = json.load(f)
            return context
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return None

    def clear_history(self): 
        try: 
            for filename in os.listdir(self.query_dir):
                file_path = os.path.join(self.query_dir, filename)
                os.unlink(file_path)
             
            for filename in os.listdir(self.response_dir):
                file_path = os.path.join(self.response_dir, filename)
                os.unlink(file_path)
             
            with open(self.context_file, 'w') as f:
                json.dump({
                    'previous_query': None,
                    'previous_response': None,
                    'conversation_history': []
                }, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False