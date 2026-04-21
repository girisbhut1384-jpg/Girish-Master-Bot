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
import textwrap

from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 सिक्योरिटी दीवार हटाई जा रही है...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

print("📦 सिस्टम के अंदर फॉन्ट इंस्टॉल हो रहे हैं...")
os.system("sudo apt-get update -y")
os.system("sudo apt-get install -y fonts-indic fonts-noto-core")

sys_fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
hindi_fonts = [f for f in sys_fonts if "Devanagari" in f or "Samyak" in f or "Gargi" in f or "Nakula" in f]
FONT_PATH = hindi_fonts[0] if hindi_fonts else (sys_fonts[0] if sys_fonts else "Arial")

# 🔑 सारी चाबियां (Keys)
GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

if not GROQ_KEY:
    print("❌ एरर: GROQ_API_KEY नहीं मिली!")
    sys.exit(1)

# 🟢 एकदम असली बिकने वाले गैजेट्स और सबसे वायरल होने वाले रहस्य
GADGET_CATEGORIES = ["Trending Smart Home Gadgets", "Viral Car Accessories on Amazon", "Best Kitchen Tech Hacks", "Student Productivity Devices", "High-Tech Security Gadgets"]
MYSTIC_CATEGORIES = ["Most Viral Unsolved Mysteries", "Deep Ocean Terrifying Secrets", "Unexplained Ancient Civilizations", "Mind-Blowing Space Facts", "Creepiest Historical Events"]

def extract_json_safely(raw_text):
    raw_text = str(raw_text).strip()
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if match: return match.group(0)
    return "{}"

def get_script_and_prompts(category, is_gadget=False):
    print(f"\n✅ 70B AI इंजन दमदार टॉपिक सोच रहा है: {category}")
    
    prompt = f"""You are a master YouTube Shorts director known for high audience retention. 
    THEME: "{category}".
    
    CRITICAL INSTRUCTION: Create a highly viral and unique sub-topic! 

    REQUIREMENTS:
    1. SCRIPT (Voiceover): Write a highly engaging HINDI script (MINIMUM 60 WORDS). 
       - Start with a SHOCKING 3-second hook so the viewer stays till the end.
       - Build extreme suspense or show insane value.
    2. CAPTIONS (On-screen text): Write 8 punchy captions strictly in ENGLISH to grab attention.
    3. PROMPTS (English): 8 image generation prompts matching sentences.
    """

    if is_gadget:
        prompt += """
    - SCRIPT ENDING: The script MUST end EXACTLY with: 'यह शानदार गैजेट खरीदने का लिंक चैनल के बायो में है।'
    - IMAGE RULES: ONLY physical products currently existing on Amazon. NO HUMANS.
        """
    else:
        prompt += """
    - SCRIPT ENDING: The script MUST end EXACTLY with: 'ऐसी और रहस्यमयी चीज़ों के लिए लिंक बायो में है।'
    - IMAGE RULES: Hyper-realistic cinematic scenes. Creepy, mysterious, highly engaging. NO TEXT.
        """

    prompt += """
    Return ONLY valid JSON format exactly like this:
    {
      "topic": "your unique viral topic name",
      "script": "Hindi script here... (MUST BE AT LEAST 60 WORDS)",
      "captions": ["SHOCKING TRUTH!", "Amazing Fact", "Mind Blown", "Awesome", "Wait for it...", "Caption 6", "Caption 7", "Link in Bio!"],
      "prompts": ["Image 1 prompt", "Image 2 prompt", "Image 3 prompt", "Image 4 prompt", "Image 5 prompt", "Image 6 prompt", "Image 7 prompt", "Image 8 prompt"],
      "amazon_search_term": "Exact 2-3 word Amazon India search keyword for this product (Leave empty if mystery)"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a precise JSON generator. Output only JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5 
    }
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=50)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                clean_json = extract_json_safely(content)
                parsed_data = json.loads(clean_json)
                script = parsed_data.get('script', '')
                if script:
                    print(f"🎯 सफलता! वायरल टॉपिक मिला: {parsed_data.get('topic')}")
                    return script.replace("*", ""), parsed_data.get('prompts', [])[:8], parsed_data.get('captions', [])[:8], parsed_data.get('amazon_search_term', '')
        except Exception as e:
            print(f"⚠️ 70B एरर: {e}. फिर से कोशिश...")
            time.sleep(2)
    raise Exception("🚨 70B मॉडल फेल हो गया!")

# 🟢 सिर्फ गैजेट्स के लिए अमेज़न से असली फोटो निकालने वाला कोड (ताकि API लिमिट बचे)
def fetch_amazon_images(query, fallback_prompts):
    print(f"🛒 अमेज़न (India) से '{query}' की असली तस्वीरें खोजी जा रही हैं...")
    if not RAPIDAPI_KEY:
        print("⚠️ RAPIDAPI_KEY नहीं मिली! AI तस्वीरों का बैकअप ले रहे हैं...")
        return fetch_ai_images(fallback_prompts)

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {"query": query, "page": "1", "country": "IN", "sort_by": "RELEVANCE"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    image_files = []
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=40)
        if response.status_code == 200:
            products = response.json().get("data", {}).get("products", [])
            for i, prod in enumerate(products):
                if len(image_files) >= 8: break
                photo_url = prod.get("product_photo")
                if photo_url:
                    img_res = requests.get(photo_url, timeout=15)
                    if img_res.status_code == 200:
                        filename = f"amazon_img_{i}.jpg"
                        with open(filename, "wb") as f:
                            f.write(img_res.content)
                        image_files.append(filename)
            
            if len(image_files) >= 4:
                print(f"✅ अमेज़न से {len(image_files)} असली तस्वीरें 100% डाउनलोड हो गईं!")
                return image_files
            else:
                print("⚠️ अमेज़न पर प्रोडक्ट नहीं मिला। AI बैकअप इस्तेमाल हो रहा है...")
                return fetch_ai_images(fallback_prompts)
        else:
            print(f"⚠️ RapidAPI एरर: {response.status_code}. AI बैकअप इस्तेमाल हो रहा है...")
            return fetch_ai_images(fallback_prompts)
    except Exception as e:
        print(f"⚠️ अमेज़न API में दिक्कत: {e}. AI बैकअप इस्तेमाल हो रहा है...")
        return fetch_ai_images(fallback_prompts)

# 🟢 मिस्ट्री चैनल के लिए खूंखार AI फोटो (बिना API लिमिट खर्च किये)
def fetch_ai_images(prompts):
    print("🌌 AI से रहस्यमयी तस्वीरें जनरेट हो रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p + ", highly detailed, cinematic, 8k, textless, mind-bending")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        for attempt in range(3): 
            try:
                res = requests.get(url, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    image_files.append(filename)
                    break
            except: time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    print("✅ वॉइसओवर रिकॉर्ड हो रहा है...")
    async def _generate():
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("वॉइस सर्वर डाउन है।")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 कैप्शंस (Text) बिल्कुल बीच में, इंग्लिश में और पीले रंग में
def create_centered_text_clip(text, font_path, duration):
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(font_path, 80)
    except: font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text, width=22)
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except Exception:
        text_width, text_height = draw.textsize(wrapped_text, font=font)
        
    x = (canvas_w - text_width) // 2
    y = (canvas_h - text_height) // 2
    
    pad_x, pad_y = 40, 20
    draw.rectangle([x - pad_x, y - pad_y, x + text_width + pad_x, y + text_height + pad_y], fill=(0, 0, 0, 190))
    draw.multiline_text((x, y), wrapped_text, font=font, fill="yellow", align='center')
    
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ प्रोफेशनल वीडियो रेंडर हो रहा है...")
    if not image_files: raise Exception("तस्वीरें नहीं मिलीं!")
        
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        base_clip = ImageClip(img_path)
        w, h = base_clip.size
        
        # ब्लर बैकग्राउंड इफ़ेक्ट (जिससे अमेज़न की फोटो बहुत प्रोफेशनल दिखेगी)
        if w / h > 1080 / 1920: base_clip = base_clip.resize(height=1920)
        else: base_clip = base_clip.resize(width=1080)
            
        base_clip = base_clip.crop(x_center=base_clip.size[0]/2, y_center=base_clip.size[1]/2, width=1080, height=1920)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.05 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, FONT_PATH, time_per_image)
                txt_clip = txt_clip.set_position(('center', 'bottom')).margin(bottom=350, opacity=0)
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=(1080, 1920)).set_duration(time_per_image)
        else:
            final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=(1080, 1920)).set_duration(time_per_image)
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

def upload_video(token, filename, title, description, tags, category):
    print("✅ यूट्यूब पर अपलोड हो रहा है...")
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
    for attempt in range(3):
        try:
            if channel_type == "GADGETS":
                print(f"\n--- 📱 GADGETS चैनल प्रोसेसिंग ---")
                cat = random.choice(GADGET_CATEGORIES)
                script, prompts, captions, amazon_term = get_script_and_prompts(cat, is_gadget=True)
                
                # 🟢 यहाँ सिर्फ गैजेट्स के लिए API यूज़ होगी
                image_files = fetch_amazon_images(amazon_term, prompts) 
                
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 यह शानदार गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {amazon_term}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 Best {amazon_term} #shorts", desc, ["shorts", "gadgets", "amazon finds", "tech"], "28")
                print("✅ GADGETS वीडियो लाइव हो गया।")
                return True 
                
            elif channel_type == "MYSTIC":
                print(f"\n--- 🌌 MYSTIC चैनल प्रोसेसिंग ---")
                cat = random.choice(MYSTIC_CATEGORIES)
                script, prompts, captions, _ = get_script_and_prompts(cat, is_gadget=False)
                
                # 🟢 मिस्ट्री के लिए API इस्तेमाल नहीं होगी (लिमिट बचेगी), सिर्फ डरावनी AI फोटो बनेगी!
                image_files = fetch_ai_images(prompts)
                
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 रहस्यमयी किताबें और शानदार गैजेट्स खरीदने का लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 Unsolved Mystery Revealed #shorts", desc, ["shorts", "mystery", "facts", "creepy"], "28")
                print("✅ MYSTIC वीडियो लाइव हो गया।")
                return True 
                
        except Exception as e: 
            print(f"🛑 एरर: {e}. रीस्टार्ट हो रहा है...")
            time.sleep(15) 
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 मास्टर ब्रह्मास्त्र इंजन चालू हो गया है (स्मार्ट API सेवर मोड)...")
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")
    print("\n🎯 काम पूरा हुआ।")
