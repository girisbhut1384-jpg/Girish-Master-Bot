import os, sys, requests, asyncio, edge_tts, time, urllib.parse, json, random, re, textwrap
from datetime import datetime, timedelta

# --- PIL & MOVIEPY SETUP ---
from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, CompositeAudioClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import urllib.request

print("🛡️ बैच 2 (ULTIMATE V2): Crash-Proof Smart Video Engine")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")

# --- 1. फोंट डाउनलोड ---
font_path = "NotoSansDevanagari-Bold.ttf"
if not os.path.exists(font_path):
    print("📥 शानदार हिंदी फोंट डाउनलोड हो रहा है...")
    try: urllib.request.urlretrieve("https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf", font_path)
    except: pass

# --- 2. API KEYS & SECRETS ---
GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-7e17ufdmt7r67urc9krua7t69vps6h57.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

AMAZON_TAG = "girishbhut07-21"
GUMROAD_LINK = "https://your_store.gumroad.com/l/ai-setup" # यहाँ अपना असली गमरोड लिंक डालें

# --- 3. 100% परफेक्ट चैनल सेटअप ---
CHANNELS_CONFIG = {
    "GADGET_PRO": {"token": os.environ.get("TOKEN_GADGET"), "category": "28", "tags": ["smart gadgets", "tech", "amazon"], "style": "high tech product photography, neon lights, glowing gadgets, 8k, hyper-realistic", "hooks": ["कमाल के स्मार्ट गैजेट्स", "फोन के लिए बेस्ट गैजेट"], "link_type": "AMAZON"},
    "AI_AUTOMATION_HUB": {"token": os.environ.get("TOKEN_AI1"), "category": "27", "tags": ["ai automation", "make money"], "style": "futuristic cyberpunk, money raining, hacking screen, 8k, hyper-realistic", "hooks": ["AI से घर बैठे पैसे कमाएं", "यूट्यूब ऑटोमेशन का सच"], "link_type": "GUMROAD"},
    "CREATOR_AI_SETUP": {"token": os.environ.get("TOKEN_AI2"), "category": "27", "tags": ["youtube growth", "ai tools"], "style": "professional studio setup, futuristic lighting, 8k, hyper-realistic", "hooks": ["बिना चेहरा दिखाए यूट्यूब से कमाई", "वायरल AI वीडियो कैसे बनाएं"], "link_type": "GUMROAD"},
    "FUTURE_TECH_AI": {"token": os.environ.get("TOKEN_AI3"), "category": "27", "tags": ["future tech", "ai news"], "style": "sci-fi, artificial intelligence brain, global network, 8k, hyper-realistic", "hooks": ["भविष्य के खतरनाक AI टूल्स", "AI जो दुनिया बदल देगा"], "link_type": "GUMROAD"},
    "EXTRA_CHANNEL": {"token": os.environ.get("TOKEN_EXTRA"), "category": "27", "tags": ["viral", "trending"], "style": "cinematic lighting, ultra detailed, 8k", "hooks": ["दुनिया का सबसे अद्भुत रहस्य"], "link_type": "NONE"}
}

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script(hook):
    print(f"\n📝 '{hook}' पर शानदार स्क्रिप्ट लिखी जा रही है...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    prompt = f"""You are a master YouTube Shorts scriptwriter. THEME: "{hook}"
    RULES: 1. Shocking hook. 2. "text" in pure Devanagari Hindi. 3. "prompt" in detailed English. 4. "caption" 2-4 Hindi words. 5. Total 5 scenes.
    JSON FORMAT: {{"title": "Viral Clickbait Hindi Title", "scenes": [{{"text": "हिंदी स्टोरी...", "caption": "छोटा कैप्शन", "prompt": "English visual prompt..."}}]}}"""
    
    for _ in range(5):
        try:
            res = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}, timeout=60)
            if res.status_code == 200:
                parsed = json.loads(extract_json_safely(res.json()['choices'][0]['message']['content']))
                if parsed.get('scenes'): return parsed
            time.sleep(5)
        except: time.sleep(5)
    raise Exception("❌ AI Script Failed")

def get_images(scenes, style):
    print("📸 स्मार्ट क्वालिटी चेक के साथ 8K इमेजेज बन रही हैं...")
    imgs = []
    for i, s in enumerate(scenes):
        success = False
        for attempt in range(5): 
            try:
                seed = random.randint(10000, 99999)
                # अगर 3 बार में फोटो न बने, तो स्टाइल को थोड़ा हल्का कर देता है ताकि एरर न आए
                current_style = style if attempt < 3 else "cinematic, high quality, 8k"
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(s['prompt'] + ', ' + current_style)}?width=1080&height=1920&nologo=true&seed={seed}"
                
                r = requests.get(url, timeout=60)
                # 50000 की जगह 15000 किया गया है ताकि अच्छी डार्क इमेजेज रिजेक्ट न हों
                if r.status_code == 200 and len(r.content) > 15000: 
                    fname = f"img_{i}.jpg"
                    with open(fname, "wb") as f: f.write(r.content)
                    
                    # 🚨 असली क्वालिटी चेक: पाइथन खुद फोटो खोलकर देखेगा कि पिक्सल फटे तो नहीं हैं
                    Image.open(fname).verify() 
                    imgs.append(fname)
                    success = True
                    break
            except Exception as e:
                time.sleep(5)
        
        if not success:
            print(f"⚠️ दृश्य {i} के लिए इमेज नहीं बन पाई।")
            
    if len(imgs) != len(scenes): raise Exception("❌ Image Quality Check Failed")
    return imgs

def create_voice(text):
    print("🎙️ एकदम साफ़ आवाज़ जनरेट हो रही है...")
    async def _generate():
        await edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+0%", volume="+50%").save("v.mp3")
    asyncio.run(_generate())

def download_bgm():
    bgm_file = "epic_bgm.mp3"
    if not os.path.exists(bgm_file):
        try:
            r = requests.get("https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3", headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            if r.status_code == 200:
                with open(bgm_file, "wb") as f: f.write(r.content)
        except: pass
    return bgm_file if os.path.exists(bgm_file) else None

def create_text_clip(caption_text, duration):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(font_path, 160)
    except: font = ImageFont.load_default()
    
    wrapped = textwrap.fill(caption_text, width=12)
    try: bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align='center')
    except: return ImageClip(img).set_duration(duration)
    
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x, y = (1080 - tw) // 2, int(1920 * 0.65)
    
    draw.multiline_text((x+5, y+5), wrapped, font=font, fill="black", align='center')
    draw.multiline_text((x, y), wrapped, font=font, fill="#FFE81F", stroke_width=8, stroke_fill="black", align='center')
    
    fname = f"txt_{random.randint(1,99999)}.png"
    img.save(fname)
    return ImageClip(fname).set_duration(duration)

def assemble_and_upload(imgs, scenes, token, title, cfg):
    print("🎬 वीडियो एडिटिंग और रेंडरिंग चालू...")
    create_voice(" ".join([s['text'] for s in scenes]))
    voice_audio = AudioFileClip("v.mp3")
    
    bgm_path = download_bgm()
    if bgm_path:
        bgm_audio = AudioFileClip(bgm_path).volumex(0.08).subclip(0, voice_audio.duration)
        final_audio = CompositeAudioClip([voice_audio, bgm_audio])
    else:
        final_audio = voice_audio

    dur = voice_audio.duration / len(imgs)
    clips = []
    for i, img_path in enumerate(imgs):
        img = Image.open(img_path).convert("RGB")
        
        bg = img.resize((1080, 1920), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40))
        ratio = 1080 / img.width
        new_h = int(img.height * ratio)
        if new_h > 1920:
            ratio = 1920 / img.height; new_w = int(img.width * ratio)
            fg = img.resize((new_w, 1920), Image.Resampling.LANCZOS)
            bg.paste(fg, ((1080 - new_w) // 2, 0))
        else:
            fg = img.resize((1080, new_h), Image.Resampling.LANCZOS)
            bg.paste(fg, (0, (1920 - new_h) // 2))
            
        proc_name = f"proc_{i}.jpg"
        bg.save(proc_name)
        
        base = ImageClip(proc_name).set_duration(dur).set_position('center')
        zoom = base.resize(lambda t: 1 + 0.04 * (t/dur)) 
        txt = create_text_clip(scenes[i].get('caption', ''), dur).set_position(('center', 'center'))
        clips.append(CompositeVideoClip([zoom, txt]))
    
    final = concatenate_videoclips(clips, method="compose").set_audio(final_audio)
    final.write_videofile("out.mp4", fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, logger=None)
    
    full_desc = " ".join([s['text'] for s in scenes]) + "\n\nऐसी ही अद्भुत जानकारी के लिए चैनल को अभी सब्सक्राइब करें।"
    if cfg['link_type'] == "AMAZON":
        full_desc += f"\n\n🔥 👉 शानदार गैजेट यहाँ से खरीदें!\n🔗 लिंक: https://www.amazon.in/?tag={AMAZON_TAG}"
    elif cfg['link_type'] == "GUMROAD":
        full_desc += f"\n\n🤖 हमारा 100% ऑटोमेटेड AI यूट्यूब सेटअप आज ही खरीदें!\n👉 यहाँ क्लिक करें: {GUMROAD_LINK}"
    
    print(f"🚀 YouTube पर अपलोड हो रहा है...")
    creds = Credentials(token=None, refresh_token=token, token_uri="https://oauth2.googleapis.com/token", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    build("youtube", "v3", credentials=creds).videos().insert(
        part="snippet,status", body={"snippet": {"title": f"{title} #shorts", "description": full_desc, "categoryId": cfg['category'], "tags": cfg['tags']}, "status": {"privacyStatus": "public"}},
        media_body=MediaFileUpload("out.mp4", chunksize=-1, resumable=True)
    ).execute()
    print("✅ सफलता! वीडियो लाइव हो गया है।\n")
    
    voice_audio.close(); final.close()
    for f in ["v.mp3", "out.mp4"] + imgs + [f"proc_{i}.jpg" for i in range(len(imgs))]:
        if os.path.exists(f): os.remove(f)

def run():
    channels = list(CHANNELS_CONFIG.keys())
    random.shuffle(channels)
    for ch in channels:
        cfg = CHANNELS_CONFIG[ch]
        try:
            print(f"⚙️ Starting Automation for: {ch}")
            data = get_script(random.choice(cfg['hooks']))
            imgs = get_images(data['scenes'], cfg['style'])
            assemble_and_upload(imgs, data['scenes'], cfg['token'], data['title'], cfg)
            time.sleep(10)
        except Exception as e: print(f"🛑 Error in {ch}: {e}")

if __name__ == "__main__": run()
