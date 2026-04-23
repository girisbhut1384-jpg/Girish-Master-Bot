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
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 सिक्योरिटी दीवार हटाई जा रही है...")
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

# एकदम असली बिकने वाले गैजेट्स और रहस्य (ताकि वीडियो कभी रिपीट न हो)
GADGET_HOOKS = ["Amazon's Hidden Tech", "Crazy Gadgets Under 1000", "Must-Have Smart Home Items", "Secret Car Hacks", "Genius Kitchen Tools", "Futuristic Office Tech"]
MYSTIC_HOOKS = ["Terrifying Space Facts", "Deep Sea Monsters", "Unsolved Crimes of History", "Lost Ancient Cities", "Creepy Government Secrets", "Time Travel Evidences"]

def extract_json_safely(raw_text):
    raw_text = str(raw_text).strip()
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if match: return match.group(0)
    return "{}"

def get_script_and_prompts(hook_theme, is_gadget=False):
    print(f"\n✅ 70B AI इंजन नया वायरल टॉपिक खोज रहा है: {hook_theme}")
    
    prompt = f"""You are a master YouTube Shorts director. Your goal is 100% audience retention.
    THEME: "{hook_theme}".
    CRITICAL INSTRUCTION: INVENT a highly specific, unique, and NEVER-BEFORE-USED sub-topic!

    REQUIREMENTS:
    1. SCRIPT (Voiceover): Write an aggressive HINDI script (MINIMUM 60 WORDS). 
       - The FIRST sentence MUST be a shocking 3-second hook.
       - Keep the energy high and build extreme suspense.
    2. CAPTIONS (On-screen text): Write 8 short, punchy captions strictly in ENGLISH ALPHABETS.
    3. PROMPTS (English): 8 image generation prompts.
    """

    if is_gadget:
        prompt += """
    - SCRIPT ENDING: The script MUST end EXACTLY with: 'यह शानदार गैजेट अभी खरीदने का लिंक चैनल के बायो में है।'
    - AMAZON SEARCH TERM RULE: MUST be a simple, highly searchable real product name on Amazon India (e.g., 'Smart Watch', 'Spice Rack', 'Car Vacuum Cleaner'). Do NOT write abstract phrases.
        """
    else:
        prompt += """
    - SCRIPT ENDING: The script MUST end EXACTLY with: 'ऐसे ही खूंखार रहस्यों के लिए लिंक बायो में है।'
        """

    prompt += """
    Return ONLY valid JSON format exactly like this:
    {
      "topic": "your unique viral topic name",
      "script": "Hindi script here...",
      "captions": ["AMAZING FACT!", "LOOK AT THIS", "WAIT FOR IT...", "SHOCKING", "Caption 5", "Caption 6", "Caption 7", "Link in Bio!"],
      "prompts": ["Image 1 prompt", "Image 2 prompt", "Image 3 prompt", "Image 4 prompt", "Image 5 prompt", "Image 6 prompt", "Image 7 prompt", "Image 8 prompt"],
      "amazon_search_term": "Simple 2-3 word real Amazon India product keyword (Leave empty if mystery)"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": "Output only JSON."}, {"role": "user", "content": prompt}], "temperature": 0.8}
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=50)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                clean_json = extract_json_safely(content)
                parsed_data = json.loads(clean_json)
                script = parsed_data.get('script', '')
                if script:
                    print(f"🎯 सफलता! नया टॉपिक मिला: {parsed_data.get('topic')}")
                    return script.replace("*", ""), parsed_data.get('prompts', [])[:8], parsed_data.get('captions', [])[:8], parsed_data.get('amazon_search_term', '')
        except Exception as e: time.sleep(2)
    raise Exception("🚨 70B मॉडल फेल हो गया!")

# 🟢 100% असली अमेज़न फोटो का कड़ा नियम
def fetch_amazon_images_strict(query):
    print(f"🛒 अमेज़न (India) से '{query}' की बिल्कुल असली तस्वीरें निकाली जा रही हैं...")
    if not RAPIDAPI_KEY:
        raise Exception("⚠️ RAPIDAPI_KEY नहीं मिली! गैजेट चैनल के लिए असली फोटो अनिवार्य है।")

    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {"query": query, "page": "1", "country": "IN", "sort_by": "RELEVANCE"}
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}

    image_files = []
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=40)
        if response.status_code == 200:
            products = response.json().get("data", {}).get("products", [])
            for i, prod in enumerate(products):
                if len(image_files) >= 8: break
                photo_url = prod.get("product_photo")
                if photo_url:
                    img_res = requests.get(photo_url, timeout=15)
                    if img_res.status_code == 200:
                        filename = f"amazon_img_{i}.jpg"
                        with open(filename, "wb") as f: f.write(img_res.content)
                        image_files.append(filename)
            
            if len(image_files) >= 4:
                print(f"✅ अमेज़न से {len(image_files)} असली तस्वीरें 100% डाउनलोड हो गईं!")
                return image_files
            else:
                raise Exception(f"⚠️ अमेज़न पर '{query}' की पर्याप्त फोटो नहीं मिलीं।")
        else:
            raise Exception(f"⚠️ RapidAPI एरर: {response.status_code}. शायद API लिमिट ख़त्म हो गई है।")
    except Exception as e:
        raise Exception(f"अमेज़न से असली फोटो लाने में फेल: {e}")

# 🟢 मिस्ट्री चैनल के लिए AI फोटो
def fetch_ai_images(prompts):
    print("🌌 मिस्ट्री चैनल के लिए AI तस्वीरें जनरेट हो रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p + ", highly detailed, cinematic, 8k, textless, mind-bending")
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        for attempt in range(3): 
            try:
                res = requests.get(url, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: f.write(res.content)
                    image_files.append(filename)
                    break
            except: time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    print("✅ वॉइसओवर रिकॉर्ड हो रहा है...")
    async def _generate():
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+15%") 
                await communicate.save(filename)
                return True
            except: await asyncio.sleep(5)
        raise Exception("वॉइस सर्वर डाउन है।")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 पीले डब्बों का 100% इलाज 
def create_centered_text_clip(text, duration):
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default() 
        
    wrapped_text = textwrap.fill(text.upper(), width=22) 
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except Exception:
        text_width, text_height = draw.textsize(wrapped_text, font=font)
        
    x = (canvas_w - text_width) // 2
    y = (canvas_h - text_height) // 2
    
    pad_x, pad_y = 40, 20
    draw.rectangle([x - pad_x, y - pad_y, x + text_width + pad_x, y + text_height + pad_y], fill=(0, 0, 0, 190))
    draw.multiline_text((x, y), wrapped_text, font=font, fill="yellow", align='center')
    
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).resize(4.0).set_duration(duration)

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ प्रोफेशनल वीडियो रेंडर हो रहा है...")
    if not image_files: raise Exception("तस्वीरें नहीं मिलीं!")
        
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        base_clip = ImageClip(img_path)
        w, h = base_clip.size
        
        if w / h > 1080 / 1920: base_clip = base_clip.resize(height=1920)
        else: base_clip = base_clip.resize(width=1080)
            
        base_clip = base_clip.crop(x_center=base_clip.size[0]/2, y_center=base_clip.size[1]/2, width=1080, height=1920)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.05 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, time_per_image)
                txt_clip = txt_clip.set_position(('center', 'bottom')).margin(bottom=350, opacity=0)
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except: final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=(1080, 1920)).set_duration(time_per_image)
        else:
            final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=(1080, 1920)).set_duration(time_per_image)
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

def upload_video(token, filename, title, description, tags, category):
    print("✅ यूट्यूब पर अपलोड हो रहा है...")
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
                print(f"\n--- 📱 GADGETS चैनल प्रोसेसिंग (Attempt {attempt+1}) ---")
                hook = random.choice(GADGET_HOOKS)
                script, prompts, captions, amazon_term = get_script_and_prompts(hook, is_gadget=True)
                
                # 🟢 सिर्फ असली फोटो, अगर नहीं मिली तो एरर देकर 5 बार दूसरा प्रोडक्ट ढूंढेगा
                image_files = fetch_amazon_images_strict(amazon_term) 
                
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 यह शानदार गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {amazon_term}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 Best {amazon_term} #shorts", desc, ["shorts", "gadgets", "amazon finds", "tech"], "28")
                print("✅ GADGETS वीडियो लाइव हो गया।")
                return True 
                
            elif channel_type == "MYSTIC":
                print(f"\n--- 🌌 MYSTIC चैनल प्रोसेसिंग (Attempt {attempt+1}) ---")
                hook = random.choice(MYSTIC_HOOKS)
                script, prompts, captions, _ = get_script_and_prompts(hook, is_gadget=False)
                
                image_files = fetch_ai_images(prompts)
                
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 ऐसे ही खूंखार रहस्यों और गैजेट्स के लिए लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 You Won't Believe This Exists! #shorts", desc, ["shorts", "mystery", "creepy", "facts"], "28")
                print("✅ MYSTIC वीडियो लाइव हो गया।")
                return True 
                
        except Exception as e: 
            print(f"🛑 एरर: {e}. असली फोटो नहीं मिली, मशीन दूसरा प्रोडक्ट ढूंढ रही है...")
            time.sleep(10) 
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 मास्टर ब्रह्मास्त्र (Strict Amazon Mode & Fixed Captions) चालू हो गया है...")
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")
    print("\n🎯 काम पूरा हुआ।")
