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

from PIL import Image, ImageDraw, ImageFont, ImageFilter
if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 Security aur Premium Setup chalu ho raha hai...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

# 100% Pukka Font Downloader
if not os.path.exists("Roboto-Black.ttf"):
    os.system("wget -qO Roboto-Black.ttf https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Black.ttf")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# 🔑 आपके 5 चैनलों के टोकन (GitHub Secrets के अनुसार)
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
TOKEN_EMPIRE = os.environ.get("YOUTUBE_TOKEN_EMPIRE")
TOKEN_GADGET = os.environ.get("YOUTUBE_TOKEN_GADGET")
TOKEN_HEALTH = os.environ.get("YOUTUBE_TOKEN_HEALTH")
TOKEN_ZEROTOUCH = os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

# 📝 हर चैनल के लिए आपके पुराने स्टाइल के हुक्स
GADGET_HOOKS = ["Amazon's Hidden Tech", "Crazy Gadgets Under 1000", "Must-Have Smart Home Items", "Secret Car Hacks", "Genius Kitchen Tools"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Deep Sea Monsters", "Unsolved Crimes of History", "Lost Ancient Cities", "Creepy Government Secrets"]
EMPIRE_HOOKS = ["Secret Habits of Billionaires", "How to Build a Business Empire", "Hidden Wealth Rules", "Money Making AI Hacks"]
HEALTH_HOOKS = ["Ayurveda Secrets for Longevity", "Hidden Benefits of Indian Spices", "Human Body Unknown Facts", "Natural Remedies That Work"]
ZEROTOUCH_HOOKS = ["Mind Blowing AI Tools", "Future of Artificial Intelligence", "Robots Taking Over Jobs", "Secret Tech Websites"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, is_gadget=False):
    print(f"\n✅ AI Engine 40+ second ki dumdaar script likh raha hai: {hook_theme}")
    
    if is_gadget:
        prompt = f"""You are a top Amazon affiliate marketer. THEME: "{hook_theme}".
        WRITE A 90-100 WORD HINDI SCRIPT.
        RULES:
        1. NO INTRODUCTIONS. START DIRECTLY WITH A SHOCKING 3-SECOND HOOK!
        2. Describe a frustrating daily problem.
        3. Reveal the product as the ultimate mind-blowing solution.
        4. Create massive URGENCY at the end.
        5. END EXACTLY WITH: 'यह शानदार गैजेट अभी आउट ऑफ़ स्टॉक होने से पहले चैनल के बायो से खरीदें।'
        
        CAPTIONS: 8 short punchy English captions.
        PROMPTS: 8 simple image generation prompts.
        AMAZON SEARCH TERM: Simple 2-3 word real product name.
        """
    else:
        prompt = f"""You are a dark, mysterious storyteller. THEME: "{hook_theme}".
        WRITE A 90-100 WORD HINDI SCRIPT.
        RULES:
        1. NO INTRODUCTIONS. START DIRECTLY WITH A CREEPY/SHOCKING HOOK!
        2. Build extreme suspense and mystery throughout.
        3. Reveal a shocking fact or theory.
        4. DO NOT TALK ABOUT BUYING, SELLING, OR STOCK.
        5. END EXACTLY WITH: 'ऐसे ही खूंखार रहस्यों के लिए चैनल को सब्सक्राइब करें और लिंक बायो में देखें।'
        
        CAPTIONS: 8 short punchy English captions.
        PROMPTS: 8 creepy image generation prompts.
        AMAZON SEARCH TERM: Leave empty ("").
        """

    prompt += """
    Return ONLY valid JSON:
    {
      "topic": "viral topic name",
      "script": "Hindi script here (min 90 words)...",
      "captions": ["SHOCKING", "DAILY PROBLEM", "THE SOLUTION", "WAIT FOR IT", "AMAZING TECH", "MIND BLOWN", "STOCK ENDING", "LINK IN BIO"],
      "prompts": ["Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6", "Image 7", "Image 8"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                if parsed.get('script'):
                    print("🎯 Script Ready!")
                    return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_search_term', '')
        except: time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

def fetch_amazon_images_strict(query):
    print(f"🛒 Amazon se '{query}' ki photos nikali ja rahi hain...")
    if not RAPIDAPI_KEY: raise Exception("⚠️ RAPIDAPI_KEY Missing!")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    image_files = []
    try:
        response = requests.get(url, headers=headers, params={"query": query, "page": "1", "country": "IN", "sort_by": "RELEVANCE"}, timeout=40)
        if response.status_code == 200:
            for i, prod in enumerate(response.json().get("data", {}).get("products", [])):
                if len(image_files) >= 8: break
                photo_url = prod.get("product_photo")
                if photo_url:
                    img_res = requests.get(photo_url, timeout=15)
                    if img_res.status_code == 200:
                        fname = f"amazon_img_{i}.jpg"
                        with open(fname, "wb") as f: f.write(img_res.content)
                        image_files.append(fname)
            if len(image_files) >= 4: return image_files
            raise Exception("⚠️ Photos kam hain.")
        raise Exception("⚠️ API Error")
    except Exception as e: raise Exception(f"Amazon Fail: {e}")

def fetch_ai_images(prompts):
    image_files, seed = [], random.randint(1000, 99999)
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + ', highly detailed, 8k')}?width=1080&height=1920&nologo=true&seed={seed+i}"
        fname = f"ai_scene_{i}.jpg"
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

def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 800
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try: font = ImageFont.truetype("Roboto-Black.ttf", 130)
    except: font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text.upper(), width=15) 
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped_text, font=font)
        
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=8, stroke_fill="black", align='center')
    
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
    print(f"✅ Professional Video Render ho raha hai: {final_vid}")
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

def run_channel_safely(channel_name, token, hook_list, is_gadget=False):
    if not token:
        print(f"⚠️ {channel_name} ka token nahi mila. Isko skip kar rahe hain.")
        return False
        
    print(f"\n==============================================")
    print(f"🚀 STARTING CHANNEL: {channel_name}")
    print(f"==============================================")
    
    for attempt in range(5):
        try:
            hook = random.choice(hook_list)
            script, prompts, captions, amazon_term = get_script_and_prompts(hook, is_gadget=is_gadget)
            
            # File names unique rakhne ke liye
            prefix = channel_name.replace(" ", "_").lower()
            voice_file = f"voice_{prefix}.mp3"
            video_file = f"final_{prefix}.mp4"

            if is_gadget:
                image_files = fetch_amazon_images_strict(amazon_term) 
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                desc = f"🔥 👉 यह शानदार गैजेट आउट ऑफ़ स्टॉक होने से पहले चैनल के Bio से खरीदें!\n🔍 अमेज़न पर सर्च करें: {amazon_term}\n\n{script}"
                title = f"🤯 Best {amazon_term}! #shorts"
                upload_video(token, video_file, title, desc, ["shorts", "gadgets", "amazon finds", "tech"], "28")
            else:
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                desc = f"🔥 👉 ऐसे ही खूंखार रहस्यों और जानकारी के लिए लिंक चैनल के Bio में है!\n\n{script}"
                title = f"🤯 Secret They Hid From You! #shorts"
                upload_video(token, video_file, title, desc, ["shorts", "mystery", "creepy", "facts"], "28")
                
            print(f"✅ {channel_name} Video Live!")
            return True 
                
        except Exception as e: 
            print(f"🛑 Error on {channel_name}: {e}. Machine dobara koshish kar rahi hai...")
            time.sleep(10) 
            
    print(f"❌ {channel_name} fail ho gaya.")
    return False

if __name__ == "__main__":
    # 5 चैनल की लिस्ट (नाम, टोकन, हुक्स, क्या ये गैजेट चैनल है?)
    channels = [
        ("GIRISH AI GADGET", TOKEN_GADGET, GADGET_HOOKS, True),
        ("MYSTERY CHANNEL", TOKEN_MYSTIC, MYSTIC_HOOKS, False),
        ("AI AUTO PILOT EMPIRE", TOKEN_EMPIRE, EMPIRE_HOOKS, False),
        ("HEALTH AND AYURVEDA", TOKEN_HEALTH, HEALTH_HOOKS, False),
        ("ZEROTOUCH AI CREATOR", TOKEN_ZEROTOUCH, ZEROTOUCH_HOOKS, False)
    ]
    
    # एक-एक करके 5 चैनल चलेंगे
    for name, token, hooks, is_gadget in channels:
        run_channel_safely(name, token, hooks, is_gadget)
        time.sleep(15) # हर चैनल के बीच 15 सेकंड का रेस्ट ताकि कोई API ब्लॉक न हो
        
    print("\n✅ सभी 5 चैनलों का काम खत्म हो गया है बॉस!")
