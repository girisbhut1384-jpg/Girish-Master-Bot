import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
import glob
import re

import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.config import change_settings

# 1. सिक्योरिटी दीवार हटाना
print("🔓 सिक्योरिटी दीवार हटाई जा रही है...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 2. हिंदी फॉन्ट इंस्टॉल करना
print("📦 सिस्टम के अंदर ऑफिशियल हिंदी फॉन्ट इंस्टॉल हो रहे हैं...")
os.system("sudo apt-get update -y")
os.system("sudo apt-get install -y fonts-indic fonts-noto-core")

sys_fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
hindi_fonts = [f for f in sys_fonts if "Devanagari" in f or "Samyak" in f or "Gargi" in f or "Nakula" in f]
FONT_PATH = hindi_fonts[0] if hindi_fonts else (sys_fonts[0] if sys_fonts else "Arial")

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# 🛑 Groq की चाबी चेक करना
GROQ_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_KEY:
    print("❌ एरर: GROQ_API_KEY गिटहब सीक्रेट्स में नहीं मिली!")
    sys.exit(1)

CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

GADGET_TOPICS = ["स्मार्ट किचन हैक्स", "मच्छर भगाने वाला गैजेट", "स्मार्ट लाइट्स", "कार गैजेट", "स्टूडेंट गैजेट", "पोर्टेबल हीटर"]
MYSTIC_TOPICS = ["बरमूडा ट्राएंगल का सच", "पिरामिडों के नीचे क्या है?", "एलियंस के सबूत", "समुद्र का रहस्य", "समय यात्रा", "ब्लैक होल"]

# 🌟 सुपर JSON कटर
def extract_json_safely(raw_text):
    raw_text = str(raw_text).strip()
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if match:
        return match.group(0)
    return "{}"

# 3. 🛡️ ऑटोमैटिक मॉडल चेंज इंजन (नए Llama 3.1 और 3.2 के साथ)
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n✅ Groq AI स्क्रिप्ट तैयार कर रहा है: {topic}")
    
    prompt = f"Write a VIRAL YouTube short script in Hindi about: {topic}. Start with a shocking hook. STRICTLY 50-60 words. "
    if is_gadget: 
        prompt += "End EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'. "
    else: 
        prompt += "End EXACTLY with: 'रहस्यमयी किताबें खरीदने का लिंक बायो में है।'. "
    
    prompt += """
    IMPORTANT: For the 'prompts' array, describe the scene for AI image generation. 
    Add exactly this to the end of EVERY image prompt: ", hyper-realistic, 8k resolution, shot on DSLR, lifelike photography, extreme detail, NO TEXT, textless, no words, no letters".
    
    Return ONLY valid JSON format exactly like this:
    {
      "topic": "topic name",
      "script": "Hindi voiceover text here...",
      "captions": ["caption 1", "caption 2", "caption 3", "caption 4", "caption 5", "caption 6", "caption 7", "caption 8"],
      "prompts": ["Image 1 prompt", "Image 2 prompt", "Image 3 prompt", "Image 4 prompt", "Image 5 prompt", "Image 6 prompt", "Image 7 prompt", "Image 8 prompt"],
      "gadget_name": "Amazon search name or empty"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    # 🟢 दुनिया के सबसे नए और 100% चालू मॉडल्स की लिस्ट
    models_to_try = [
        "llama-3.1-8b-instant", 
        "llama-3.1-70b-versatile", 
        "llama-3.2-3b-preview", 
        "gemma2-9b-it"
    ]
    
    for model_name in models_to_try:
        print(f"🔄 ट्राइंग मॉडल: {model_name}...")
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a JSON generator. Never add conversational text."},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=40)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                clean_json = extract_json_safely(content)
                parsed_data = json.loads(clean_json)
                
                script = parsed_data.get('script', '')
                if script and len(parsed_data.get('prompts', [])) >= 4:
                    print(f"🎯 सफलता! {model_name} ने सही स्क्रिप्ट दी।")
                    return script.replace("*", ""), parsed_data.get('prompts', [])[:8], parsed_data.get('captions', [])[:8], parsed_data.get('gadget_name', '')
            else:
                # 🛑 अब मशीन बताएगी कि Groq ने 400 एरर क्यों दिया!
                print(f"⚠️ {model_name} फेल हुआ (Status: {response.status_code}). कारण: {response.text[:150]}")
        except Exception as e:
            print(f"⚠️ {model_name} में इंटरनेट एरर आया: {e}. अगला ट्राई कर रहे हैं...")
            time.sleep(2)
            
    raise Exception("🚨 सभी AI मॉडल्स फेल हो गए! कृपया बाद में कोशिश करें।")

# 4. 🛡️ तस्वीरें बनाना
def fetch_ai_images(prompts):
    print("✅ हाई-क्वालिटी 8K तस्वीरें जनरेट हो रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        
        success = False
        for attempt in range(3): 
            try:
                res = requests.get(url, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    image_files.append(filename)
                    success = True
                    break
            except Exception: 
                time.sleep(3)
        if not success:
            print(f"⚠️ तस्वीर {i} जनरेट नहीं हो पाई, स्किप कर रहे हैं।")
    return image_files

# 5. 🛡️ आवाज़ बनाना
def create_human_voice(text, filename):
    print("✅ वॉइसओवर रिकॉर्ड हो रहा है...")
    async def _generate():
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
                await communicate.save(filename)
                return True
            except Exception as e:
                print(f"⚠️ वॉइस एरर: {e}. 5 सेकंड बाद फिर कोशिश कर रहे हैं...")
                await asyncio.sleep(5)
        raise Exception("वॉइस सर्वर डाउन है।")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 6. वीडियो बनाना
def make_video(image_files, captions, final_vid, audio_file):
    print("✅ वीडियो रेंडर हो रहा है...")
    if not image_files or len(image_files) == 0:
        raise Exception("एक भी तस्वीर जनरेट नहीं हुई! वीडियो नहीं बन सकता।")
        
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    
    if audio_duration <= 0:
        raise Exception("ऑडियो फाइल करप्ट है या उसकी लंबाई 0 है।")
        
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
        
        cap_text = captions[i] if i < len(captions) else ""
        txt_clip = TextClip(cap_text, fontsize=85, color='yellow', bg_color='black', font=FONT_PATH, method='caption', size=(900, None))
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
    print("✅ यूट्यूब पर वीडियो अपलोड किया जा रहा है...")
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )
    request.execute()

# 8. सेफ रनर
def run_channel_safely(channel_type):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            if channel_type == "GADGETS":
                print(f"\n--- 📱 GADGETS चैनल प्रोसेसिंग ---")
                topic = random.choice(GADGET_TOPICS)
                script, prompts, captions, gadget_name = get_script_and_prompts(topic, is_gadget=True)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {gadget_name}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 {gadget_name} #shorts", desc, ["shorts", "gadgets", "amazon finds"], "28")
                print("✅ GADGETS चैनल पर वीडियो लाइव हो गया।")
                return True 
                
            elif channel_type == "MYSTIC":
                print(f"\n--- 🌌 MYSTIC चैनल प्रोसेसिंग ---")
                topic = random.choice(MYSTIC_TOPICS)
                script, prompts, captions, _ = get_script_and_prompts(topic, is_gadget=False)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 रहस्यमयी किताबें और गैजेट्स का लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 {topic} #shorts", desc, ["shorts", "mystery", "facts"], "28")
                print("✅ MYSTIC चैनल पर वीडियो लाइव हो गया।")
                return True 
                
        except Exception as e: 
            print(f"🛑 एरर: {e}")
            print(f"⚠️ सिस्टम रीस्टार्ट हो रहा है... (Attempt {attempt+1}/{max_attempts})")
            time.sleep(15) 
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 मास्टर बुलेटप्रूफ इंजन 2.0 चालू हो गया है...")
    run_channel_safely("GADGETS")
    print("\n⏳ ब्रेक...\n")
    time.sleep(30)
    run_channel_safely("MYSTIC")
    print("\n🎯 आज का काम पूरा हुआ।")
