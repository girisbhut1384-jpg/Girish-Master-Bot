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

# 🟢 UPDATE: UTF-8 Encoding Fix (ताकि हिंदी के कारण Latin-1 एरर न आए)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 Premium Setup (Yellow Text + 40s Story + Dynamic Links) chalu...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 🟢 Font Downloader (बड़े टेक्स्ट के लिए)
if not os.path.exists("Roboto-Black.ttf"):
    print("📥 Font download ho raha hai...")
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

# ENV SECRETS (GitHub Secrets से आएंगे)
GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

GADGET_HOOKS = ["Hidden Tech Gems", "Must-Have 2026 Gadgets", "Insane Survival Inventions", "Genius Home Tools"]
MYSTIC_HOOKS = ["Mysterious Space Events", "Deep Ocean Secrets", "Unexplained History", "Parallel Universe Proof"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

# 🟢 UPDATE: कहानी के रूप में 30-40 सेकंड की स्क्रिप्ट और English Search Term
def get_script_and_prompts(hook_theme, is_gadget=False):
    print(f"\n✅ AI Engine dumdaar script likh raha hai: {hook_theme}")
    
    if is_gadget:
        prompt = f"""Write a 100-word viral HINDI STORY script for a YouTube Short. Theme: "{hook_theme}".
        STORY STRUCTURE:
        1. 0-10s: Start with a real-life frustrating problem.
        2. 10-30s: Introduce the product as the hero solution. Explain how it works.
        3. 30-40s: Stock warning and link instructions.
        IMPORTANT: The 'amazon_search_term' MUST BE IN ENGLISH ONLY.
        RULES: End with 'शानदार गैजेट का लिंक पहले कमेंट में है, अभी खरीदें।'
        Return JSON: {{"topic": "name", "script": "Hindi...", "captions": ["10-lines"], "prompts": ["10-prompts"], "amazon_search_term": "English Product Name Only"}}"""
    else:
        prompt = f"""Write a 120-word dark Mystery HINDI script (40 seconds). Theme: "{hook_theme}".
        STORY STRUCTURE:
        1. Start with intense suspense. 2. Reveal 3 shocking facts.
        3. MUST END BY MENTIONING A FAMOUS MYSTERIOUS BOOK NAME.
        4. End with 'Is rahasya ko janne ke liye link bio mein dekhein.'
        Return JSON: {{"topic": "name", "script": "Hindi...", "captions": ["10-lines"], "prompts": ["10-prompts"]}}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
            return (parsed['script'].replace("*", ""), parsed['prompts'][:10], parsed['captions'][:10], parsed.get('amazon_search_term', 'Gadget'))
        except: time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

def fetch_amazon_images_strict(query):
    # 🟢 Latin-1 Error रोकने के लिए Encoding
    encoded_query = urllib.parse.quote(str(query))
    print(f"🛒 Amazon photo search: {query}")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": encoded_query, "country": "IN"}, timeout=40)
        for i, prod in enumerate(response.json().get("data", {}).get("products", [])[:10]):
            img_res = requests.get(prod.get("product_photo"), timeout=20)
            fname = f"amz_{i}.jpg"
            with open(fname, "wb") as f: f.write(img_res.content)
            image_files.append(fname)
        return image_files if len(image_files) >= 5 else fetch_ai_images([query]*10)
    except: return fetch_ai_images([query]*10)

def fetch_ai_images(prompts):
    print("🎨 Generating HD AI Images...")
    files = []
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(str(p) + ', photorealistic, 8k')}?width=1080&height=1920&nologo=true"
        for attempt in range(3):
            try:
                res = requests.get(url, timeout=40)
                if res.status_code == 200:
                    fname = f"ai_{i}.jpg"
                    with open(fname, "wb") as f: f.write(res.content)
                    files.append(fname)
                    break
            except: time.sleep(5)
    return files

def create_human_voice(text, filename):
    async def _gen():
        # रफ़्तार 10% ताकि आवाज़ साफ़ समझ आए
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%") 
        await communicate.save(filename)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_gen())

# 🟢 UPDATE: विशाल पीला टेक्स्ट (साइज़ 160) और काला आउटलाइन (12)
def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 600
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("Roboto-Black.ttf", 160)
    except: font = ImageFont.load_default()
    wrapped = textwrap.fill(text.upper(), width=10)
    draw.multiline_text((540, 300), wrapped, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", anchor="mm", align='center')
    fname = f"cap_{random.randint(1,9999)}.png"
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
    print("🎬 Video Render ho raha hai...")
    main_audio = AudioFileClip(audio_file)
    dur_per_img = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        fixed = f"f_{i}.jpg"
        process_image_for_video(img_path, fixed)
        base = ImageClip(fixed).set_duration(dur_per_img).resize(lambda t: 1 + 0.05 * (t / dur_per_img))
        txt = create_centered_text_clip(captions[i], dur_per_img).set_position(('center', 0.65), relative=True)
        clips.append(CompositeVideoClip([base.set_position('center'), txt], size=(1080, 1920)))
    final = concatenate_videoclips(clips).set_audio(main_audio)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()

def upload_video(token, filename, title, desc, tags, cat):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": cat}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(filename, resumable=True)).execute()

def run_channel_safely(channel_type):
    for attempt in range(3):
        try:
            if channel_type == "GADGETS":
                theme = random.choice(GADGET_HOOKS)
                script, prompts, caps, term = get_script_and_prompts(theme, is_gadget=True)
                imgs = fetch_amazon_images_strict(term)
                # 🟢 UPDATE: Dynamic Amazon Search Link
                amz_link = f"https://www.amazon.in/s?k={urllib.parse.quote(term)}&tag=girishbhut07-21"
                create_human_voice(script, "v_gadget.mp3")
                make_video(imgs, caps, "final_gadget.mp4", "v_gadget.mp3")
                desc = f"🔥 Buy Here: {amz_link}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 Best {term}! #shorts", desc, ["gadgets", "ai"], "28")
                return True 
            elif channel_type == "MYSTIC":
                theme = random.choice(MYSTIC_HOOKS)
                script, prompts, caps, _ = get_script_and_prompts(theme, is_gadget=False)
                imgs = fetch_ai_images(prompts)
                create_human_voice(script, "v_mystic.mp3")
                make_video(imgs, caps, "final_mystic.mp4", "v_mystic.mp3")
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 Dark Mystery: {theme}! #shorts", script, ["mystery", "facts"], "28")
                return True 
        except Exception as e: 
            print(f"🛑 Error: {e}. Retrying in 10s...")
            time.sleep(10)

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(60)
    run_channel_safely("MYSTIC")
