import socket
import threading
from queue import Queue

open_ports = []  # list for open ports
queue = Queue()  # empty queue

target = ''  # IP address to scan

# This function creates a socket and attempts to connect with given port and IP
# Connection is only sucessful if the port is open
# returns true or false


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

# This function fills the queue with ports given the port list


def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


# This function iterates through the queue until its empty
# If the port is open it prints the port


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("port {} is open".format(port))
            open_ports.append(port)


port_list = range(1, 500)  # Range of the ports to check
fill_queue(port_list)  # Call fill queue function passing in the list of ports

thread_list = []   # Create empty list of thread

for t in range(100):  # Create 10 threads
    thread = threading.Thread(target=worker)  # instantiate the thread class with target worker
    thread_list.append(thread)  # add thread to list

for thread in thread_list:  # start thread
    thread.start()

for thread in thread_list:  # wait for the threads to finish before printing the list of open ports
    thread.join()

print("Open ports are ", open_ports)
