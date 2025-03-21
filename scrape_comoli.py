import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_USER_ID = os.getenv('LINE_USER_ID')
COMOLI_INFO_URL = 'https://www.comoli.jp/info'
STORAGE_FILE = 'previous_content.json'

def scrape_comoli_info():
    """Scrape COMOLI info page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(COMOLI_INFO_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the latest date from time tag
    latest_date = soup.find('time')
    if not latest_date:
        return None, None
    
    date_text = latest_date.get_text(strip=True)
    
    # Extract the content from the div following the time tag
    content_div = latest_date.find_next('div')
    if not content_div:
        return date_text, None
    
    content_text = content_div.get_text(strip=True)
    return date_text, content_text

def load_previous_content():
    """Load previous content from storage"""
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'date': '', 'content': '', 'last_updated': ''}

def save_current_content(date, content):
    """Save current content to storage"""
    data = {
        'date': date,
        'content': content,
        'last_updated': datetime.now().isoformat()
    }
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_line_notification(date, content):
    """Send notification via LINE"""
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    try:
        message = f"COMOLIの更新を検知しました！\n\n日付：{date}\n\n{content}\n\n{COMOLI_INFO_URL}"
        line_bot_api.push_message(
            LINE_USER_ID,
            TextSendMessage(text=message)
        )
        return True
    except Exception as e:
        print(f"Error sending LINE notification: {e}")
        return False

def main():
    # Scrape current content
    current_date, current_content = scrape_comoli_info()
    if not current_date:
        print("Failed to scrape date")
        return
    
    if not current_content:
        print("Failed to scrape content")
        return

    # Load previous content
    previous_data = load_previous_content()
    previous_date = previous_data.get('date', '')

    # Compare and notify if different
    if current_date != previous_date:
        if send_line_notification(current_date, current_content):
            print("Notification sent successfully")
            save_current_content(current_date, current_content)
        else:
            print("Failed to send notification")
    else:
        print("No updates found")

if __name__ == '__main__':
    main() 