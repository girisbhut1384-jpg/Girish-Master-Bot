# गिरीश भाई का V5.3 हाई-प्रोफाइल मास्टर कोड (All Gemini Models Combined Fallback)
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

# ImageMagick का पाथ सेट करें
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# 1. तिजोरी से चाबियाँ
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = "https://www.amazon.in/?tag=girishbhut07-21"  

# 2. रैंडम टॉपिक्स की ब्रेन डिक्शनरी 
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

# 3. Gemini AI - (सारे मॉडल्स एक साथ जोड़े गए - ब्रह्मास्त्र लूप)
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n🧠 Gemini AI '{topic}' पर वायरल स्क्रिप्ट सोच रहा है...")
    
    # 🛑 V5.3 मास्टरमाइंड आइडिया: सारे मॉडल्स की लिस्ट (एक फेल तो दूसरा चालू)
    models_to_try = [
        "models/gemini-1.5-flash",
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-pro",
        "models/gemini-1.5-pro-latest",
        "models/gemini-pro"
    ]
    
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
    response_data = None
    
    # एक-एक करके सारे मॉडल्स को आज़माएगा
    for model in models_to_try:
        print(f"🤖 मशीन ट्राई कर रही है: {model}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={GEMINI_KEY}"
        try:
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                temp_data = res.json()
                if 'candidates' in temp_data:
                    response_data = temp_data
                    print(f"✅ सफलता! {model} ने स्क्रिप्ट बना दी।")
                    break # काम हो गया, लूप से बाहर आओ
            else:
                print(f"⚠️ {model} ने मना कर दिया (Error {res.status_code}). अगले मॉडल पर जा रहे हैं...")
        except Exception as e:
            print(f"⚠️ {model} डाउन है ({e}). अगले मॉडल पर जा रहे हैं...")
            
    if not response_data:
        raise Exception("❌ सारे Gemini मॉडल्स फेल हो गए! गूगल का सर्वर पूरी तरह डाउन है।")
    
    clean_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:-3].strip()
    elif clean_text.startswith("```"):
        clean_text = clean_text[3:-3].strip()
         
    data = json.loads(clean_text)
    hindi_script = data['script'].replace("*", "").replace("#", "")
    print(f"✅ [AI स्क्रिप्ट तैयार]: {hindi_script[:60]}...")
    return hindi_script, data['prompts'][:8], data['captions'][:8], data.get('gadget_name', '')

# 4. Pollinations AI 
def fetch_ai_images(prompts):
    print("🎨 8 हाई-क्वालिटी तस्वीरें बनाई जा रही हैं (Fast Cuts के लिए)...")
    image_files = []
    seed = random.randint(1000, 99999) 
    
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p + ", highly detailed, 4k, cinematic")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        
        for attempt in range(3): # फोटो के लिए भी ट्राई-अगेन
            try:
                res = requests.get(url, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: f.write(res.content)
                    image_files.append(filename)
                    print(f"   ✅ फोटो {i+1}/8 तैयार!")
                    break
            except Exception:
                time.sleep(3)
    
    if len(image_files) < 8:
        raise Exception("❌ फोटो बनाने वाला सर्वर डाउन है।")
    return image_files

# 5. असली इंसानों जैसी आवाज़ 
def create_human_voice(text, filename):
    print("🎙️ आवाज़ बनाई जा रही है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
        await communicate.save(filename)
    asyncio.run(_generate())

# 6. मास्टर एडिटिंग
def make_video(image_files, captions, final_vid, audio_file):
    print("🎬 प्रो-लेवल एडिटिंग (Fast Cuts + Text Subtitles)...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    
    clips = []
    for i, img in enumerate(image_files):
        base_clip = ImageClip(img)
        w, h = base_clip.size
        if w / h > 1080 / 1920: 
            base_clip = base_clip.resize(height=1920)
        else: 
            base_clip = base_clip.resize(width=1080)
        base_clip = base_clip.crop(x_center=base_clip.size[0]/2, y_center=base_clip.size[1]/2, width=1080, height=1920)
        
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.05 * (t / time_per_image)).set_duration(time_per_image)
        
        txt_clip = TextClip(captions[i], fontsize=80, color='white', bg_color='black', font='Arial-Bold', method='caption', size=(900, None))
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(time_per_image).margin(bottom=300, opacity=0)
        
        final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

# 7. यूट्यूब अपलोड
def upload_video(token, filename, title, description, tags, category):
    print(f"🚀 यूट्यूब पर वीडियो अपलोड हो रहा है...")
    credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "tags": tags, "categoryId": category},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"✅ वीडियो लाइव है: https://www.youtube.com/watch?v={response['id']}\n")

# 8. स्मार्ट 'जिद्दी' एग्जीक्यूशन इंजन 
def run_channel_safely(channel_type):
    max_retries = 3
    wait_minutes = 10
    
    for attempt in range(max_retries):
        try:
            if channel_type == "GADGETS":
                print("--- 📱 Girish AI Gadgets ---")
                topic = random.choice(GADGET_TOPICS)
                script, prompts, captions, gadget_name = get_script_and_prompts(topic, is_gadget=True)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                
                desc = f"🔥 👉 गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {gadget_name}\n\n{script}\n\n#gadgets #smarthome #amazonfinds"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 {gadget_name} #shorts", desc, ["shorts", "gadgets", "amazon finds"], "28")
                return True 
                
            elif channel_type == "MYSTIC":
                print("--- 🌌 Mystic Universe ---")
                topic = random.choice(MYSTIC_TOPICS)
                script, prompts, captions, _ = get_script_and_prompts(topic, is_gadget=False)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                
                desc = f"🔥 👉 रहस्यमयी किताबें और गैजेट्स का लिंक चैनल के Bio में है!\n\n{script}\n\n#space #universe #mystery #shorts"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 {topic} #shorts", desc, ["shorts", "space", "mystery"], "28")
                return True 
                
        except Exception as e:
            print(f"⚠️ एरर आया: {e}")
            print(f"⏳ फेल नहीं हो रहा हूँ, {wait_minutes} मिनट बाद दोबारा कोशिश करूँगा... (Attempt {attempt+1}/{max_retries})")
            time.sleep(wait_minutes * 60)
            
    print(f"❌ 3 बार कोशिश की पर सर्वर नहीं चला। अब बंद हो रहा हूँ।")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 V5.3 हाई-प्रोफाइल जिद्दी AI इंजन स्टार्ट...")
    run_channel_safely("GADGETS")
    print("\n⏳ 60 सेकंड का ब्रेक...\n")
    time.sleep(60)
    run_channel_safely("MYSTIC")
    print("🎯 दोनों चैनलों का काम शानदार तरीके से पूरा हो गया!")
