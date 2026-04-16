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

from google import genai  
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.config import change_settings

# 1. इमेजमैजिक सिक्योरिटी दीवार हटाना
print("🔓 सिक्योरिटी दीवार हटाई जा रही है...")
os.system("sudo sed -i '/pattern=\"@\\*\"/d' /etc/ImageMagick-6/policy.xml")

# 2. लिनक्स के ऑफिशियल हिंदी फॉन्ट
print("📦 सिस्टम के अंदर ऑफिशियल हिंदी फॉन्ट इंस्टॉल हो रहे हैं...")
os.system("sudo apt-get update -y")
os.system("sudo apt-get install -y fonts-indic fonts-noto-core")

sys_fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
hindi_fonts = [f for f in sys_fonts if "Devanagari" in f or "Samyak" in f or "Gargi" in f or "Nakula" in f]
FONT_PATH = hindi_fonts[0] if hindi_fonts else (sys_fonts[0] if sys_fonts else "Arial")
print(f"✅ फॉन्ट मिल गया: {FONT_PATH}")

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    sys.exit(1)

client = genai.Client(api_key=GEMINI_KEY)
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

GADGET_TOPICS = ["स्मार्ट किचन हैक्स", "मच्छर भगाने वाला गैजेट", "स्मार्ट लाइट्स", "कार गैजेट", "स्टूडेंट गैजेट", "पोर्टेबल हीटर"]
MYSTIC_TOPICS = ["बरमूडा ट्राएंगल का सच", "पिरामिडों के नीचे क्या है?", "एलियंस के सबूत", "समुद्र का रहस्य", "समय यात्रा", "ब्लैक होल"]

# 3. डायरेक्ट बैकअप API
def get_fallback_script(prompt):
    print(f"   👉 बैकअप इंजन चालू कर रहा हूँ...")
    safe_prompt = prompt + "\n\nCRITICAL RULE: Return ONLY a valid JSON object starting with { and ending with }. NO markdown, NO reasoning tags, NO text outside the JSON."
    url = f"https://text.pollinations.ai/{urllib.parse.quote(safe_prompt)}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.text

# 4. पक्का JSON कटर
def extract_json_safely(raw_text):
    raw_text = str(raw_text).strip()
    
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0]
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0]

    match = re.search(r'\{[\s\S]*\}', raw_text)
    if match:
        return match.group(0)
    return raw_text

def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n✅ AI स्क्रिप्ट तैयार कर रहा है: {topic}")
    
    prompt = f"Write a VIRAL YouTube short script in Hindi about: {topic}. Start with a shocking hook. STRICTLY 50-60 words. "
    if is_gadget: 
        prompt += "End EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'. "
    else: 
        prompt += "End EXACTLY with: 'रहस्यमयी किताबें खरीदने का लिंक बायो में है।'. "
    
    prompt += """
    IMPORTANT: For the 'prompts' array, describe the scene. 
    Add exactly this to the end of EVERY image prompt: ", hyper-realistic, 8k resolution, shot on DSLR, lifelike photography, extreme detail, NO TEXT, textless, no words, no letters".
    Return ONLY JSON:
    {
      "script": "Hindi voiceover text...",
      "captions": ["शॉकिंग सच! 😲", "क्या आपको पता है?", "खतरनाक गैजेट 🔥", "लिंक बायो में है!", "कैप्शन 5", "कैप्शन 6", "कैप्शन 7", "कैप्शन 8"],
      "prompts": ["Image 1 prompt...", "Image 2 prompt...", "...", "...", "...", "...", "...", "..."],
      "gadget_name": "Amazon search name or empty."
    }
    """
    
    clean_text = None
    
    try:
        print("   👉 मेन इंजन ट्राई कर रहा हूँ: gemini-2.0-flash...")
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        if response.text:
            clean_text = response.text
            print("   ✅ मेन इंजन ने जवाब दिया।")
    except:
        pass
        
    if not clean_text:
        try:
            print("   👉 मेन इंजन फेल। दूसरा मेन इंजन ट्राई कर रहा हूँ: gemini-1.5-flash...")
            response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
            if response.text:
                clean_text = response.text
                print("   ✅ दूसरे मेन इंजन ने जवाब दिया।")
        except:
            pass

    if not clean_text:
        try:
            clean_text = get_fallback_script(prompt)
            if clean_text:
                print("   ✅ बैकअप इंजन ने जवाब दिया।")
        except Exception as e:
            raise Exception(f"इंटरनेट या बैकअप इंजन फेल: {e}")

    if not clean_text:
        raise Exception("सारे इंजन फेल हो गए।")

    clean_text = extract_json_safely(clean_text)

    try:
        data = json.loads(clean_text)
    except json.JSONDecodeError:
        raise Exception(f"AI का डाटा JSON नहीं है: {clean_text[:100]}...")

    script = data.get('script', data.get('Script', ''))
    if not script:
         raise Exception(f"'script' नहीं मिली! डाटा: {clean_text[:100]}...")

    return script.replace("*", ""), data.get('prompts', [])[:8], data.get('captions', [])[:8], data.get('gadget_name', '')

def fetch_ai_images(prompts):
    print("✅ हाई-क्वालिटी 8K तस्वीरें जनरेट हो रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        for _ in range(3): 
            try:
                res = requests.get(url, timeout=40) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    image_files.append(filename)
                    break
            except Exception: 
                time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    print("✅ वॉइसओवर रिकॉर्ड हो रहा है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
        await communicate.save(filename)
    asyncio.run(_generate())

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ वीडियो रेंडर हो रहा है...")
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
        
        txt_clip = TextClip(
            captions[i], 
            fontsize=85, 
            color='yellow', 
            bg_color='black', 
            font=FONT_PATH, 
            method='caption', 
            size=(900, None)
        )
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(time_per_image).margin(bottom=300, opacity=0)
        
        final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

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
    print("🚀 फाइनल इंजन चालू हो गया है...")
    run_channel_safely("GADGETS")
    print("\n⏳ ब्रेक...\n")
    time.sleep(30)
    run_channel_safely("MYSTIC")
    print("\n🎯 आज का काम पूरा हुआ।")
