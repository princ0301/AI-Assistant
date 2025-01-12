import datetime
import time
import threading
from playsound import playsound

class SystemAlarmTimer:
    def __init__(self):
        self.alarm_thread = None
        self.timer_thread = None
        self.alarm_active = False
        self.timer_active = False

    def set_alarm(self):
        try:
            alarm_time = input("Enter alarm time (HH:MM AM/PM): ").strip()
            alarm_datetime = datetime.datetime.strptime(alarm_time, '%I:%M %p').replace(
                year=datetime.datetime.now().year,
                month=datetime.datetime.now().month,
                day=datetime.datetime.now().day
            )

            if alarm_datetime < datetime.datetime.now():
                alarm_datetime += datetime.timedelta(days=1)

            time_to_wait = (alarm_datetime - datetime.datetime.now()).total_seconds()
            print(f"Alarm set for {alarm_time}. It will ring in {int(time_to_wait // 60)} minutes.")
            
            self.alarm_active = True

            def play_alarm():
                time.sleep(time_to_wait)
                if self.alarm_active:
                    print("Alarm ringing!")
                    sound_path = r"D:\Projects\Llama3-Voice-Assistant\AI Assistant\assistant\media\Warriyo - Mortals (feat. Laura Brehm) Future Trap NCS - Copyright Free Music.mp3"
                    playsound(sound_path)
                else:
                    print("Alarm canceled.")

            self.alarm_thread = threading.Thread(target=play_alarm, daemon=True)
            self.alarm_thread.start()

        except Exception as e:
            print(f"Error setting alarm: {str(e)}")

    def cancel_alarm(self):
        if self.alarm_active:
            self.alarm_active = False
            print("Alarm canceled successfully.")
        else:
            print("No active alarm to cancel.")

    def set_timer(self):
        try:
            duration_minutes = float(input("Enter timer duration in minutes: ").strip())
            seconds = int(duration_minutes * 60)
            print(f"Timer set for {duration_minutes} minutes.")

            self.timer_active = True

            def run_timer():
                time.sleep(seconds)
                if self.timer_active:
                    print("Timer finished!")
                    sound_path = r"D:\Projects\Llama3-Voice-Assistant\AI Assistant\assistant\media\Warriyo - Mortals (feat. Laura Brehm) Future Trap NCS - Copyright Free Music.mp3"
                    playsound(sound_path)
                else:
                    print("Timer canceled.")

            self.timer_thread = threading.Thread(target=run_timer, daemon=True)
            self.timer_thread.start()

        except Exception as e:
            print(f"Error setting timer: {str(e)}")

    def cancel_timer(self):
        if self.timer_active:
            self.timer_active = False
            print("Timer canceled successfully.")
        else:
            print("No active timer to cancel.")

def main():
    system = SystemAlarmTimer()
    while True:
        print("\nChoose an option:")
        print("1. Set Alarm")
        print("2. Set Timer")
        print("3. Cancel Alarm")
        print("4. Cancel Timer")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        if choice == '1':
            system.set_alarm()
        elif choice == '2':
            system.set_timer()
        elif choice == '3':
            system.cancel_alarm()
        elif choice == '4':
            system.cancel_timer()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
