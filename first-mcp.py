from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
import requests
import schedule
import time
import threading
from datetime import datetime
import uvicorn

app = FastAPI()
mcp = FastMCP("Telegram Scheduler")

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
    # اینجا پردازش پیام‌های تلگرام انجام میشه
    return {"ok": True}

@mcp.tool()
def send_telegram_message(chat_id: str, message: str) -> str:
    """Send a message to Telegram chat immediately"""
    result = send_message_to_telegram(chat_id, message)
    return f"Message sent: {result}"

@mcp.tool()
async def schedule_message(chat_id: str, message: str, time: str) -> str:
    """Schedule a message to be sent at a specific time"""
    # اینجا منطق زمانبندی پیام اضافه میشه
    return f"Message scheduled for {time}"

def run_scheduler():
    """Run the scheduler in background"""
    while True:
        schedule.run_pending()
        time.sleep(1)

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.prompt()
def telegram_prompt(message: str) -> str:
    """Create a Telegram message prompt"""
    return f"Please send this message: {message}"

if __name__ == "__main__":
    # Start the scheduler in a background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("MCP Server is ready!")
    print("You can test it with:")
    print("mcp dev first-mcp.py")
    print("\nScheduler is running in background...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
