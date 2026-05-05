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

# 🟢 UTF-8 Encoding Fix for Hindi Support
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 Security aur Premium Setup chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 🟢 Font Downloader
if not os.path.exists("Roboto-Black.ttf"):
    print("📥 Font download ho raha hai...")
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

# ENV SECRETS
GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

GADGET_HOOKS = ["Amazon's Hidden Tech", "Crazy Gadgets Under 1000", "Must-Have Smart Home Items", "Secret Car Hacks", "Genius Kitchen Tools"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Deep Sea Monsters", "Unsolved Crimes of History", "Lost Ancient Cities", "Creepy Government Secrets"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, is_gadget=False):
    # 🟢 UPDATE: Story-Based Prompt for Gadgets and Mystery
    print(f"\n✅ AI Engine dumdaar script likh raha hai: {hook_theme}")
    
    if is_gadget:
        prompt = f"""You are a top Amazon affiliate marketer. THEME: "{hook_theme}". 
        WRITE A 100-WORD HINDI STORY SCRIPT (35-40 seconds).
        RULES:
        1. Start with a daily life problem.
        2. Introduce gadget as a miracle solution.
        3. Explain features clearly.
        4. End with urgency and link call-to-action.
        Return JSON with: topic, script, captions (10), prompts (10), amazon_search_term."""
    else:
        prompt = f"""You are a mysterious storyteller. THEME: "{hook_theme}". 
        WRITE A 110-WORD HINDI SCRIPT (40 seconds).
        RULES:
        1. Build dark suspense.
        2. Reveal 3 shocking facts.
        3. END BY MENTIONING A MYSTERIOUS BOOK NAME related to the topic.
        4. Call-to-action for link in bio.
        Return JSON with: topic, script, captions (10), prompts (10), amazon_search_term."""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                return parsed['script'].replace("*", ""), parsed['prompts'][:10], parsed['captions'][:10], parsed.get('amazon_search_term', '')
        except: time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

def fetch_amazon_images_strict(query):
    print(f"🛒 Amazon se '{query}' ki photos nikali ja rahi hain...")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": query, "country": "IN"}, timeout=40)
        if response.status_code == 200:
            for i, prod in enumerate(response.json().get("data", {}).get("products", [])[:10]):
                img_url = prod.get("product_photo")
                if img_url:
                    img_res = requests.get(img_url, timeout=15)
                    fname = f"amz_img_{i}.jpg"
                    with open(fname, "wb") as f: f.write(img_res.content)
                    image_files.append(fname)
        return image_files if len(image_files) >= 5 else fetch_ai_images([query]*10)
    except: return fetch_ai_images([query]*10)

def fetch_ai_images(prompts):
    print("🎨 Generating High-Quality AI Images...")
    image_files = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + ', 8k, photorealistic, clean focus')}?width=1080&height=1920&nologo=true"
        for _ in range(3): 
            try:
                res = requests.get(url, headers=headers, timeout=30) 
                if res.status_code == 200: 
                    fname = f"ai_scene_{i}.jpg"
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    break
            except: time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%") 
        await communicate.save(filename)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 UPDATE: VIRAL UI - EXTRA LARGE YELLOW TEXT
def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 600
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("Roboto-Black.ttf", 155) 
    except: font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text.upper(), width=10) 
    # Bright Yellow with Thick Black Outline (Stroke 12)
    draw.multiline_text((540, 300), wrapped_text, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", anchor="mm", align='center')
    
    fname = f"cap_{random.randint(1000, 9999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def process_image_for_video(img_path, output_path):
    img = Image.open(img_path).convert("RGB")
    bg = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=45))
    ratio = 1080 / img.width
    new_h = int(img.height * ratio)
    fg = img.resize((1080, new_h), Image.Resampling.LANCZOS)
    bg.paste(fg, (0, (1920 - new_h) // 2))
    bg.save(output_path)
    return output_path

def make_video(image_files, captions, final_vid, audio_file):
    print("🎬 Professional Video Render ho raha hai...")
    main_audio = AudioFileClip(audio_file)
    dur_per_img = main_audio.duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        fixed = f"fixed_{i}.jpg"
        process_image_for_video(img_path, fixed)
        base = ImageClip(fixed).set_duration(dur_per_img).resize(lambda t: 1 + 0.05 * (t / dur_per_img))
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            txt_clip = create_centered_text_clip(cap_text, dur_per_img).set_position(('center', 0.65), relative=True) 
            clips.append(CompositeVideoClip([base.set_position('center'), txt_clip], size=(1080, 1920)))
        else:
            clips.append(base.set_position('center'))
        
    video = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    video.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()

def upload_video(token, filename, title, description, tags, category):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "tags": tags, "categoryId": category},
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    ).execute()

def run_channel_safely(channel_type):
    for attempt in range(3):
        try:
            if channel_type == "GADGETS":
                theme = random.choice(GADGET_HOOKS)
                script, prompts, captions, amz_term = get_script_and_prompts(theme, is_gadget=True)
                imgs = fetch_amazon_images_strict(amz_term)
                
                # 🟢 UPDATE: Specific Amazon Search Link
                clean_term = urllib.parse.quote(amz_term)
                amz_link = f"https://www.amazon.in/s?k={clean_term}&tag=girishbhut07-21"
                
                create_human_voice(script, "v_gadget.mp3")
                make_video(imgs, captions, "final_gadget.mp4", "v_gadget.mp3")
                desc = f"🔥 Buy Here: {amz_link}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 Best {amz_term}! #shorts", desc, ["gadgets", "tech"], "28")
                print("✅ GADGETS Live!")
                return True 

            elif channel_type == "MYSTIC":
                theme = random.choice(MYSTIC_HOOKS)
                script, prompts, captions, _ = get_script_and_prompts(theme, is_gadget=False)
                imgs = fetch_ai_images(prompts)
                create_human_voice(script, "v_mystic.mp3")
                make_video(imgs, captions, "final_mystic.mp4", "v_mystic.mp3")
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 Dark Mystery: {theme}! #shorts", script, ["mystery", "facts"], "28")
                print("✅ MYSTIC Live!")
                return True 
                
        except Exception as e: 
            print(f"🛑 Error: {e}. Retrying...")
            time.sleep(10)

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(60)
    run_channel_safely("MYSTIC")
