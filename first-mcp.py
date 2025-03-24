from mcp.server.fastmcp import FastMCP
import requests
import schedule
import time
import threading
from datetime import datetime

# Create an MCP server
mcp = FastMCP("Telegram Bot Demo")

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

@mcp.tool()
def send_telegram_message(chat_id: str, message: str) -> str:
    """Send a message to Telegram chat immediately"""
    result = send_message_to_telegram(chat_id, message)
    return f"Message sent: {result}"

@mcp.tool()
def schedule_telegram_message(chat_id: str, message: str, send_time: str) -> str:
    """Schedule a message to be sent at a specific time
    send_time format should be HH:MM (24-hour format)"""
    try:
        # Parse the time
        hour, minute = map(int, send_time.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return "Invalid time format. Please use HH:MM in 24-hour format."

        # Schedule the message
        schedule.every().day.at(send_time).do(
            send_message_to_telegram,
            chat_id=chat_id,
            message=f"{message}\n\n⏰ Scheduled message sent at: {send_time}"
        )
        
        return f"Message scheduled to be sent at {send_time}"
    except Exception as e:
        return f"Error scheduling message: {str(e)}"

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
