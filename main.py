import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Encoding fix for Hindi
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

GADGET_HOOKS = ["Amazon's Hidden Tech", "Future Inventions 2026", "Mind-Blowing Smart Tools", "Secret Car Gadgets"]
MYSTIC_HOOKS = ["Terrifying Space Secrets", "Deep Sea Creatures", "Forbidden History", "Unsolved Mysteries"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

# 🟢 UPDATE: 30-Second Rule & Long Video Scripting
def get_script_and_prompts(hook_theme, is_gadget=False, is_long=False):
    words = "550 words" if is_long else "75 words (Strict 30 Seconds)"
    print(f"\n✅ AI Engine {words} ki script likh raha hai: {hook_theme}")
    
    prompt = f"""You are a professional YouTube creator. THEME: "{hook_theme}".
    WRITE A {words} HINDI SCRIPT.
    RULES:
    1. If Shorts: Finish entire story in exactly 30 seconds.
    2. If Long: Build deep mystery and detail for 8-10 minutes.
    Return ONLY JSON: {{"script": "...", "captions": ["8 items"], "prompts": ["8 items"], "amazon_term": "..."}}
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    
    res = requests.post(url, headers=headers, json=data, timeout=60)
    parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
    return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_search_term', '')

# (fetch_amazon_images_strict, fetch_ai_images, process_image_for_video remain same as your original)
def fetch_amazon_images_strict(query):
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
    files = []
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1080&height=1920&nologo=true"
        res = requests.get(url, timeout=30)
        fname = f"ai_{i}.jpg"
        with open(fname, "wb") as f: f.write(res.content)
        files.append(fname)
    return files

def create_human_voice(text, filename, is_long=False):
    rate = "+15%" if not is_long else "+5%"
    async def _gen():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate=rate)
        await communicate.save(filename)
    asyncio.run(_gen())

# 🟢 UPDATE: Viral Yellow Text (Big & Bold)
def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 500
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Black.ttf", 150) # Big font
    wrapped = textwrap.fill(text.upper(), width=12)
    # Bright Yellow with Thick Black Stroke
    draw.multiline_text((540, 250), wrapped, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", anchor="mm", align='center')
    fname = f"cap_{random.randint(1,9999)}.png"
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
        fixed = f"f_{i}.jpg"
        process_image_for_video(img_path, fixed)
        base = ImageClip(fixed).set_duration(dur_per_img).resize(lambda t: 1 + 0.05 * (t/dur_per_img))
        txt = create_centered_text_clip(captions[i], dur_per_img).set_position(('center', 0.65), relative=True)
        clips.append(CompositeVideoClip([base.set_position('center'), txt], size=(1080, 1920)))
    final = concatenate_videoclips(clips).set_audio(main_audio)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)

def upload_video(token, filename, title, desc, tags, cat):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=creds)
    youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": cat}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload(filename, resumable=True)).execute()

# 🟢 UPDATE: Long Video Agent at 10 PM IST
def run_channel_safely(channel_type):
    hour = time.localtime().tm_hour
    is_long = (hour == 22) # 10 PM IST
    try:
        theme = random.choice(GADGET_HOOKS if channel_type == "GADGETS" else MYSTIC_HOOKS)
        script, prompts, caps, term = get_script_and_prompts(theme, (channel_type=="GADGETS"), is_long)
        imgs = fetch_amazon_images_strict(term) if channel_type == "GADGETS" else fetch_ai_images(prompts)
        v_file = f"out_{channel_type}.mp4"
        create_human_voice(script, "t.mp3", is_long)
        make_video(imgs, caps, v_file, "t.mp3")
        token = TOKEN_GADGETS if channel_type == "GADGETS" else TOKEN_MYSTIC
        title = f"🤯 {theme} | Amazing AI" if is_long else f"🤯 {theme}! #shorts"
        upload_video(token, v_file, title, script, ["viral", "ai"], "28")
        print(f"✅ {channel_type} {'Long' if is_long else 'Short'} Live!")
    except Exception as e: print(f"🛑 Error: {e}")

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")
