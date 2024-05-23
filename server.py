# -*- coding: utf-8 -*-
"""
Created on Thu May 23 17:10:30 2024

@author: Atique
"""
from fastapi import FastAPI, BackgroundTasks, HTTPException
import httpx  # Library for HTTP requests
import asyncio  # Library for asynchronous programming


app = FastAPI()
ping_url = None
pong_time_ms = None
is_paused = False
task = None

@app.get("/ping")
async def ping():
    global is_paused
    if is_paused:
        return {"status": "paused"}
    return {"response": "pong"}

@app.post("/start")
async def start(pong_time_ms: int, ping_url: str):
    global task, is_paused
    set_pong_time_ms(pong_time_ms)
    set_ping_url(ping_url)
    is_paused = False
    if task:
        task.cancel()
    task = asyncio.create_task(ping_pong_task())

@app.post("/pause")
async def pause():
    set_pause_status(True)

@app.post("/resume")
async def resume():
    set_pause_status(False)

@app.post("/stop")
async def stop():
    global task
    if task:
        task.cancel()
    task = None

async def ping_pong_task():
    while True:
        if not is_paused:
            async with httpx.AsyncClient() as client:
                await client.get(ping_url)
            await asyncio.sleep(pong_time_ms / 1000)

def set_ping_url(url):
    global ping_url
    ping_url = url

def set_pong_time_ms(time):
    global pong_time_ms
    pong_time_ms = time

def set_pause_status(status):
    global is_paused
    is_paused = status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    

