import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 🟢 PIL Resampling Fix
if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 Security aur Premium Setup chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 🟢 Font Downloader
if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

# Config & Secrets
GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
TELEGRAM_TOKEN = "8382528984:AAHLJYwQIvLN5xEHV9iSjvgI18b8pF4bWJ8"
CHAT_ID = "8285187691"

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

# 🟢 अपडेट 1: डायनामिक रैंडम टॉपिक्स
GADGET_HOOKS = ["Amazon's Hidden Tech", "Crazy Gadgets Under 1000", "Must-Have Smart Home Items", "Secret Car Hacks", "Genius Kitchen Tools", "Future Tech 2026", "Mind-Blowing Survival Gear"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Deep Sea Monsters", "Unsolved Crimes of History", "Lost Ancient Cities", "Creepy Government Secrets", "Parallel Universe Proof", "Forbidden Knowledge"]

def send_telegram(msg):
    try: requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    except: pass

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, is_gadget=False, is_long=False):
    # 🟢 अपडेट 2: 30-सेकंड बनाम लॉन्ग वीडियो लॉजिक
    words = "550 words (Detailed Story)" if is_long else "75 words (Strict 30 Seconds)"
    print(f"\n✅ AI Engine {words} ki script likh raha hai: {hook_theme}")
    
    if is_gadget:
        prompt = f"""You are a top Amazon affiliate marketer. THEME: "{hook_theme}". WRITE A {words} HINDI SCRIPT.
        RULES: Start with a SHOCKING hook. Describe a problem. Product is the solution. High urgency.
        END EXACTLY: 'यह शानदार गैजेट अभी आउट ऑफ़ स्टॉक होने से पहले चैनल के बायो से खरीदें।'"""
    else:
        prompt = f"""You are a dark, mysterious storyteller. THEME: "{hook_theme}". WRITE A {words} HINDI SCRIPT.
        RULES: Build suspense and mystery. Reveal shocking facts.
        END EXACTLY: 'ऐसे ही खूंखार रहस्यों के लिए चैनल को सब्सक्राइब करें और लिंक बायो में देखें।'"""

    prompt += f"""\nReturn ONLY valid JSON:
    {{ "topic": "viral name", "script": "Hindi script...", "captions": ["8-short-lines"], "prompts": ["8-visual-prompts"], "amazon_search_term": "Product name", "score": 95 }}"""
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_search_term', ''), parsed.get('score', 90)
        except: time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

def fetch_amazon_images_strict(query):
    print(f"🛒 Amazon photo search: {query}")
    if not RAPIDAPI_KEY: raise Exception("⚠️ RAPIDAPI_KEY Missing!")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": query, "page": "1", "country": "IN", "sort_by": "RELEVANCE"}, timeout=40)
        if response.status_code == 200:
            for i, prod in enumerate(response.json().get("data", {}).get("products", [])):
                if len(image_files) >= 8: break
                photo_url = prod.get("product_photo")
                if photo_url:
                    img_res = requests.get(photo_url, timeout=15)
                    if img_res.status_code == 200:
                        fname = f"amazon_img_{i}.jpg"
                        with open(fname, "wb") as f: f.write(img_res.content)
                        image_files.append(fname)
            if len(image_files) >= 4: return image_files
        return fetch_ai_images([query]*8)
    except: return fetch_ai_images([query]*8)

def fetch_ai_images(prompts):
    print("🎨 Generating AI Scenes...")
    image_files, seed = [], random.randint(1000, 99999)
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + ', highly detailed, 8k')}?width=1080&height=1920&nologo=true&seed={seed+i}"
        fname = f"ai_scene_{i}.jpg"
        for _ in range(3): 
            try:
                res = requests.get(url, headers=headers, timeout=30) 
                if res.status_code == 200: 
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    break
            except: time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def create_centered_text_clip(text, duration):
    # 🟢 अपडेट 3: वायरल UI (बड़ा पीला टेक्स्ट + काला गहरा स्ट्रोक)
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("Roboto-Black.ttf", 145)
    except: font = ImageFont.load_default()
    wrapped = textwrap.fill(text.upper(), width=12)
    draw.multiline_text((540, 200), wrapped, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", anchor="mm", align='center')
    temp_filename = f"cap_{random.randint(1000, 9999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def process_image_for_video(img_path, output_path):
    img = Image.open(img_path).convert("RGB")
    bg = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=40))
    ratio = 1080 / img.width
    new_h = int(img.height * ratio)
    fg = img.resize((1080, new_h), Image.Resampling.LANCZOS)
    bg.paste(fg, (0, (1920 - new_h) // 2))
    bg.save(output_path)
    return output_path

def make_video(image_files, captions, final_vid, audio_file):
    print("🎬 Rendering Professional Video...")
    main_audio = AudioFileClip(audio_file)
    dur_per_image = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        fixed = f"fixed_{i}.jpg"
        process_image_for_video(img_path, fixed)
        base = ImageClip(fixed).set_duration(dur_per_image).resize(lambda t: 1 + 0.05 * (t / dur_per_image))
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            txt = create_centered_text_clip(cap_text, dur_per_image).set_position(('center', 0.65), relative=True)
            clips.append(CompositeVideoClip([base.set_position('center'), txt], size=(1080, 1920)))
        else: clips.append(base.set_position('center'))
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()

def upload_video(token, filename, title, description, tags, category):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)).execute()

def run_channel_safely(channel_type):
    # 🟢 रात 10 बजे का चेक (16:30 UTC)
    hour = time.localtime().tm_hour
    is_long = (hour == 22)
    for attempt in range(3):
        try:
            theme = random.choice(GADGET_HOOKS if channel_type == "GADGETS" else MYSTIC_HOOKS)
            script, prompts, captions, term, score = get_script_and_prompts(theme, (channel_type == "GADGETS"), is_long)
            imgs = fetch_amazon_images_strict(term) if channel_type == "GADGETS" else fetch_ai_images(prompts)
            create_human_voice(script, "temp.mp3")
            v_file = f"final_{channel_type}.mp4"
            make_video(imgs, captions, v_file, "temp.mp3")
            token = TOKEN_GADGETS if channel_type == "GADGETS" else TOKEN_MYSTIC
            upload_video(token, v_file, f"🤯 {theme}! #shorts", script, ["viral", "ai"], "28")
            send_telegram(f"✅ {channel_type} Live!\nType: {'Long' if is_long else 'Short'}\nScore: {score}%")
            return True
        except Exception as e:
            print(f"🛑 Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(60)
    run_channel_safely("MYSTIC")
