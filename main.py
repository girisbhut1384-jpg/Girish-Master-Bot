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
import io  

from PIL import Image, ImageDraw, ImageFont, ImageFilter
# 🟢 PIL Fixes
if not hasattr(Image, 'ANTIALIAS'): Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

# 🟢 Unicode Hindi Fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🚀 5-Channel Superfast 2-Part System Active (Crash-Proof Mode)!")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# 🟢 5 Channels Tokens
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
TOKEN_EMPIRE = os.environ.get("YOUTUBE_TOKEN_EMPIRE")
TOKEN_ZEROTOUCH = os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH")
TOKEN_WEALTH = os.environ.get("YOUTUBE_TOKEN_WEALTH")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

# 🟢 Links & Hooks
AMAZON_TAG = "girishbhut07-21"
GUMROAD_LINK = "https://girisbhut.gumroad.com/l/ajhzk"
MARKETING_COMMENT = f"🔥 अपना खुद का ऑटोमैटिक AI चैनल शुरू करें और सोते हुए कमाई करें! कोड यहाँ से डाउनलोड करें: {GUMROAD_LINK}"

GADGET_HOOKS = ["Secret Amazon Hacks", "Crazy Gadgets Under 500", "Smart Home Magic", "Genius Survival Tools", "Car Gadgets You Need", "Hidden Kitchen Tech"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Unsolved Psychological Mysteries", "Ghost Towns of India", "Time Travel Proof", "Dark Web Secrets", "Creepy Historical Events"]
WEALTH_HOOKS = ["Make Money Sleeping", "Quit 9 to 5 Job", "Passive Income Secret", "AI Robot Earning"]
ZEROTOUCH_HOOKS = ["Zero Editing Needed", "No Camera YouTube", "Magic AI Tool", "100% Autopilot System"]
EMPIRE_HOOKS = ["AI Running My Channel", "Robots Doing Hard Work", "Stop Manual Editing", "Tech Future Now"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(channel_type, hook_theme):
    print(f"\n✅ AI Engine script likh raha hai ({channel_type} - {hook_theme})...")
    
    if channel_type == "GADGETS":
        prompt = f"""You are a top Amazon affiliate marketer. THEME: "{hook_theme}". WRITE A 90-100 WORD HINDI SCRIPT.
        RULES: 1. NO INTRO. SHOCKING 3-SEC HOOK! 2. Describe frustrating problem. 3. Reveal product. 
        4. END EXACTLY WITH: 'यह शानदार गैजेट अभी आउट ऑफ़ स्टॉक होने से पहले नीचे दिए गए लिंक से खरीदें।'
        AMAZON SEARCH TERM: Simple 2-3 word real English product name."""
    elif channel_type == "MYSTIC":
        prompt = f"""You are a dark, mysterious storyteller. THEME: "{hook_theme}". WRITE A 90-100 WORD HINDI SCRIPT.
        RULES: 1. NO INTRO. CREEPY 3-SEC HOOK! 2. Build extreme suspense. 3. Reveal unique fact.
        4. END EXACTLY WITH: 'ऐसे ही खूंखार रहस्यों के लिए चैनल को सब्सक्राइब करें और लिंक बायो में देखें।'
        AMAZON SEARCH TERM: Leave empty ("")."""
    elif channel_type in ["WEALTH", "ZEROTOUCH", "EMPIRE"]:
        prompt = f"""You are selling an AI YouTube automation bot. THEME: "{hook_theme}". WRITE A 90-100 WORD HINDI SCRIPT.
        RULES: 1. NO INTRO. Hook about freedom from 9 to 5 or automatic AI work. 
        2. NO MENTION OF CITIES OR CODE LINES.
        3. END EXACTLY WITH: 'मेरा यह सेटअप अभी डाउनलोड करें! लिंक डिस्क्रिप्शन और कमेंट में है!'
        AMAZON SEARCH TERM: Leave empty ("")."""

    prompt += """
    Return ONLY valid JSON with EXACTLY 6 captions and 6 prompts:
    {
      "topic": "viral topic name",
      "script": "Hindi script here...",
      "captions": ["Caption 1", "Caption 2", "Caption 3", "Caption 4", "Caption 5", "Caption 6"],
      "prompts": ["Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
        return parsed['script'].replace("*", ""), parsed['prompts'][:6], parsed['captions'][:6], parsed.get('amazon_search_term', 'Gadget')
    except:
        raise Exception(f"🚨 AI Model Failed for {channel_type}!")

def fetch_amazon_images_strict(query, channel_type):
    clean_query = re.sub(r'[^a-zA-Z0-9 ]', '', str(query)).strip()
    print(f"🛒 Amazon se '{clean_query}' ki photos nikal rahi hain...")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": clean_query, "country": "IN"}, timeout=40)
        if response.status_code == 200:
            for i, prod in enumerate(response.json().get("data", {}).get("products", [])):
                if len(image_files) >= 6: break
                photo_url = prod.get("product_photo")
                if photo_url:
                    img_res = requests.get(photo_url, timeout=15)
                    fname = f"amazon_img_{channel_type}_{i}.jpg"
                    with open(fname, "wb") as f: f.write(img_res.content)
                    image_files.append(fname)
        return image_files
    except: return []

def fetch_ai_images(prompts, channel_type):
    # 🟢 Fixed seed logic to avoid 'concatenate list' error
    image_files = []
    seed_val = random.randint(1000, 99999)
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1080&height=1920&nologo=true&seed={seed_val + i}"
        fname = f"ai_scene_{channel_type}_{i}.jpg"
        try:
            res = requests.get(url, headers=headers, timeout=30)
            if res.status_code == 200:
                with open(fname, "wb") as f: f.write(res.content)
                image_files.append(fname)
        except: pass
    return image_files

def create_human_voice(text, filename):
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%") 
        await communicate.save(filename)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def create_centered_text_clip(text, duration, channel_type):
    canvas_w, canvas_h = 1080, 800
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("Roboto-Black.ttf", 150)
    except: font = ImageFont.load_default()
    wrapped_text = textwrap.fill(text.upper(), width=12)
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(((canvas_w - text_w) // 2, (canvas_h - text_h) // 2), wrapped_text, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", align='center')
    temp_filename = f"temp_cap_{channel_type}_{random.randint(100,999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def make_video(image_files, captions, final_vid, audio_file, channel_type):
    main_audio = AudioFileClip(audio_file)
    dur = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        img = Image.open(img_path).convert("RGB")
        bg = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
        new_h = int(img.height * (1080 / img.width))
        fg = img.resize((1080, new_h), Image.Resampling.LANCZOS)
        bg.paste(fg, (0, (1920 - new_h) // 2))
        fixed_path = f"f_{channel_type}_{i}.jpg"
        bg.save(fixed_path)
        base = ImageClip(fixed_path).set_duration(dur)
        if i < len(captions):
            txt = create_centered_text_clip(captions[i], dur, channel_type).set_position(('center', 0.65), relative=True)
            clips.append(CompositeVideoClip([base, txt]))
        else: clips.append(base)
    final = concatenate_videoclips(clips).set_audio(main_audio)
    final.write_videofile(final_vid, fps=24, codec="libx264", preset="ultrafast", logger=None)

def upload_video_and_comment(token, filename, title, description, tags, category, auto_comment=""):
    if not token: return
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    req = youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(filename, resumable=True))
    res = req.execute()
    if auto_comment and res.get("id"):
        time.sleep(5)
        youtube.commentThreads().insert(part="snippet", body={"snippet": {"videoId": res["id"], "topLevelComment": {"snippet": {"textOriginal": auto_comment}}}}).execute()

def run_channel_safely(channel_type):
    try:
        print(f"🚀 Starting {channel_type}...")
        if channel_type == "GADGETS":
            script, prompts, captions, amz_term = get_script_and_prompts("GADGETS", random.choice(GADGET_HOOKS))
            imgs = fetch_amazon_images_strict(amz_term, channel_type)
            if not imgs: 
                print("⚠️ Amazon API Failed. Skipping Gadgets.")
                return
            create_human_voice(script, "v.mp3")
            make_video(imgs, captions, "f.mp4", "v.mp3", "G")
            upload_video_and_comment(TOKEN_GADGETS, "f.mp4", f"🤯 Best {amz_term}! #shorts", script, ["gadgets"], "28")
        elif channel_type == "MYSTIC":
            script, prompts, captions, _ = get_script_and_prompts("MYSTIC", random.choice(MYSTIC_HOOKS))
            imgs = fetch_ai_images(prompts, "M")
            create_human_voice(script, "v.mp3")
            make_video(imgs, captions, "f.mp4", "v.mp3", "M")
            upload_video_and_comment(TOKEN_MYSTIC, "f.mp4", "Secret Fact! #shorts", script, ["mystery"], "28")
        elif channel_type in ["WEALTH", "ZEROTOUCH", "EMPIRE"]:
            tokens = {"WEALTH": TOKEN_WEALTH, "ZEROTOUCH": TOKEN_ZEROTOUCH, "EMPIRE": TOKEN_EMPIRE}
            script, prompts, captions, _ = get_script_and_prompts(channel_type, random.choice(WEALTH_HOOKS if channel_type=="WEALTH" else EMPIRE_HOOKS))
            imgs = fetch_ai_images(prompts, channel_type[0])
            create_human_voice(script, "v.mp3")
            make_video(imgs, captions, "f.mp4", "v.mp3", channel_type[0])
            upload_video_and_comment(tokens[channel_type], "f.mp4", f"AI {channel_type} Money! #shorts", script, ["ai"], "28", MARKETING_COMMENT)
    except Exception as e: print(f"🛑 Error on {channel_type}: {e}")

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(10)
    run_channel_safely("MYSTIC")
    print("⏳ SMART BREAK: 15 minutes...")
    time.sleep(900)
    run_channel_safely("WEALTH")
    time.sleep(10)
    run_channel_safely("ZEROTOUCH")
    time.sleep(10)
    run_channel_safely("EMPIRE")
    print("✅ MISSION SUCCESSFUL!")
