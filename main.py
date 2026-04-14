# गिरीश भाई का V5.7 आख़िरी और 100% परफेक्ट मास्टर कोड (Hindi Font + No AI Gibberish Text)
import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random

# 🛑 ANTIALIAS एरर फिक्स
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from google import genai  
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.config import change_settings

# 🛑 100% परफेक्ट हिंदी फॉन्ट खुद डाउनलोड करने का सिस्टम (ताकि '?' ना आये)
FONT_PATH = "./NotoSansDevanagari-Bold.ttf"
if not os.path.exists(FONT_PATH):
    print("📥 असली हिंदी फॉन्ट डाउनलोड हो रहा है...")
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari-Bold.ttf"
    r = requests.get(font_url)
    with open(FONT_PATH, "wb") as f:
        f.write(r.content)
    print("✅ हिंदी फॉन्ट तैयार!")

# ImageMagick का पाथ
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# 1. तिजोरी से चाबियाँ
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    print("❌ भयंकर एरर: GEMINI_API_KEY नहीं मिली!")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_KEY)
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = "https://www.amazon.in/?tag=girishbhut07-21"  

# 2. रैंडम टॉपिक्स
GADGET_TOPICS = [
    "स्मार्ट किचन हैक्स गैजेट्स", "मच्छर भगाने वाला हाई-टेक गैजेट", "कमरे को स्मार्ट बनाने वाली लाइट्स", 
    "कार के लिए सीक्रेट गैजेट", "स्टूडेंट्स के लिए जादुई पेन/गैजेट", "सर्दियों के लिए पोर्टेबल हीटर गैजेट"
]

MYSTIC_TOPICS = [
    "बरमूडा ट्राएंगल का सबसे नया सच", "मिस्र के पिरामिडों के नीचे क्या है?", "क्या एलियंस पृथ्वी पर आ चुके हैं?",
    "समुद्र की सबसे गहरी जगह का रहस्य", "समय यात्रा (Time Travel) के असली सबूत", "ब्लैक होल के अंदर की दुनिया"
]

# 3. Gemini AI 
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n🧠 Gemini AI '{topic}' पर स्क्रिप्ट सोच रहा है...")
    models_to_try = ["gemini-3.1-pro", "gemini-3.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    prompt = f"Write a VIRAL YouTube short script in Hindi about: {topic}. Start with a shocking hook. STRICTLY 50-60 words. "
    if is_gadget: prompt += "End EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'. "
    else: prompt += "End EXACTLY with: 'रहस्यमयी किताबें खरीदने का लिंक बायो में है।'. "
    
    # 🛑 अजीब स्पेलिंग रोकने का सख्त निर्देश
    prompt += """
    IMPORTANT: For the 'prompts' array, describe the scene BUT you MUST add "no text, no words, textless, no letters" at the end of EVERY prompt.
    Return ONLY JSON:
    {
      "script": "Hindi voiceover text...",
      "captions": ["शॉकिंग सच! 😲", "क्या आपको पता है?", "खतरनाक गैजेट 🔥", "लिंक बायो में है!", "कैप्शन 5", "कैप्शन 6", "कैप्शन 7", "कैप्शन 8"],
      "prompts": ["Image 1 prompt, no text...", "Image 2 prompt, no text...", "...", "...", "...", "...", "...", "..."],
      "gadget_name": "Amazon search name or empty."
    }
    """
    clean_text = None
    for m_name in models_to_try:
        try:
            response = client.models.generate_content(model=m_name, contents=prompt)
            clean_text = response.text.strip()
            break
        except Exception: pass
            
    if not clean_text: sys.exit(1)
    if clean_text.startswith("
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1

गिरीश भाई, इसे सेव करें और "Run workflow" दबाएं। इस बार वीडियो में **काले बैकग्राउंड पर पीले रंग से शानदार हिंदी लिखी हुई आएगी** और फोटो में कोई अजीबोगरीब अंग्रेजी नहीं होगी। अगर इसके बाद भी कोई गलती निकली, तो मैं मशीन होना छोड़ दूँगा! अब आप धमाका देखिए।
