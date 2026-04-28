import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

# --- बुनियादी सेटअप ---
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

# --- पर्यावरण चाबियाँ (Secrets) ---
GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
TELEGRAM_TOKEN = "8382528984:AAHLJYwQIvLN5xEHV9iSjvgI18b8pF4bWJ8"
CHAT_ID = "8285187691"

# --- रैंडम टॉपिक इंजन ---
GADGET_HOOKS = ["Mind-Blowing Gadgets 2026", "Secret Amazon Finds", "Survival Gear Hacks", "Smart Kitchen Tech", "Pocket Inventions"]
MYSTIC_HOOKS = ["Unsolved Space Mysteries", "Ancient Civilizations Secrets", "Parallel Universe Proof", "Dark Sea Monsters", "Digital Cryptids"]

def send_telegram(msg):
    try: requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    except: print(f"Telegram Fail: {msg}")

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return json.loads(match.group(0)) if match else None

def get_ai_content(theme, is_gadget=False, is_long=False):
    word_count = "500-600 words" if is_long else "70-75 words"
    prompt = f"""Write a {word_count} Hindi script for YouTube. Theme: {theme}. Style: Viral, shocking.
    Return ONLY JSON: {{"script": "...", "prompts": ["p1",..."p10"], "captions": ["c1",..."c10"], "search_term": "product name"}}"""
    
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9}
    
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return extract_json(res.json()['choices'][0]['message']['content'])

async def generate_voice(text, output_file):
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%")
    await communicate.save(output_file)

def create_viral_text(text, duration):
    img = Image.new('RGBA', (1080, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Black.ttf", 140)
    wrapped = textwrap.fill(text.upper(), width=12)
    # पीला टेक्स्ट और काला स्ट्रोक (Viral Look)
    draw.multiline_text((540, 200), wrapped, font=font, fill="#FFE81F", stroke_width=10, stroke_fill="black", anchor="mm", align='center')
    fname = f"cap_{random.randint(100,999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def process_video(image_urls, captions, audio_path, output_path):
    audio = AudioFileClip(audio_path)
    dur_per_clip = audio.duration / len(image_urls)
    clips = []
    
    for i, url in enumerate(image_urls):
        res = requests.get(url)
        with open(f"temp_{i}.jpg", "wb") as f: f.write(res.content)
        
        base = ImageClip(f"temp_{i}.jpg").set_duration(dur_per_clip).resize(height=1920)
        # ज़ूम इफ़ेक्ट
        base = base.resize(lambda t: 1 + 0.05 * t)
        
        txt = create_viral_text(captions[i], dur_per_clip).set_position(('center', 0.7), relative=True)
        clips.append(CompositeVideoClip([base.set_position('center'), txt]))
    
    final = concatenate_videoclips(clips).set_audio(audio)
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast")

def upload_to_youtube(token, file, title, desc):
    # (यहाँ अपलोडिंग का असली API कोड आएगा जो आपने पहले इस्तेमाल किया था)
    print(f"Uploading {file} to YouTube...")

def run_automation_cycle(channel_type):
    hour = time.localtime().tm_hour
    is_long = (hour == 22) # रात 10 बजे लॉन्ग वीडियो
    
    theme = random.choice(GADGET_HOOKS if channel_type == "GADGETS" else MYSTIC_HOOKS)
    content = get_ai_content(theme, is_gadget=(channel_type=="GADGETS"), is_long=is_long)
    
    if content:
        audio_file = f"voice_{channel_type}.mp3"
        asyncio.run(generate_voice(content['script'], audio_file))
        
        # इमेज सोर्सिंग (AI या Amazon)
        images = [f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1080&height=1920&nologo=true" for p in content['prompts']]
        
        video_file = f"final_{channel_type}.mp4"
        process_video(images, content['captions'], audio_file, video_file)
        
        token = TOKEN_GADGETS if channel_type == "GADGETS" else TOKEN_MYSTIC
        upload_to_youtube(token, video_file, content.get('topic', theme), content['script'])
        send_telegram(f"✅ {channel_type} Video Live!\nType: {'Long' if is_long else 'Short'}\nTopic: {theme}")

if __name__ == "__main__":
    try:
        run_automation_cycle("GADGETS")
        time.sleep(30)
        run_automation_cycle("MYSTIC")
    except Exception as e:
        send_telegram(f"🛑 Error: {str(e)}")
