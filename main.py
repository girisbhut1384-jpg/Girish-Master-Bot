import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 Premium Setup (Yellow Text + 30s + Long Video) chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

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

# 🟢 UPDATE: 30-Second Shorts & Long Video Logic
def get_script_and_prompts(hook_theme, is_gadget=False, is_long=False):
    # अगर लॉन्ग वीडियो है तो 550 शब्द, शॉर्ट्स है तो 75 शब्द (30 सेकंड)
    words = "550 words" if is_long else "75 words (Strict 30 Seconds)"
    print(f"\n✅ AI Engine {words} ki script likh raha hai: {hook_theme}")
    
    if is_gadget:
        prompt = f"""You are a top Amazon affiliate marketer. THEME: "{hook_theme}".
        WRITE A {words} HINDI SCRIPT.
        RULES:
        1. START DIRECTLY WITH A SHOCKING 3-SECOND HOOK!
        2. If Shorts: Finish entire story in 30 seconds. If Long: Build detail for 8 minutes.
        3. Reveal the product as the ultimate solution.
        4. END EXACTLY WITH: 'यह शानदार गैजेट अभी आउट ऑफ़ स्टॉक होने से पहले चैनल के बायो से खरीदें।'
        """
    else:
        prompt = f"""You are a dark, mysterious storyteller. THEME: "{hook_theme}".
        WRITE A {words} HINDI SCRIPT.
        RULES:
        1. START DIRECTLY WITH A CREEPY HOOK!
        2. If Shorts: Finish mystery in 30 seconds. If Long: Build suspense for 8 minutes.
        3. END EXACTLY WITH: 'ऐसे ही खूंखार रहस्यों के लिए चैनल को सब्सक्राइब करें और लिंक बायो में देखें।'
        """

    prompt += """
    Return ONLY JSON:
    {
      "topic": "viral name",
      "script": "Hindi script...",
      "captions": ["8 captions"],
      "prompts": ["8 image prompts"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
            return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_search_term', '')
        except: time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

def fetch_amazon_images_strict(query):
    print(f"🛒 Amazon photo search: {query}")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": query, "country": "IN"}, timeout=40)
        for i, prod in enumerate(response.json().get("data", {}).get("products", [])[:8]):
            img_res = requests.get(prod.get("product_photo"), timeout=15)
            fname = f"amz_{i}.jpg"
            with open(fname, "wb") as f: f.write(img_res.content)
            image_files.append(fname)
        return image_files
    except: return fetch_ai_images([query]*8)

def fetch_ai_images(prompts):
    image_files = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1080&height=1920&nologo=true"
        res = requests.get(url, headers=headers, timeout=30)
        fname = f"ai_{i}.jpg"
        with open(fname, "wb") as f: f.write(res.content)
        image_files.append(fname)
    return image_files

def create_human_voice(text, filename, is_long=False):
    # लॉन्ग वीडियो के लिए आवाज़ की रफ़्तार थोड़ी कम रखी है ताकि नैचुरल लगे
    rate = "+15%" if not is_long else "+5%"
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate=rate) 
        await communicate.save(filename)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 UPDATE: Viral Yellow Text (Big & Bold with Heavy Stroke)
def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 600
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try: font = ImageFont.truetype("Roboto-Black.ttf", 150) # Increased Size
    except: font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text.upper(), width=12) 
    
    # Bright Yellow with Thick Black Outline (Stroke 12)
    draw.multiline_text((540, 300), wrapped_text, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", anchor="mm", align='center')
    
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
    main_audio = AudioFileClip(audio_file)
    dur_per_img = main_audio.duration / len(image_files)
    clips = []
    for i, img_path in enumerate(image_files):
        fixed = f"f_{i}.jpg"
        process_image_for_video(img_path, fixed)
        base = ImageClip(fixed).set_duration(dur_per_img).resize(lambda t: 1 + 0.05 * (t/dur_per_img))
        txt = create_centered_text_clip(captions[i], dur_per_img).set_position(('center', 0.65), relative=True) 
        clips.append(CompositeVideoClip([base.set_position('center'), txt], size=(1080, 1920)))
    final = concatenate_videoclips(clips, method="compose").set_audio(main_audio)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)

def upload_video(token, filename, title, description, tags, category):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)).execute()

# 🟢 UPDATE: Night Agent (10 PM IST Check)
def run_channel_safely(channel_type):
    # रात के 10 बजे IST (GitHub Actions में यह UTC समय के हिसाब से चेक होगा)
    hour = time.localtime().tm_hour
    is_long = (hour == 22) # 10 PM IST
    
    for attempt in range(3):
        try:
            theme = random.choice(GADGET_HOOKS if channel_type == "GADGETS" else MYSTIC_HOOKS)
            script, prompts, caps, term = get_script_and_prompts(theme, (channel_type == "GADGETS"), is_long)
            imgs = fetch_amazon_images_strict(term) if channel_type == "GADGETS" else fetch_ai_images(prompts)
            create_human_voice(script, "t.mp3", is_long)
            v_file = f"out_{channel_type}.mp4"
            make_video(imgs, caps, v_file, "t.mp3")
            token = TOKEN_GADGETS if channel_type == "GADGETS" else TOKEN_MYSTIC
            title = f"🤯 {theme} | Detailed Story" if is_long else f"🤯 {theme}! #shorts"
            upload_video(token, v_file, title, script, ["viral", "ai"], "28")
            print(f"✅ {channel_type} Live!")
            return True 
        except Exception as e:
            print(f"🛑 Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")
