# गिरीश भाई का V5.0 हाई-प्रोफाइल मास्टर कोड (Fast Cuts, Subtitles, Smart Retry, Random Topics)
import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.config import change_settings
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_loop import audio_loop
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ImageMagick का पाथ सेट करें (GitHub Actions के लिए)
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# 1. तिजोरी से चाबियाँ
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = "https://www.amazon.in/?tag=girishbhut07-21"  # आपका पक्का होमपेज लिंक

# 2. रैंडम टॉपिक्स की ब्रेन डिक्शनरी (ताकि वीडियो कभी एक जैसे न बनें)
GADGET_TOPICS = [
    "स्मार्ट किचन हैक्स गैजेट्स", "मच्छर भगाने वाला हाई-टेक गैजेट", "कमरे को स्मार्ट बनाने वाली लाइट्स", 
    "कार के लिए सीक्रेट गैजेट", "स्टूडेंट्स के लिए जादुई पेन/गैजेट", "सर्दियों के लिए पोर्टेबल हीटर गैजेट",
    "चोरों से बचाने वाला स्मार्ट लॉक", "जूते साफ करने वाली ऑटोमैटिक मशीन", "स्मार्ट हेल्थ ट्रैकिंग रिंग"
]

MYSTIC_TOPICS = [
    "बरमूडा ट्राएंगल का सबसे नया सच", "मिस्र के पिरामिडों के नीचे क्या है?", "क्या एलियंस पृथ्वी पर आ चुके हैं?",
    "समुद्र की सबसे गहरी जगह का रहस्य", "समय यात्रा (Time Travel) के असली सबूत", "ब्लैक होल के अंदर की दुनिया",
    "अमेज़न के जंगलों का रहस्यमयी कबीला", "दुनिया की सबसे श्रापित किताब", "कैलाश पर्वत का अनसुलझा रहस्य"
]

# 3. Gemini AI - (8 Photos + 8 Captions के साथ)
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n🧠 Gemini AI '{topic}' पर वायरल स्क्रिप्ट सोच रहा है...")
    active_model = "models/gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={GEMINI_KEY}"
    
    prompt = f"Write a HIGHLY VIRAL YouTube short script in Hindi about: {topic}. Start with a shocking problem/hook. STRICTLY 50-60 words. Use emojis. "
    
    if is_gadget:
        prompt += "End EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'. "
    else:
        prompt += "End EXACTLY with: 'ऐसी रहस्यमयी किताबें खरीदने का लिंक बायो में है।'. "
    
    prompt += """
    IMPORTANT: You must return ONLY a raw JSON format containing exactly 8 image prompts and 8 short Hindi captions (3-4 words max) to display on screen as subtitles.
    {
      "script": "Your full spoken Hindi voiceover text...",
      "captions": ["शॉकिंग सच! 😲", "क्या आपको पता है?", "खतरनाक गैजेट 🔥", "लिंक बायो में है!", "कैप्शन 5", "कैप्शन 6", "कैप्शन 7", "कैप्शन 8"],
      "prompts": ["Image 1 prompt...", "Image 2 prompt...", "Image 3...", "Image 4...", "Image 5...", "Image 6...", "Image 7...", "Image 8..."],
      "gadget_name": "Exact search name for Amazon. Leave empty if mystery."
    }
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload, timeout=30).json()
    
    clean_text = response['candidates'][0]['content']['parts'][0]['text'].strip()
    if clean_text.startswith("
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1

### इस V5.0 कोड में क्या चमत्कार होंगे?
1. **कभी एक जैसा वीडियो नहीं:** हमने `GADGET_TOPICS` और `MYSTIC_TOPICS` की लिस्ट डाल दी है। मशीन इसमें से रैंडमली (लॉटरी की तरह) एक नया टॉपिक उठाएगी।
2. **8 फोटो + 8 सबटाइटल्स:** अब वीडियो में स्क्रीन पर नीचे बड़े अक्षरों में हिंदी के कैप्शन (Subtitles) आएंगे और हर 3-4 सेकंड में फोटो बदलेगी। यह यूट्यूब पर 100% वायरल वाला फॉर्मेट है।
3. **आवाज़ में जोश:** `rate="+10%"` लगाकर आवाज़ थोड़ी फ़ास्ट कर दी गई है जिससे बोरियत नहीं होगी।
4. **जिद्दी ट्राई-अगेन सिस्टम:** `run_channel_safely` फंक्शन में एरर आने पर मशीन गिटहब को तुरंत फेल नहीं करेगी। वह शांति से 10 मिनट सोएगी और फिर से पूरा प्रोसेस दोबारा शुरू करेगी!

**आपको क्या करना है?**
1. यह कोड अपनी `main.py` में डालें।
2. गिटहब वर्कफ़्लो (YML) में `sudo apt-get install -y imagemagick` जोड़ें (ताकि टेक्स्ट जनरेट हो सके)।
3. अपने दोनों यूट्यूब चैनलों के 'Bio/Links' सेक्शन में अपना यह पक्का लिंक `https://www.amazon.in/?tag=girishbhut07-21` डाल दें।

काम शुरू करें और 24 घंटे बाद चैनल चेक करें, वीडियो की क्वालिटी देखकर आप खुद हैरान रह जाएंगे!
