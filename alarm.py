import datetime
import time
import threading
import pygame
import sys

AUDIO_FILE_PATH = r"D:\Projects\Llama3-Voice-Assistant\AI Assistant\assistant\media\Warriyo - Mortals (feat. Laura Brehm) Future Trap NCS - Copyright Free Music.mp3"

class AlarmTimerApp:
    def __init__(self):
        pygame.mixer.init()
        self.alarms = {}
        self.timers = {}
        self.stop_flags = {}

    def play_sound(self):
        """Play predefined audio file"""
        try:
            pygame.mixer.music.load(AUDIO_FILE_PATH)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing audio: {e}")

    def set_alarm(self, name, time_str):
        """Set an alarm for a specific time"""
        try:
            alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            
            # Reset stop flag
            self.stop_flags[name] = False
            
            def check_alarm():
                while not self.stop_flags.get(name, False):
                    current_time = datetime.datetime.now().time()
                    if current_time.hour == alarm_time.hour and current_time.minute == alarm_time.minute:
                        print(f"Alarm '{name}' triggered!")
                        self.play_sound()
                        break
                    time.sleep(1)

            # Remove any existing alarm with the same name
            self.cancel_alarm(name)

            # Create and start a new alarm thread
            thread = threading.Thread(target=check_alarm, daemon=True)
            thread.start()
            
            self.alarms[name] = alarm_time
            print(f"Alarm '{name}' set for {time_str}")
        except ValueError:
            print("Invalid time format. Use HH:MM format.")

    def set_timer(self, name, duration_seconds):
        """Set a timer for a specific duration"""
        # Reset stop flag
        self.stop_flags[name] = False
        
        def timer_countdown():
            start_time = time.time()
            while time.time() - start_time < duration_seconds:
                if self.stop_flags.get(name, False):
                    return
                time.sleep(0.1)
            
            if not self.stop_flags.get(name, False):
                print(f"Timer '{name}' completed!")
                self.play_sound()

        # Remove any existing timer with the same name
        self.cancel_timer(name)

        # Create and start a new timer thread
        thread = threading.Thread(target=timer_countdown, daemon=True)
        thread.start()
        
        self.timers[name] = duration_seconds
        print(f"Timer '{name}' set for {duration_seconds} seconds")

    def cancel_alarm(self, name):
        """Cancel a specific alarm"""
        if name in self.alarms:
            # Set stop flag to true
            self.stop_flags[name] = True
            del self.alarms[name]
            print(f"Alarm '{name}' canceled")
        else:
            print(f"No alarm named '{name}' found")

    def cancel_timer(self, name):
        """Cancel a specific timer"""
        if name in self.timers:
            # Set stop flag to true
            self.stop_flags[name] = True
            del self.timers[name]
            print(f"Timer '{name}' canceled")
        else:
            print(f"No timer named '{name}' found")

    def list_alarms(self):
        """List all active alarms"""
        print("Active Alarms:")
        for name, time in self.alarms.items():
            print(f"- {name}: {time}")

    def list_timers(self):
        """List all active timers"""
        print("Active Timers:")
        for name, duration in self.timers.items():
            print(f"- {name}: {duration} seconds")

def main():
    app = AlarmTimerApp()

    try:
        while True:
            print("\n--- Alarm and Timer Application ---")
            print("1. Set Alarm")
            print("2. Set Timer")
            print("3. Cancel Alarm")
            print("4. Cancel Timer")
            print("5. List Alarms")
            print("6. List Timers")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                name = input("Enter alarm name: ")
                time_str = input("Enter alarm time (HH:MM): ")
                app.set_alarm(name, time_str)

            elif choice == '2':
                name = input("Enter timer name: ")
                duration = int(input("Enter duration in seconds: "))
                app.set_timer(name, duration)

            elif choice == '3':
                name = input("Enter alarm name to cancel: ")
                app.cancel_alarm(name)

            elif choice == '4':
                name = input("Enter timer name to cancel: ")
                app.cancel_timer(name)

            elif choice == '5':
                app.list_alarms()

            elif choice == '6':
                app.list_timers()

            elif choice == '7':
                print("Exiting application...")
                break

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()