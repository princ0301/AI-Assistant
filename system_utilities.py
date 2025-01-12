import os
import psutil
import platform
import socket
import requests

class SystemUtilities:
    @staticmethod
    def get_system_info(): 
        return {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Computer Name": platform.node(),
            "Processor": platform.processor(),
            "RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "IP Address": socket.gethostbyname(socket.gethostname())
        }

    @staticmethod
    def check_internet_connection(): 
        try:
            requests.get("http://www.google.com", timeout=3)
            return True
        except requests.ConnectionError:
            return False

    @staticmethod
    def get_battery_status(): 
        battery = psutil.sensors_battery()
        if battery:
            return {
                "Percent": battery.percent,
                "Plugged In": battery.power_plugged
            }
        return None

    @staticmethod
    def open_application(app_name): 
        try:
            if platform.system() == "Windows":
                os.startfile(app_name)
            elif platform.system() == "Darwin":  # macOS
                os.system(f"open {app_name}")
            else:  # Linux
                os.system(f"xdg-open {app_name}")
            return True
        except Exception as e:
            print(f"Error opening application: {e}")
            return False