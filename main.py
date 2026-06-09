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
if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from googleapiclient.errors import HttpError 

print("🔓 Security aur Premium Multi-Engine Setup chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-ndfvqmbb0p7ffa1r1cg6bmmuimim98n6.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET_JSON") or os.environ.get("GOOGLE_CLIENT_SECRET")

TOKEN_GADGET = os.environ.get("YOUTUBE_TOKEN_GADGET")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
TOKEN_EMPIRE = os.environ.get("YOUTUBE_TOKEN_EMPIRE")
TOKEN_WEALTH = os.environ.get("YOUTUBE_TOKEN_WEALTH")
TOKEN_ZEROTOUCH = os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

GADGET_HOOKS = ["Hidden Amazon Tech", "Must-Have Smart Gadgets", "Genius Kitchen Tools", "Car Gadgets You Need", "Cool Room Tech"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Unsolved Psychological Mysteries", "Ghost Towns of India", "Time Travel Proof", "Dark Web Secrets", "Creepy Historical Events"]
AI_SELL_HOOKS = ["Free AI Tools 2026", "AI Video Editing Hacks", "Secret Websites Nobody Knows", "Smart Work vs Hard Work", "AI Tools for Students", "Time Saving Tech"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def fetch_script_with_fallback(prompt):
    models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it", "llama3-8b-8192"]
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    for model in models:
        try:
            data = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.9}
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                if parsed.get('script'):
                    return parsed
        except:
            continue
    raise Exception("🚨 All 4 AI Text Models Failed!")

def get_script_and_prompts(hook_theme, category):
    print(f"\n✅ AI Engine Master Prompt ke sath Content likh raha hai: {hook_theme}")
    
    # 🟢 वायरल शॉर्ट्स के लिए एकदम परफेक्ट टाइमिंग (50-55s) और स्ट्रिक्ट नियम
    master_system_rules = """
    STRICT RULES TO FOLLOW FOR VIRAL SHORTS:
    1. Length & Format: CRITICAL RULE: Write EXACTLY 10 to 12 SHORT sentences in Hindi. The total word count MUST be exactly between 120 and 130 words. This ensures the voiceover spans exactly 50 to 55 seconds. DO NOT write short scripts under 100 words.
    2. The Hook (FATAL RULE): NEVER start with "क्या आप जानते हैं" or "क्या आपको पता है". Start directly with a bold, shocking claim like "99% लोग यह सीक्रेट नहीं जानते..." or "यह टूल आपकी जिंदगी बदल देगा...".
    3. Title Generation: Create a unique, highly clickable title (under 50 characters). DO NOT use the "🤯" emoji at the start. Use an emoji at the END.
    4. Call to Action (CTA): END EXACTLY WITH: 'चैनल को अभी सब्सक्राइब करें।' DO NOT say 'Link in description'.
    """
    
    if category == "GADGET":
        prompt = f"""You are an expert YouTube Shorts Scriptwriter. THEME: "{hook_theme}".
        {master_system_rules}
        NICHE: Tech Gadgets.
        CRITICAL RULE: The product MUST BE a common real-world item easily found on Amazon India.
        
        Generate a UNIQUE 2-line SEO DESCRIPTION. Generate 3 UNIQUE TAGS.
        CAPTIONS: 6 short English captions. PROMPTS: 6 simple image generation prompts.
        AMAZON SEARCH TERM: Simple 2-3 word real English product name.
        """
    elif category == "AI_SELL":
        prompt = f"""You are an expert YouTube Shorts Scriptwriter. THEME: "{hook_theme}".
        {master_system_rules}
        NICHE: AI Tools & Automation Value.
        CRITICAL RULE FOR AI: You MUST say the REAL NAME of a specific tool (e.g., ChatGPT, Midjourney, Canva, 11Labs) in the very first sentence. Stop talking generically about "AI Tools".
        DO NOT SELL ANYTHING IN THE SCRIPT. Provide pure value.
        
        Generate a UNIQUE 2-line SEO DESCRIPTION. Generate 3 UNIQUE TAGS.
        CAPTIONS: 6 short English captions. PROMPTS: 6 highly detailed image prompts.
        AMAZON SEARCH TERM: Leave empty ("").
        """
    else: 
        prompt = f"""You are a dark, mysterious storyteller. THEME: "{hook_theme}".
        {master_system_rules}
        NICHE: Creepy Mysteries. Build extreme suspense with a complete story arc. Give creepy details. Remember word count must be 120-130 words.
        
        Generate a UNIQUE 2-line SEO DESCRIPTION. Generate 3 UNIQUE TAGS.
        CAPTIONS: 6 short English captions. PROMPTS: 6 distinct dark/creepy image prompts.
        AMAZON SEARCH TERM: Leave empty ("").
        """

    prompt += """
    Return ONLY valid JSON in this exact format:
    {
      "title": "Unique Viral Title Here 🔥",
      "description": "Unique 2-3 lines description here...",
      "tags": ["tag1", "tag2", "tag3"],
      "script": "Hindi script here...",
      "captions": ["CAP1", "CAP2", "CAP3", "CAP4", "CAP5", "CAP6"],
      "prompts": ["Prompt1", "Prompt2", "Prompt3", "Prompt4", "Prompt5", "Prompt6"],
      "amazon_search_term": "Product name"
    }
    """
    
    parsed = fetch_script_with_fallback(prompt)
    print("🎯 Script, Title, Description aur Tags Ready (120-130 words for 55 sec)!")
    return (
        parsed['script'].replace("*", ""), 
        parsed['prompts'][:6], 
        parsed['captions'][:6], 
        parsed.get('amazon_search_term', 'Gadget'), 
        parsed.get('title', 'Viral Shorts 🔥'),
        parsed.get('description', 'Watch this amazing video!'),
        parsed.get('tags', ['shorts', 'viral', 'trending'])
    )

def fetch_amazon_images_strict(query):
    clean_query = re.sub(r'[^a-zA-Z0-9 ]', '', str(query)).strip()
    print(f"🛒 Amazon se '{clean_query}' ki photos nikali ja rahi hain...")
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
                    try:
                        img_res = requests.get(photo_url, timeout=10)
                        if img_res.status_code == 200:
                            fname = f"amazon_img_{i}.jpg"
                            with open(fname, "wb") as f: f.write(img_res.content)
                            image_files.append(fname)
                    except: continue
        if len(image_files) >= 3: return image_files
    except: pass
    
    print("⚠️ Amazon API failed or zero images. Fallback to AI generation...")
    return fetch_ai_images_with_fallback([f"High quality product photo of {clean_query}, studio lighting, 4k, realistic"] * 6)

def fetch_ai_images_with_fallback(prompts):
    image_files = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for i, p in enumerate(prompts):
        seed = random.randint(100000, 999999) 
        encoded_p = urllib.parse.quote(p + ", highly detailed, 8k, cinematic")
        
        urls = [
            f"https://image.pollinations.ai/prompt/{encoded_p}?seed={seed}&model=flux&width=1080&height=1920&nologo=true",
            f"https://image.pollinations.ai/prompt/{encoded_p}?seed={seed}&model=turbo&width=1080&height=1920&nologo=true",
            f"https://image.pollinations.ai/prompt/{encoded_p}?seed={seed}&width=1080&height=1920&nologo=true"
        ]
        
        for url in urls:
            try:
                res = requests.get(url, headers=headers, timeout=15) 
                if res.status_code == 200 and len(res.content) > 10000:
                    fname = f"ai_scene_{i}.jpg"
                    with open(fname, "wb") as f: f.write(res.content)
                    image_files.append(fname)
                    break
            except:
                continue
                
    # 🟢 QUALITY CONTROL: NO DARK SCREENS ALLOWED
    if len(image_files) < 3:
        raise Exception("🚨 APIs ne photo nahi di. Kachra video nahi banayenge! Channel skipped.")
        
    return image_files

def create_human_voice(text, filename):
    async def _generate():
        for _ in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-5%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("Voice Fail")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

def create_centered_text_clip(text, duration):
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
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
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

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ Professional Video Render ho raha hai...")
    if not image_files or len(image_files) < 3: 
        raise Exception("System Error: Not enough images available. Stopping render.") 
    
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        fixed_img_path = f"fixed_{i}.jpg"
        process_image_for_video(img_path, fixed_img_path)
        base_clip = ImageClip(fixed_img_path)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.04 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, time_per_image)
                txt_clip = txt_clip.set_position(('center', 0.65), relative=True) 
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = zoomed_clip
        else: final_clip = zoomed_clip
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

def upload_video(token, filename, title, description, tags, category):
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
    request.execute()

def run_channel_safely(channel_name, token, hook_list, category="MYSTERY"):
    if not token:
        print(f"⚠️ {channel_name} ka token nahi mila. Isko skip kar rahe hain.")
        return False
        
    print(f"\n==============================================")
    print(f"🚀 STARTING CHANNEL: {channel_name}")
    print(f"==============================================")
    
    for attempt in range(3):
        try:
            hook = random.choice(hook_list)
            script, prompts, captions, amazon_term, dyn_title, dyn_desc, dyn_tags = get_script_and_prompts(hook, category)
            
            prefix = channel_name.replace(" ", "_").lower()
            voice_file = f"voice_{prefix}.mp3"
            video_file = f"final_{prefix}.mp4"

            if category == "GADGET":
                image_files = fetch_amazon_images_strict(amazon_term) 
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                clean_term = re.sub(r'[^a-zA-Z0-9 ]', '', str(amazon_term)).strip()
                amz_link = f"https://www.amazon.in/s?k={urllib.parse.quote(clean_term)}&tag=girishbhut07-21"
                final_desc = f"{dyn_desc}\n\n🔥 👉 यह शानदार गैजेट यहाँ से खरीदें:\n🔗 लिंक: {amz_link}\n\n📝 Script:\n{script}"
                
                upload_video(token, video_file, dyn_title, final_desc, dyn_tags, "28")
                print(f"✅ GADGETS Video Live! Title: {dyn_title}")
                return True 
                
            elif category == "AI_SELL":
                image_files = fetch_ai_images_with_fallback(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                gumroad_link = "https://girisbhut.gumroad.com/l/ajhzk"
                final_desc = f"{dyn_desc}\n\n🚀 👉 मेरा यह पूरा 100% ऑटोमैटिक YouTube Setup अभी खरीदें:\n🔗 यहाँ क्लिक करें: {gumroad_link}\n\n📝 Script:\n{script}"
                
                upload_video(token, video_file, dyn_title, final_desc, dyn_tags, "28")
                print(f"✅ AI SELL Video Live (Passive Marketing)! Title: {dyn_title}")
                return True 

            else: 
                image_files = fetch_ai_images_with_fallback(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                final_desc = f"{dyn_desc}\n\n🔥 👉 ऐसे ही खूंखार रहस्यों के लिए सब्सक्राइब करें!\n\n📝 Script:\n{script}"
                
                upload_video(token, video_file, dyn_title, final_desc, dyn_tags, "28")
                print(f"✅ {channel_name} Video Live! Title: {dyn_title}")
                return True 
                
        except HttpError as e:
            error_content = str(e).lower()
            if "quota" in error_content or "ratelimit" in error_content or "429" in error_content:
                print(f"🚨 YOUTUBE QUOTA FULL for {channel_name}!")
                break 
            else:
                time.sleep(10)
        except Exception as e: 
            print(f"🛑 Error on {channel_name}: {e}. Retrying with fallback systems...")
            time.sleep(10) 
            
    print(f"❌ {channel_name} fail ho gaya. Garbage upload nahi kiya gaya.")
    return False

if __name__ == "__main__":
    channels = [
        ("GIRISH AI GADGET", TOKEN_GADGET, GADGET_HOOKS, "GADGET"),
        ("MYSTERY CHANNEL", TOKEN_MYSTIC, MYSTIC_HOOKS, "MYSTERY"),
        ("FACELESS AI WEALTH", TOKEN_WEALTH, AI_SELL_HOOKS, "AI_SELL"),             
        ("AI AUTO PILOT EMPIRE", TOKEN_EMPIRE, AI_SELL_HOOKS, "AI_SELL"),         
        ("ZEROTOUCH AI CREATOR", TOKEN_ZEROTOUCH, AI_SELL_HOOKS, "AI_SELL")       
    ]
    
    for name, token, hooks, cat in channels:
        run_channel_safely(name, token, hooks, cat)
        time.sleep(15)
        
    print("\n✅ सभी 5 चैनलों का काम बिना क्रैश हुए खत्म हो गया है बॉस!")
