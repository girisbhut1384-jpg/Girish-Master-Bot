import os
import requests

# गिरीश भाई, अब इसमें कोई टोकन नहीं है, यह पूरी तरह सुरक्षित है
def start_engine():
    try:
        # यहाँ जानकारी सीधे GitHub की 'तिजोरी' से आएगी
        tg_token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        amazon_id = os.getenv('AMAZON_ID')

        msg = f"🚀 गिरीश भाई, बधाई हो!\nमशीन अब पूरी तरह से सुरक्षित और ऑनलाइन है।"
        url = f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text={msg}"
        
        requests.get(url)
        print("Success: System Securely Started")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_engine()
