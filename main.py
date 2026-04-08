import os, json, requests, time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def main_engine():
    tg_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    client_secrets = json.loads(os.getenv('CLIENT_SECRETS_JSON'))

    # १. यूट्यूब की चाबी चेक करना
    scopes = ['https://www.googleapis.com/auth/youtube.upload']
    
    # गिरीश भाई, यहाँ हम चाबी मांगने का जुगाड़ कर रहे हैं
    flow = InstalledAppFlow.from_client_config(client_secrets, scopes=scopes)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob' # मोबाइल के लिए आसान तरीका

    auth_url, _ = flow.authorization_url(prompt='consent')

    # २. टेलीग्राम पर लिंक भेजना
    msg = f"🔑 **गिरीश भाई, आख़िरी ताला खोलें!**\n\n1. इस लिंक पर क्लिक करें: {auth_url}\n\n2. 'Allow' दबाने के बाद जो **Code** मिले, उसे यहाँ टेलीग्राम पर मुझे भेज दें।"
    requests.get(f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown")

if __name__ == "__main__":
    main_engine()
