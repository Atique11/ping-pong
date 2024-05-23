# -*- coding: utf-8 -*-
"""
Created on Thu May 23 17:18:00 2024

@author: Atique
"""

import sys
import requests
import time

def start_game(pong_time_ms):
    requests.post("http://localhost:8000/start", json={"pong_time_ms": pong_time_ms, "ping_url": "http://localhost:8001/ping"})
    requests.post("http://localhost:8001/start", json={"pong_time_ms": pong_time_ms, "ping_url": "http://localhost:8000/ping"})

def pause_game():
    requests.post("http://localhost:8000/pause")
    requests.post("http://localhost:8001/pause")

def resume_game():
    requests.post("http://localhost:8000/resume")
    requests.post("http://localhost:8001/resume")

def stop_game():
    requests.post("http://localhost:8000/stop")
    requests.post("http://localhost:8001/stop")

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "start":
        pong_time_ms = int(sys.argv[2])
        start_game(pong_time_ms)
    elif command == "pause":
        pause_game()
    elif command == "resume":
        resume_game()
    elif command == "stop":
        stop_game()
    else:
        print("Unknown command")
