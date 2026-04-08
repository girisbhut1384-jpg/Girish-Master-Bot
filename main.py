import os, requests

def start_engine():
    # गिरीश भाई, ये आपकी फिक्स आईडी और सीक्रेट है
    cid = "768932543756-30vbto7a15hqosjmpnbh99bfkbf8ngj1.apps.googleusercontent.com"
    
    # यह जादुई लिंक आपको सीधा यूट्यूब के 'Allow' बटन पर ले जाएगा
    auth_link = (
        f"https://accounts.google.com/o/oauth2/auth?client_id={cid}"
        "&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
        "&scope=https://www.googleapis.com/auth/youtube.upload"
        "&response_type=code&access_type=offline&prompt=consent"
    )
    
    tg_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    msg = f"🚀 **गिरीश भाई, बस ये आखिरी बटन दबाएँ:**\n\n1. यहाँ क्लिक करें: {auth_link}\n\n2. 'Allow' दबाने के बाद जो **Code** मिले, उसे यहाँ चैट में मुझे भेज दें।"
    
    requests.get(f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown")

if __name__ == "__main__":
    start_engine()
