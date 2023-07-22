import socket
from IPy import IP
import threading
import ctypes

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

ascii = """
   █████ ██▀███   ▄▄▄       ██████      ██████   ▄████▄  ▄▄▄      ███▄    █ 
 ▓██    ▓██ ▒ ██▒▒████▄   ▒██    ▒    ▒██    ▒  ▒██▀ ▀█ ▒████▄    ██ ▀█   █ 
 ▒████  ▓██ ░▄█ ▒▒██  ▀█▄ ░ ▓██▄      ░ ▓██▄    ▒▓█    ▄▒██  ▀█▄ ▓██  ▀█ ██▒
 ░▓█▒   ▒██▀▀█▄  ░██▄▄▄▄██  ▒   ██▒     ▒   ██▒▒▒▓▓▄ ▄██░██▄▄▄▄██▓██▒  ▐▌██▒
▒░▒█░   ░██▓ ▒██▒▒▓█   ▓██▒██████▒▒██ ▒██████▒▒░▒ ▓███▀ ▒▓█   ▓██▒██░   ▓██░
░ ▒ ░   ░ ▒▓ ░▒▓░░▒▒   ▓▒█▒ ▒▓▒ ▒ ░▒▒ ▒ ▒▓▒ ▒ ░░░ ░▒ ▒  ░▒▒   ▓▒█░ ▒░   ▒ ▒ 
░ ░       ░▒ ░ ▒ ░ ░   ▒▒ ░ ░▒  ░ ░░  ░ ░▒  ░     ░  ▒  ░ ░   ▒▒ ░ ░░   ░ ▒░
  ░ ░     ░░   ░   ░   ▒  ░  ░  ░  ░  ░  ░  ░   ░         ░   ▒     ░   ░ ░ 
░          ░           ░        ░   ░       ░   ░ ░           ░           ░ 
"""

def scan_ports(target_ip, min_port, max_port, progress_callback=None):
    open_ports = []
    total_ports = max_port - min_port + 1
    scanned_ports = 0

    for port in range(min_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target_ip, port))
                open_ports.append(port)
        except:
            pass

        scanned_ports += 1
        if progress_callback:
            progress = (scanned_ports / total_ports) * 100
            progress_callback(progress)

    return open_ports

def scan_ports_threaded(target_ip, min_port, max_port, num_threads=10, progress_callback=None):
    open_ports = []
    total_ports = max_port - min_port + 1
    ports_per_thread = total_ports // num_threads

    def scan_range(start_port, end_port):
        open_ports.extend(scan_ports(target_ip, start_port, end_port, progress_callback))

    threads = []
    for i in range(num_threads):
        start_port = min_port + i * ports_per_thread
        end_port = start_port + ports_per_thread - 1 if i < num_threads - 1 else max_port
        thread = threading.Thread(target=scan_range, args=(start_port, end_port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return open_ports
print(ascii)
def print_progress(progress):
    print(f"\rScanning ports... {progress:.2f}% completed.", end='', flush=True)

def main():
    target = input("IP: ")
    target_ip = IP(target)

    min_port = int(input("Min Port: "))
    max_port = None

    while max_port is None:
        max_port_input = input("Max Ports: ")
        try:
            max_port = int(max_port_input)
            if max_port <= min_port:
                print("Max port must be greater than min port.")
                max_port = None
        except ValueError:
            print("Invalid input. Please enter a valid integer for the max port.")
            max_port = None

    num_threads = int(input("Threads: "))

    open_ports = scan_ports_threaded(str(target_ip), min_port, max_port, num_threads, print_progress)

    if open_ports:
        print(f"\n\nThe following ports are open on {target_ip}:")
        print(open_ports)
    else:
        print("\n\nNo Ports Open")

if __name__ == "__main__":
    new_title = "PortScanner-Frasquito"
    set_console_title(new_title)
    main()
