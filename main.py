import os, requests

def finalize_setup():
    # आपकी आईडी और सीक्रेट जो पहले से सेट है
    cid = "768932543756-30vbto7a15hqosjmpnbh99bfkbfbngj1.apps.googleusercontent.com"
    secret = "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"
    
    # यह लिंक आपको सीधा 'Allow' बटन पर ले जाएगा
    url = f"https://accounts.google.com/o/oauth2/auth?client_id={cid}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&response_type=code&access_type=offline&prompt=consent"
    
    print("--------------------------------------------------")
    print("गिरीश भाई, बस इस आखरी लिंक को खोलकर 'Allow' दबा दें:")
    print(url)
    print("--------------------------------------------------")
    
    # टेलीग्राम पर भी भेज रहा हूँ ताकि आपको आसानी रहे
    tg_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    requests.get(f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text=आखरी लिंक: {url}")

if __name__ == "__main__":
    finalize_setup()
