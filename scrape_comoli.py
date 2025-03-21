import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from linebot.v3.messaging import MessagingApi, ApiClient, Configuration
from linebot.v3.messaging import TextMessage, BroadcastRequest
import sys
import argparse

# Load environment variables
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
COMOLI_INFO_URL = 'https://www.comoli.jp/info'
STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'previous_content.json')

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
    print(f"Saving to file: {STORAGE_FILE}")
    print(f"Current working directory: {os.getcwd()}")
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"File saved successfully. File exists: {os.path.exists(STORAGE_FILE)}")

def send_line_notification(message):
    try:
        configuration = Configuration(
            access_token=LINE_CHANNEL_ACCESS_TOKEN
        )
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # Send broadcast message to all followers
            message = TextMessage(text=message)
            request = BroadcastRequest(
                messages=[message]
            )
            
            response = line_bot_api.broadcast(request)
            print("LINE notification broadcast successfully")
            return True
    except Exception as e:
        print(f"Error sending LINE notification: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='COMOLI Info Scraper')
        parser.add_argument('--test', action='store_true', help='Run in test mode (skip content comparison and storage)')
        args = parser.parse_args()

        # Scrape current content
        current_date, current_content = scrape_comoli_info()
        if not current_date:
            print("Failed to scrape date")
            return
        
        if not current_content:
            print("Failed to scrape content")
            return

        # Create notification message
        message = f"COMOLIの更新を検知しました！\n\n日付：{current_date}\n\n{current_content}\n\n{COMOLI_INFO_URL}"

        if args.test:
            # Test mode: Always send notification
            if send_line_notification(message):
                print("Test notification sent successfully")
            else:
                print("Failed to send LINE notification")
                sys.exit(1)
            return

        # Normal mode: Compare with previous content
        previous_data = load_previous_content()
        previous_date = previous_data.get('date', '')

        # Compare and notify if different
        if current_date != previous_date:
            if send_line_notification(message):
                print("Notification sent successfully")
                save_current_content(current_date, current_content)
            else:
                print("Failed to send LINE notification")
                sys.exit(1)  # エラーコード1で終了
        else:
            print("No updates found")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)  # エラーコード1で終了

if __name__ == '__main__':
    main() 