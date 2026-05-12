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
    elif channel_type == "WEALTH":
        prompt = f"""You are selling an AI YouTube automation bot. THEME: "{hook_theme}". WRITE A 90-100 WORD HINDI SCRIPT.
        RULES: 1. NO INTRO. Hook about passive income and relaxing at home while AI works. 
        2. NO MENTION OF CITIES OR CODE LINES. Emphasize freedom from 9 to 5.
        3. END EXACTLY WITH: 'मेरा यह ऑटोमैटिक AI सेटअप अभी डाउनलोड करें! लिंक डिस्क्रिप्शन और कमेंट में है!'
        AMAZON SEARCH TERM: Leave empty ("")."""
    elif channel_type == "ZEROTOUCH":
        prompt = f"""You are selling an AI YouTube automation bot. THEME: "{hook_theme}". WRITE A 90-100 WORD HINDI SCRIPT.
        RULES: 1. NO INTRO. Hook about running a channel with ZERO camera and ZERO editing.
        2. NO MENTION OF CITIES OR CODE LINES. Highlight the magic of the AI tool doing all the work.
        3. END EXACTLY WITH: 'यह सीक्रेट ऑटोमेशन कोड अभी डाउनलोड करें, लिंक डिस्क्रिप्शन और कमेंट बॉक्स में है!'
        AMAZON SEARCH TERM: Leave empty ("")."""
    elif channel_type == "EMPIRE":
        prompt = f"""You are selling an AI YouTube automation bot. THEME: "{hook_theme}". WRITE A 90-100 WORD HINDI SCRIPT.
        RULES: 1. NO INTRO. Hook proving that an AI robot can run channels automatically and get Amazon sales.
        2. NO MENTION OF CITIES OR CODE LINES. Challenge people who still edit manually.
        3. END EXACTLY WITH: 'मेरा पूरा रेडी-टू-अर्न सेटअप डाउनलोड करें और आज ही अपना चैनल शुरू करें! लिंक डिस्क्रिप्शन और कमेंट में है!'
        AMAZON SEARCH TERM: Leave empty ("")."""

    prompt += """
    Return ONLY valid JSON with EXACTLY 6 captions and 6 prompts:
    {
      "topic": "viral topic name",
      "script": "Hindi script here (min 90 words)...",
      "captions": ["Caption 1", "Caption 2", "Caption 3", "Caption 4", "Caption 5", "Caption 6"],
      "prompts": ["Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                if parsed.get('script'):
                    print(f"🎯 Script Ready for {channel_type}!")
                    return parsed['script'].replace("*", ""), parsed['prompts'][:6], parsed['captions'][:6], parsed.get('amazon_search_term', 'Gadget')
        except: time.sleep(5)
    raise Exception(f"🚨 AI Model Failed for {channel_type}!")

def fetch_amazon_images_strict(query, channel_type):
    clean_query = re.sub(r'[^a-zA-Z0-9 ]', '', str(query)).strip()
    print(f"🛒 Amazon se '{clean_query}' ki photos nikal rahi hain...")
    if not RAPIDAPI_KEY: raise Exception("⚠️ RAPIDAPI_KEY Missing!")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": clean_query, "page": "1", "country": "IN", "sort_by": "RELEVANCE"}, timeout=40)
        if response.status_code == 200:
            for i, prod in enumerate(response.json().get("data", {}).get("products", [])):
                if len(image_files) >= 6: break
                photo_url = prod.get("product_photo")
                if photo_url:
                    img_res = requests.get(photo_url, timeout=15)
                    if img_res.status_code == 200:
                        fname = f"amazon_img_{channel_type}_{i}.jpg"
                        with open(fname, "wb") as f: f.write(img_res.content)
                        image_files.append(fname)
            if len(image_files) >= 4: return image_files
            raise Exception("⚠️ Photos kam hain.")
        raise Exception("⚠️ API Error")
    except Exception as e: raise Exception(f"Amazon Fail: {e}")

def fetch_ai_images(prompts, channel_type):
    image_files, seed = random.randint(1000, 99999), []
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + ', highly detailed, 8k')}?width=1080&height=1920&nologo=true&seed={seed+i}"
        fname = f"ai_scene_{channel_type}_{i}.jpg"
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
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
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
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped_text, font=font)
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", align='center')
    temp_filename = f"temp_caption_{channel_type}_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def process_image_for_video(img_path, output_path):
    img = Image.open(img_path).convert("RGB")
    bg = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=40))
    ratio = 1080 / img.width
    new_h = int(img.height * ratio)
    if new_h > 1920:
        ratio = 1920 / img.height
        new_w = int(img.width * ratio)
        fg = img.resize((new_w, 1920), Image.Resampling.LANCZOS)
        bg.paste(fg, ((1080 - new_w) // 2, 0))
    else:
        fg = img.resize((1080, new_h), Image.Resampling.LANCZOS)
        bg.paste(fg, (0, (1920 - new_h) // 2))
    bg.save(output_path)
    return output_path

def make_video(image_files, captions, final_vid, audio_file, channel_type):
    print("✅ Professional Video Render ho raha hai...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        fixed_img_path = f"fixed_{channel_type}_{i}.jpg"
        process_image_for_video(img_path, fixed_img_path)
        base_clip = ImageClip(fixed_img_path)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.04 * (t / time_per_image)).set_duration(time_per_image)
        cap_text = captions[i] if i < len(captions) else ""
        
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, time_per_image, channel_type).set_position(('center', 0.65), relative=True) 
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = zoomed_clip
        else: final_clip = zoomed_clip
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    main_audio.close()
    video.close()

def upload_video_and_comment(token, filename, title, description, tags, category, auto_comment=""):
    if not token:
        print("⚠️ Token missing, skipping upload.")
        return
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
    response = request.execute()
    video_id = response.get("id")
    print(f"✅ Video Uploaded Successfully! ID: {video_id}")
    
    if auto_comment and video_id:
        try:
            time.sleep(5) 
            comment_request = youtube.commentThreads().insert(
                part="snippet",
                body={"snippet": {"videoId": video_id, "topLevelComment": {"snippet": {"textOriginal": auto_comment}}}}
            )
            comment_request.execute()
            print("💬 BOOM! AI ne automatic link wala comment pin kar diya hai!")
        except Exception as e:
            print(f"⚠️ Comment fail hua (par video dal gaya): {e}")

def run_channel_safely(channel_type):
    for attempt in range(2): 
        try:
            print(f"\n🚀 Starting Process for {channel_type}")
            if channel_type == "GADGETS":
                script, prompts, captions, amazon_term = get_script_and_prompts("GADGETS", random.choice(GADGET_HOOKS))
                
                try:
                    image_files = fetch_amazon_images_strict(amazon_term, channel_type) 
                except Exception as e:
                    print(f"⚠️ Amazon API Failed ({e}). Gadgets skip kar rahe hain, machine crash nahi hogi!")
                    return False
                    
                create_human_voice(script, f"voice_{channel_type}.mp3")
                make_video(image_files, captions, f"final_{channel_type}.mp4", f"voice_{channel_type}.mp3", channel_type)
                clean_term = re.sub(r'[^a-zA-Z0-9 ]', '', str(amazon_term)).strip()
                amz_link = f"https://www.amazon.in/s?k={urllib.parse.quote(clean_term)}&tag={AMAZON_TAG}"
                desc = f"🔥 👉 यह शानदार गैजेट आउट ऑफ़ स्टॉक होने से पहले यहाँ से खरीदें!\n🔗 लिंक: {amz_link}\n\n{script}"
                upload_video_and_comment(TOKEN_GADGETS, f"final_{channel_type}.mp4", f"🤯 Best {amazon_term}! #shorts", desc, ["shorts", "gadgets", "amazon finds", "tech"], "28")
                
            elif channel_type == "MYSTIC":
                script, prompts, captions, _ = get_script_and_prompts("MYSTIC", random.choice(MYSTIC_HOOKS))
                image_files = fetch_ai_images(prompts, channel_type)
                create_human_voice(script, f"voice_{channel_type}.mp3")
                make_video(image_files, captions, f"final_{channel_type}.mp4", f"voice_{channel_type}.mp3", channel_type)
                desc = f"🔥 👉 रहस्यमयी किताबें और गैजेट्स यहाँ देखें: https://www.amazon.in/?tag={AMAZON_TAG}\n\n{script}"
                upload_video_and_comment(TOKEN_MYSTIC, f"final_{channel_type}.mp4", f"🤯 Secret They Hid From You! #shorts", desc, ["shorts", "mystery", "creepy", "facts"], "28")

            elif channel_type == "WEALTH":
                script, prompts, captions, _ = get_script_and_prompts("WEALTH", random.choice(WEALTH_HOOKS))
                image_files = fetch_ai_images(prompts, channel_type)
                create_human_voice(script, f"voice_{channel_type}.mp3")
                make_video(image_files, captions, f"final_{channel_type}.mp4", f"voice_{channel_type}.mp3", channel_type)
                desc = f"🔥 👉 मेरा पूरा ऑटोमैटिक AI सेटअप यहाँ से डाउनलोड करें: {GUMROAD_LINK}\n\n{script}"
                upload_video_and_comment(TOKEN_WEALTH, f"final_{channel_type}.mp4", "Make Money While Sleeping! 💸 #shorts", desc, ["passive income", "ai bot", "wealth"], "28", MARKETING_COMMENT)
                
            elif channel_type == "ZEROTOUCH":
                script, prompts, captions, _ = get_script_and_prompts("ZEROTOUCH", random.choice(ZEROTOUCH_HOOKS))
                image_files = fetch_ai_images(prompts, channel_type)
                create_human_voice(script, f"voice_{channel_type}.mp3")
                make_video(image_files, captions, f"final_{channel_type}.mp4", f"voice_{channel_type}.mp3", channel_type)
                desc = f"🔥 👉 यह जादुई ऑटोमेशन कोड अभी पाएँ: {GUMROAD_LINK}\n\n{script}"
                upload_video_and_comment(TOKEN_ZEROTOUCH, f"final_{channel_type}.mp4", "Zero Touch AI YouTube Automation! 💻 #shorts", desc, ["youtube automation", "ai tool"], "28", MARKETING_COMMENT)
                
            elif channel_type == "EMPIRE":
                script, prompts, captions, _ = get_script_and_prompts("EMPIRE", random.choice(EMPIRE_HOOKS))
                image_files = fetch_ai_images(prompts, channel_type)
                create_human_voice(script, f"voice_{channel_type}.mp3")
                make_video(image_files, captions, f"final_{channel_type}.mp4", f"voice_{channel_type}.mp3", channel_type)
                desc = f"🔥 👉 अपना ऑटोमैटिक चैनल आज ही शुरू करें: {GUMROAD_LINK}\n\n{script}"
                upload_video_and_comment(TOKEN_EMPIRE, f"final_{channel_type}.mp4", "My AI Runs 3 Channels Automatically! 🤖 #shorts", desc, ["ai", "automation", "tech"], "28", MARKETING_COMMENT)
                
            return True
        except Exception as e: 
            print(f"🛑 Error on {channel_type}: {e}. Machine dobara koshish kar rahi hai...")
            time.sleep(10)
    print(f"❌ {channel_type} FAILED after retries.")
    return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 PHASE 1: Purane Regular Channels (Gadgets & Mystic)")
    print("="*50)
    
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")

    # 🟢 15 Minute ka Smart Delay
    print("\n" + "="*50)
    print("⏳ SMART BREAK: Machine 15 minute ke liye shant ho rahi hai...")
    print("="*50)
    
    for i in range(15, 0, -1):
        print(f"⏳ Phase 2 shuru hone mein samay baki: {i} minute...")
        time.sleep(60) 

    print("\n" + "="*50)
    print("🚀 PHASE 2: Naye AI Marketing Channels (Gumroad Sales)")
    print("="*50)
    
    run_channel_safely("WEALTH")
    time.sleep(30)
    run_channel_safely("ZEROTOUCH")
    time.sleep(30)
    run_channel_safely("EMPIRE")
    
    print("\n✅ MISSION SUCCESSFUL! 5-Channel Superfast Upload Complete!")
