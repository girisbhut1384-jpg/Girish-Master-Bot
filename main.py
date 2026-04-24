import os
import sys
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
import glob
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 सिक्योरिटी दीवार और प्रीमियम सेटअप चालू हो रहा है...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") 
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

if not GROQ_KEY:
    print("❌ एरर: GROQ_API_KEY नहीं मिली!")
    sys.exit(1)

GADGET_HOOKS = ["Amazon's Hidden Tech", "Crazy Gadgets Under 1000", "Must-Have Smart Home Items", "Secret Car Hacks", "Genius Kitchen Tools", "Futuristic Office Tech"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Deep Sea Monsters", "Unsolved Crimes of History", "Lost Ancient Cities", "Creepy Government Secrets", "Time Travel Evidences"]

def extract_json_safely(raw_text):
    raw_text = str(raw_text).strip()
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if match: return match.group(0)
    return "{}"

# 🟢 प्रीमियम फॉन्ट (Huge Size)
def get_premium_font():
    font_path = "Montserrat-Black.ttf"
    if not os.path.exists(font_path):
        try:
            r = requests.get("https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Black.ttf")
            with open(font_path, "wb") as f: f.write(r.content)
        except: return ImageFont.load_default()
    return font_path

def get_script_and_prompts(hook_theme, is_gadget=False):
    print(f"\n✅ 70B AI इंजन दमदार 35+ सेकंड की 'Sales' स्क्रिप्ट लिख रहा है: {hook_theme}")
    
    prompt = f"""You are a master YouTube Shorts director and affiliate marketer. 
    THEME: "{hook_theme}".
    
    CRITICAL INSTRUCTION: Your script MUST be EXACTLY 90 to 110 words long to ensure the video is over 35 seconds. DO NOT write short scripts.

    REQUIREMENTS:
    1. SCRIPT (Voiceover): Write an aggressive, high-energy HINDI script. 
       - 0-5s: Start with a MIND-BLOWING 3-second hook.
       - 5-15s: Talk about a major daily problem people face.
       - 15-25s: Introduce the product/mystery as the ultimate mind-blowing solution.
       - 25-35s: Build extreme urgency (e.g., "स्टॉक खत्म हो रहा है!").
    2. CAPTIONS: Write 8 short, punchy captions in ENGLISH ALPHABETS (MAX 2-3 words per caption).
    3. PROMPTS (English): 8 image generation prompts.
    """

    if is_gadget:
        prompt += """
    - SCRIPT ENDING: 'यह शानदार गैजेट अभी आउट ऑफ़ स्टॉक होने से पहले चैनल के बायो से खरीदें।'
    - AMAZON SEARCH TERM: Simple 2-3 word real product name.
        """
    else:
        prompt += """
    - SCRIPT ENDING: 'ऐसे ही खूंखार रहस्यों के लिए लिंक बायो में है।'
        """

    prompt += """
    Return ONLY valid JSON format exactly like this:
    {
      "topic": "viral topic name",
      "script": "Long 90+ words Hindi script here...",
      "captions": ["SHOCKING!", "DAILY PROBLEM", "THE SOLUTION", "WAIT FOR IT", "AMAZING TECH", "MIND BLOWN", "STOCK ENDING", "LINK IN BIO"],
      "prompts": ["Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6", "Image 7", "Image 8"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Output only JSON."}, {"role": "user", "content": prompt}], "temperature": 0.7}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                clean_json = extract_json_safely(result['choices'][0]['message']['content'])
                parsed = json.loads(clean_json)
                if parsed.get('script'):
                    print("🎯 स्क्रिप्ट तैयार!")
                    return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_search_term', '')
        except: time.sleep(2)
    raise Exception("🚨 70B मॉडल फेल!")

def fetch_amazon_images_strict(query):
    print(f"🛒 अमेज़न से '{query}' की फोटो निकाली जा रही हैं...")
    if not RAPIDAPI_KEY: raise Exception("⚠️ RAPIDAPI_KEY नहीं मिली!")
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
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
                        filename = f"amazon_img_{i}.jpg"
                        with open(filename, "wb") as f: f.write(img_res.content)
                        image_files.append(filename)
            if len(image_files) >= 4: return image_files
            else: raise Exception("⚠️ फोटो कम हैं।")
        else: raise Exception("⚠️ API एरर")
    except Exception as e: raise Exception(f"अमेज़न फेल: {e}")

def fetch_ai_images(prompts):
    image_files = []
    seed = random.randint(1000, 99999) 
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p + ", highly detailed, cinematic, 8k")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        for attempt in range(3): 
            try:
                res = requests.get(url, headers=headers, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: f.write(res.content)
                    image_files.append(filename)
                    break
            except: time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    async def _generate():
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%", pitch="+0Hz") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("वॉइस फेल")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 विशाल कैप्शंस (HUGE TEXT)
def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 600
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = get_premium_font()
    
    try: font = ImageFont.truetype(font_path, 150) # 👈 साइज़ 80 से बढ़ाकर 150 कर दिया है!
    except: font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text.upper(), width=14) 
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_width, text_height = draw.textsize(wrapped_text, font=font)
        
    x, y = (canvas_w - text_width) // 2, (canvas_h - text_height) // 2
    
    # मोटी काली आउटलाइन के साथ 100% साफ पीला टेक्स्ट
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=12, stroke_fill="black", align='center')
    
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ प्रोफेशनल वीडियो रेंडर हो रहा है...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        # 🟢 बीमारी 1 का इलाज: फोटो को बिना काटे फिट करना (Studio Fit)
        img = Image.open(img_path).convert("RGB")
        bg = Image.new("RGB", (1080, 1920), (20, 20, 20)) # डार्क प्रीमियम बैकग्राउंड
        
        # फोटो को 1080 की चौड़ाई में फिट करना ताकि प्रोडक्ट पूरा दिखे
        resampling_filter = getattr(Image, 'Resampling', Image).LANCZOS
        img.thumbnail((1080, 1400), resampling_filter) 
        bg.paste(img, ((1080 - img.width) // 2, (1920 - img.height) // 2))
        
        fixed_img_path = f"fixed_img_{i}.jpg"
        bg.save(fixed_img_path)
        
        base_clip = ImageClip(fixed_img_path)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.04 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, time_per_image)
                txt_clip = txt_clip.set_position(('center', 0.60), relative=True) # गोल्डन ज़ोन में
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

def run_channel_safely(channel_type):
    for attempt in range(5):
        try:
            if channel_type == "GADGETS":
                hook = random.choice(GADGET_HOOKS)
                script, prompts, captions, amazon_term = get_script_and_prompts(hook, is_gadget=True)
                image_files = fetch_amazon_images_strict(amazon_term) 
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 यह शानदार गैजेट आउट ऑफ़ स्टॉक होने से पहले चैनल के Bio से खरीदें!\n🔍 अमेज़न पर सर्च करें: {amazon_term}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 Don't Miss This {amazon_term}! #shorts", desc, ["shorts", "gadgets", "amazon finds", "tech"], "28")
                print("✅ GADGETS वीडियो लाइव हो गया।")
                return True 
                
            elif channel_type == "MYSTIC":
                hook = random.choice(MYSTIC_HOOKS)
                script, prompts, captions, _ = get_script_and_prompts(hook, is_gadget=False)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 ऐसे ही खूंखार रहस्यों और गैजेट्स के लिए लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 The Secret They Hid From You! #shorts", desc, ["shorts", "mystery", "creepy", "facts"], "28")
                print("✅ MYSTIC वीडियो लाइव हो गया।")
                return True 
                
        except Exception as e: 
            print(f"🛑 एरर: {e}. मशीन दोबारा कोशिश कर रही है...")
            time.sleep(10) 
    sys.exit(1)

if __name__ == "__main__":
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")
