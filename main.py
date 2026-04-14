# गिरीश भाई का V5.7 मास्टर कोड (Hindi Font + No AI Gibberish + Mobile Safe Format)
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
    if is_gadget: 
        prompt += "End EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'. "
    else: 
        prompt += "End EXACTLY with: 'रहस्यमयी किताबें खरीदने का लिंक बायो में है।'. "
    
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
        except Exception: 
            pass
            
    # यहाँ पर कटी हुई लाइन को सुरक्षित किया गया है
    if not clean_text: 
        sys.exit(1)
        
    if clean_text.startswith("```json"): 
        clean_text = clean_text[7:-3].strip()
    elif clean_text.startswith("```"): 
        clean_text = clean_text[3:-3].strip()
         
    data = json.loads(clean_text)
    return data['script'].replace("*", ""), data['prompts'][:8], data['captions'][:8], data.get('gadget_name', '')

# 4. Pollinations AI (बिना टेक्स्ट वाली फोटो)
def fetch_ai_images(prompts):
    print("🎨 तस्वीरें बन रही हैं (No Text)...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p + ", highly detailed, cinematic, no text, no words, no letters, textless")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        for _ in range(3): 
            try:
                res = requests.get(url, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    image_files.append(filename)
                    break
            except Exception: 
                time.sleep(3)
    return image_files

# 5. आवाज़ 
def create_human_voice(text, filename):
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
        await communicate.save(filename)
    asyncio.run(_generate())

# 6. मास्टर एडिटिंग (100% परफेक्ट हिंदी सबटाइटल्स)
def make_video(image_files, captions, final_vid, audio_file):
    print("🎬 एडिटिंग (असली हिंदी टेक्स्ट के साथ)...")
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
        
        # 🛑 असली हिंदी फॉन्ट का इस्तेमाल
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

# 7. यूट्यूब अपलोड
def upload_video(token, filename, title, description, tags, category):
    credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )
    request.execute()

# 8. स्मार्ट रन
def run_channel_safely(channel_type):
    for attempt in range(3):
        try:
            if channel_type == "GADGETS":
                topic = random.choice(GADGET_TOPICS)
                script, prompts, captions, gadget_name = get_script_and_prompts(topic, is_gadget=True)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {gadget_name}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 {gadget_name} #shorts", desc, ["shorts", "gadgets"], "28")
                return True 
            elif channel_type == "MYSTIC":
                topic = random.choice(MYSTIC_TOPICS)
                script, prompts, captions, _ = get_script_and_prompts(topic, is_gadget=False)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 किताबें और गैजेट्स का लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 {topic} #shorts", desc, ["shorts", "mystery"], "28")
                return True 
        except Exception: 
            time.sleep(600)
    sys.exit(1)

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(60)
    run_channel_safely("MYSTIC")
