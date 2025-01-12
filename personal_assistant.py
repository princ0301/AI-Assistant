import datetime
import webbrowser
import wikipedia
import threading
import time
import winsound  # For Windows sound alerts
import platform

class PersonalAssistant:
    def __init__(self):
        self.active_alarms = []
        self.active_timers = []

    @staticmethod
    def get_current_time(): 
        now = datetime.datetime.now()
        return f"Current time is {now.strftime('%I:%M %p')} on {now.strftime('%d %B %Y')}"

    @staticmethod
    def search_wikipedia(query): 
        try:
            return wikipedia.summary(query, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Try being more specific. Suggestions: {e.options[:3]}"
        except Exception:
            return "Sorry, I couldn't find information on that topic."

    @staticmethod
    def open_website(url): 
        try:
            webbrowser.open(url)
            return f"Opening {url}"
        except Exception as e:
            return f"Error opening website: {e}"

    @staticmethod
    def calculate(expression):
        try:
            return str(eval(expression))
        except Exception:
            return "Sorry, I couldn't perform the calculation."

    def set_alarm(self, alarm_time):
        """
        Set an alarm at a specific time
        :param alarm_time: Time to set the alarm (in 24-hour format 'HH:MM')
        :return: Confirmation message
        """
        try:
            # Parse the alarm time
            alarm_datetime = datetime.datetime.strptime(alarm_time, '%I:%M %p')
            
            # Create a thread for the alarm
            alarm_thread = threading.Thread(target=self._run_alarm, args=(alarm_datetime,))
            alarm_thread.start()
            
            self.active_alarms.append(alarm_thread)
            return f"Alarm set for {alarm_time}"
        except ValueError:
            return "Invalid time format. Please use format like '09:45 PM'"

    def _run_alarm(self, alarm_datetime):
        """
        Internal method to run the alarm
        :param alarm_datetime: Datetime object for the alarm time
        """
        # Adjust alarm to today or next day
        now = datetime.datetime.now()
        alarm_datetime = alarm_datetime.replace(year=now.year, month=now.month, day=now.day)
        
        # If the time has already passed today, set for tomorrow
        if alarm_datetime <= now:
            alarm_datetime += datetime.timedelta(days=1)
        
        # Wait until alarm time
        wait_seconds = (alarm_datetime - datetime.datetime.now()).total_seconds()
        time.sleep(wait_seconds)
        
        # Sound the alarm
        self._sound_alarm()

    def _sound_alarm(self):
        """
        Play alarm sound based on operating system
        """
        os_name = platform.system()
        try:
            if os_name == 'Windows':
                # Windows-specific sound (beeping)
                for _ in range(10):
                    winsound.Beep(1000, 500)  # Frequency 1000Hz, Duration 500ms
            elif os_name == 'Darwin':  # macOS
                os.system('say "Alarm!"')
            else:  # Linux and others
                os.system('paplay /usr/share/sounds/alsa/Front_Center.wav')
        except Exception as e:
            print(f"Error playing alarm sound: {e}")

    def set_timer(self, duration_minutes):
        """
        Set a timer for specified minutes
        :param duration_minutes: Duration of timer in minutes
        :return: Confirmation message
        """
        try:
            duration_seconds = int(duration_minutes) * 60
            
            # Create a thread for the timer
            timer_thread = threading.Thread(target=self._run_timer, args=(duration_seconds,))
            timer_thread.start()
            
            self.active_timers.append(timer_thread)
            return f"Timer set for {duration_minutes} minutes"
        except ValueError:
            return "Invalid duration. Please provide a number of minutes."

    def _run_timer(self, duration_seconds):
        """
        Internal method to run the timer
        :param duration_seconds: Duration of timer in seconds
        """
        time.sleep(duration_seconds)
        self._sound_alarm()  # Use the same alarm sound method

    def cancel_alarm(self, alarm_time=None):
        """
        Cancel specific or all alarms
        :param alarm_time: Optional specific time to cancel
        :return: Cancellation message
        """
        if not alarm_time:
            # Cancel all alarms
            for thread in self.active_alarms:
                thread.join(timeout=1)  # Gracefully stop the thread
            self.active_alarms.clear()
            return "All alarms cancelled"
        
        # TODO: Implement specific alarm cancellation if needed
        return "Specific alarm cancellation not implemented yet"

    def cancel_timer(self, timer_id=None):
        """
        Cancel specific or all timers
        :param timer_id: Optional specific timer to cancel
        :return: Cancellation message
        """
        if not timer_id:
            # Cancel all timers
            for thread in self.active_timers:
                thread.join(timeout=1)  # Gracefully stop the thread
            self.active_timers.clear()
            return "All timers cancelled"
        
        # TODO: Implement specific timer cancellation if needed
        return "Specific timer cancellation not implemented yet"
    
 