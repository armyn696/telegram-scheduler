from fastapi import FastAPI, Request
import requests
import schedule
import time
import threading
from datetime import datetime

app = FastAPI()

# Telegram Bot Configuration
TELEGRAM_TOKEN = "7454317511:AAFrlEhKVRYWY4K2o09wXAGmS5kbxVnNUPI"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message_to_telegram(chat_id: str, message: str) -> dict:
    """Helper function to send message to Telegram"""
    url = f"{TELEGRAM_API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=data)
    return response.json()

@app.get("/")
async def root():
    return {"message": "Telegram Scheduler Bot is running!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    # Process incoming Telegram messages here
    return {"ok": True}

def schedule_message(chat_id: str, message: str, time: str) -> str:
    """Schedule a message to be sent at a specific time"""
    def job():
        send_message_to_telegram(chat_id, message)
    
    schedule.every().day.at(time).do(job)
    return f"Message scheduled for {time}"

# Start the scheduler in a background thread
scheduler_thread = threading.Thread(target=lambda: schedule.run_pending(), daemon=True)
scheduler_thread.start()
