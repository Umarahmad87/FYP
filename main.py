from client import *
import signal
import sys
import threading

signal.signal(signal.SIGINT,signal_handler)
def main():
    program_start()

if __name__=="__main__":
    main()