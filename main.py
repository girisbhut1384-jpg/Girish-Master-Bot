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

print("🔓 Security aur Premium Setup chalu ho raha hai...")
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
AI_SELL_HOOKS = ["Escape the Matrix", "Smart Work Secrets", "Future Tech Tools", "AI Automation Power", "Time Saving Tech", "Secret of the 1%"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, category):
    print(f"\n✅ AI Engine dumdaar, fast-paced script aur viral Title likh raha hai: {hook_theme}")
    
    # 🟢 आपके दिए गए सख्त नियम (Strict Rules)
    base_rules = """
    STRICT RULES TO FOLLOW:
    1. Title Generation: Create a unique, highly clickable title (under 50 characters). DO NOT use the "🤯" emoji at the start. Use 1 different, relevant emoji at the END of the title.
    2. Avoid Spam Words: Do NOT use 'Passive Income', 'Get Rich Quick', 'Make Money While Sleeping', 'Digital Real Estate', or '10 Lakh'.
    3. Use Safe Words: 'Smart Work', 'Future Tech', 'AI Automation', 'Time Saving'.
    4. SCRIPT STRUCTURE (Hindi):
       - Hook (0-3s): Pattern-interrupt. Ask a shocking question or state a mind-blowing fact. No boring intros. DO NOT use "क्या आप जानते हैं".
       - Body (3-40s): Fast-paced, high-value information. Keep sentences short and punchy (3-4 sentences).
    """
    
    if category == "GADGET":
        prompt = f"""You are an expert YouTube Shorts Scriptwriter. THEME: "{hook_theme}".
        {base_rules}
        CRITICAL: The product MUST BE a common real-world item easily found on Amazon India.
        CTA (Call to Action): DO NOT say 'Link in description'. END EXACTLY WITH: 'ऐसे ही और शानदार गैजेट्स के लिए चैनल को अभी सब्सक्राइब करें।'
        
        CAPTIONS: 8 short English captions.
        PROMPTS: 8 simple image generation prompts.
        AMAZON SEARCH TERM: Simple 2-3 word real English product name.
        """
    elif category == "AI_SELL":
        prompt = f"""You are an expert YouTube Shorts Scriptwriter. THEME: "{hook_theme}".
        {base_rules}
        CRITICAL: Deliver a highly unique, futuristic concept about AI/Smart Work.
        CTA (Call to Action): DO NOT say 'Link in description'. END EXACTLY WITH: 'ऐसे ही और शानदार टूल्स के लिए चैनल को अभी सब्सक्राइब करें।'
        
        CAPTIONS: 8 short English captions.
        PROMPTS: 8 highly detailed, VISUALLY DISTINCT image prompts matching the exact concept. NO HUMANS.
        AMAZON SEARCH TERM: Leave empty ("").
        """
    else: 
        prompt = f"""You are an expert YouTube Shorts Scriptwriter. THEME: "{hook_theme}".
        {base_rules}
        CRITICAL: Build extreme suspense with a complete mini-story arc.
        CTA (Call to Action): DO NOT say 'Link in description'. END EXACTLY WITH: 'ऐसे ही खूंखार और गुप्त रहस्यों के लिए चैनल को अभी सब्सक्राइब करें।'
        
        CAPTIONS: 8 short English captions.
        PROMPTS: 8 distinct dark/creepy image prompts matching the exact storyline.
        AMAZON SEARCH TERM: Leave empty ("").
        """

    prompt += """
    Return ONLY valid JSON in this exact format:
    {
      "title": "Unique Title Here 🔥",
      "tags": ["shorts", "tech", "smartwork"],
      "script": "Complete Hindi script here (Hook + Body + CTA)",
      "captions": ["SHOCKING", "DAILY PROBLEM", "THE SOLUTION", "WAIT FOR IT", "AMAZING TECH", "MIND BLOWN", "STOCK ENDING", "SUBSCRIBE NOW"],
      "prompts": ["Image 1", "Image 2", "Image 3", "Image 4", "Image 5", "Image 6", "Image 7", "Image 8"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.95} 
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                if parsed.get('script') and parsed.get('title'):
                    print("🎯 Script, Title & Tags Ready!")
                    return parsed['script'].replace("*", ""), parsed['prompts'][:8], parsed['captions'][:8], parsed.get('amazon_search_term', ''), parsed['title'], parsed.get('tags', ['shorts', 'viral', 'trending'])[:3]
        except: time.sleep(2)
    raise Exception("🚨 AI Model Failed!")

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
    image_files = []
    headers = {"User-Agent": "Mozilla/5.0"}
    style_modifier = ", cinematic photography, highly detailed, 8k, hyperrealistic"
    
    for i, p in enumerate(prompts):
        seed = random.randint(100000, 999999) 
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p + style_modifier)}?width=1080&height=1920&nologo=true&seed={seed}"
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
    
    for attempt in range(5):
        try:
            hook = random.choice(hook_list)
            # 🟢 अब मशीन टाइटल और टैग्स भी डायनामिक निकाल रही है!
            script, prompts, captions, amazon_term, dyn_title, dyn_tags = get_script_and_prompts(hook, category)
            
            prefix = channel_name.replace(" ", "_").lower()
            voice_file = f"voice_{prefix}.mp3"
            video_file = f"final_{prefix}.mp4"

            if category == "GADGET":
                image_files = fetch_amazon_images_strict(amazon_term) 
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                clean_term = re.sub(r'[^a-zA-Z0-9 ]', '', str(amazon_term)).strip()
                amz_link = f"https://www.amazon.in/s?k={urllib.parse.quote(clean_term)}&tag=girishbhut07-21"
                desc = f"🔗 प्रोडक्ट यहाँ से खरीदें: {amz_link}\n\n{script}"
                
                upload_video(token, video_file, dyn_title, desc, dyn_tags, "28")
                print(f"✅ GADGETS Video Live! Title: {dyn_title}")
                
            elif category == "AI_SELL":
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                gumroad_link = "https://girisbhut.gumroad.com/l/ajhzk"
                desc = f"🔗 पूरा AI YouTube Setup खरीदें: {gumroad_link}\n\n{script}"
                
                upload_video(token, video_file, dyn_title, desc, dyn_tags, "28")
                print(f"✅ AI SELL Video Live! Title: {dyn_title}")

            else: 
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                desc = f"🔥 ऐसे ही रहस्यों के लिए सब्सक्राइब करें!\n\n{script}"
                upload_video(token, video_file, dyn_title, desc, dyn_tags, "28")
                print(f"✅ {channel_name} Video Live! Title: {dyn_title}")
                
            return True 
                
        except Exception as e: 
            print(f"🛑 Error on {channel_name}: {e}. Machine dobara koshish kar rahi hai...")
            time.sleep(10) 
            
    print(f"❌ {channel_name} fail ho gaya.")
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
        
    print("\n✅ सभी 5 चैनलों का काम खत्म हो गया है बॉस!")
