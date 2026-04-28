import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 🟢 Image Resampling Fix
if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 Security aur Premium Setup chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 🟢 Font Downloader
if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

# ENV SECRETS
GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
TELEGRAM_TOKEN = "8382528984:AAHLJYwQIvLN5xEHV9iSjvgI18b8pF4bWJ8"
CHAT_ID = "8285187691"

# 🟢 IMPROVEMENT 1: DYNAMIC TOPIC ENGINE
GADGET_HOOKS = ["Advanced Tech 2026", "Mind-Blowing Home Gadgets", "Insane Survival Gear", "Smart Car Accessories", "Future Kitchen Tools"]
MYSTIC_HOOKS = ["Ancient Aliens Secrets", "Forbidden Space Mysteries", "Unsolved Deep Sea Myths", "Time Travel Paradoxes", "Lost Cities of Gold"]

def send_telegram(msg):
    try: requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    except: pass

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, is_gadget=False, is_long=False):
    # 🟢 IMPROVEMENT 2: 30-SEC VS LONG LOGIC
    words = "500-600 words" if is_long else "70-75 words (Strict 30 Seconds)"
    print(f"\n✅ AI Engine {words} ki script likh raha hai: {hook_theme}")
    
    prompt = f"""You are a professional creator. THEME: "{hook_theme}". WRITE A {words} HINDI SCRIPT.
    FOR SHORTS: Finish in 30s. FOR LONG: Deep story.
    Return ONLY JSON: {{"topic": "viral name", "script": "Hindi script...", "captions": ["8 items"], "prompts": ["8 items"], "amazon_term": "name", "score": 95}}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
            return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_term', ''), parsed.get('score', 90)
        except: time.sleep(2)
    raise Exception("🚨 AI Failed")

def fetch_amazon_images_strict(query):
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": query, "page": "1", "country": "IN"}, timeout=40)
        for i, prod in enumerate(response.json().get("data", {}).get("products", [])):
            if len(image_files) >= 8: break
            img_res = requests.get(prod.get("product_photo"), timeout=15)
            if img_res.status_code == 200:
                fname = f"img_{i}.jpg"
                with Image.open(requests.get(prod.get("product_photo"), stream=True).raw).convert("RGB").save(fname)
                image_files.append(fname)
        return image_files
    except: return fetch_ai_images([query]*8)

def fetch_ai_images(prompts):
    image_files = []
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1080&height=1920&nologo=true"
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            fname = f"ai_{i}.jpg"
            with open(fname, "wb") as f: f.write(res.content)
            image_files.append(fname)
    return image_files

def create_human_voice(text, filename):
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%")
        await communicate.save(filename)
    asyncio.run(_generate())

def create_centered_text_clip(text, duration):
    # 🟢 IMPROVEMENT 3: VIRAL UI (Large Yellow/Black)
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Black.ttf", 140)
    wrapped = textwrap.fill(text.upper(), width=12)
    draw.multiline_text((540, 200), wrapped, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", anchor="mm", align='center')
    fname = f"cap_{random.randint(1,999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

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
    main_audio = AudioFileClip(audio_file)
    dur_per_img = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        fixed = f"fixed_{i}.jpg"
        process_image_for_video(img_path, fixed)
        base = ImageClip(fixed).set_duration(dur_per_img).resize(lambda t: 1 + 0.04 * (t/dur_per_img))
        txt = create_centered_text_clip(captions[i], dur_per_img).set_position(('center', 0.65), relative=True)
        clips.append(CompositeVideoClip([base.set_position('center'), txt], size=(1080,1920)))
    final = concatenate_videoclips(clips).set_audio(main_audio)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)

def upload_video(token, filename, title, description, tags, category):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(filename, resumable=True)).execute()

def run_channel_safely(channel_type):
    # 🟢 10 PM IST CHECK (16:30 UTC)
    hour = time.localtime().tm_hour
    is_long = (hour == 22)
    try:
        theme = random.choice(GADGET_HOOKS if channel_type == "GADGETS" else MYSTIC_HOOKS)
        script, prompts, captions, term, score = get_script_and_prompts(theme, (channel_type=="GADGETS"), is_long)
        imgs = fetch_amazon_images_strict(term) if channel_type == "GADGETS" else fetch_ai_images(prompts)
        v_file = f"final_{channel_type}.mp4"
        create_human_voice(script, "temp.mp3")
        make_video(imgs, captions, v_file, "temp.mp3")
        token = TOKEN_GADGETS if channel_type == "GADGETS" else TOKEN_MYSTIC
        upload_video(token, v_file, f"🤯 {theme}! #shorts", script, ["shorts", "viral"], "28")
        send_telegram(f"✅ {channel_type} Live!\nType: {'Long' if is_long else 'Short'}\nScore: {score}%")
    except Exception as e: send_telegram(f"🛑 Error {channel_type}: {str(e)}")

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(60)
    run_channel_safely("MYSTIC")
