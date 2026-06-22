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
AI_SELL_HOOKS = ["Free AI Tools 2026", "AI Video Editing Hacks", "Secret Websites Nobody Knows", "Smart Work vs Hard Work", "AI Tools for Students", "Time Saving Tech"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, category):
    print(f"\n✅ AI Engine Master Prompt ke sath Content likh raha hai: {hook_theme}")
    
    # 🟢 बॉस का दिया हुआ 'Master System Prompt' यहाँ 100% फिट कर दिया गया है
    master_system_rules = """
    STRICT RULES TO FOLLOW:
    1. Title Generation: Create a unique, highly clickable title (under 50 characters). DO NOT use the "🤯" emoji at the start. Use a different, relevant emoji at the END of the title. Never repeat previous titles.
    2. Avoid Spam Words: DO NOT use words like 'Passive Income', 'Get Rich Quick', 'Make Money While Sleeping', or 'Digital Real Estate'. Instead, use safe words like 'Smart Work', 'Future Tech', 'AI Automation', or 'Time Saving'.
    3. The Hook (0-3 Seconds): The first sentence MUST be a pattern-interrupt. Ask a shocking question or state a mind-blowing fact to stop the user from scrolling. No boring introductions. Do NOT use "क्या आप जानते हैं".
    4. The Value (3-40 Seconds): Provide fast-paced, high-value information. Keep sentences short and punchy. Write exactly enough words (around 100-110 words) for a 45-50 second Hindi voiceover.
    5. Call to Action (CTA): DO NOT say 'Link in description' in the voiceover script.
    """
    
    if category == "GADGET":
        prompt = f"""You are an expert YouTube Shorts Scriptwriter and Viral Content Strategist. THEME: "{hook_theme}".
        {master_system_rules}
        NICHE: Tech Gadgets.
        CRITICAL RULE: The product MUST BE a common real-world item easily found on Amazon India.
        VOICEOVER CTA: END EXACTLY WITH: 'ऐसे ही और शानदार गैजेट्स के लिए चैनल को अभी सब्सक्राइब करें।'
        
        Generate a UNIQUE 2-line SEO DESCRIPTION about the video.
        Generate 3 UNIQUE TAGS.
        CAPTIONS: 8 short English captions.
        PROMPTS: 8 simple image generation prompts.
        AMAZON SEARCH TERM: Simple 2-3 word real English product name.
        """
    elif category == "AI_SELL":
        prompt = f"""You are an expert YouTube Shorts Scriptwriter and Viral Content Strategist. THEME: "{hook_theme}".
        {master_system_rules}
        NICHE: AI Tools & Automation Value.
        CRITICAL RULES: DO NOT SELL ANYTHING IN THE SCRIPT. DO NOT mention Gumroad or setups. Only provide high-value information.
        VOICEOVER CTA: END EXACTLY WITH: 'ऐसे ही और शानदार टूल्स के लिए चैनल को अभी सब्सक्राइब करें।'
        
        Generate a UNIQUE 2-line SEO DESCRIPTION about the video value.
        Generate 3 UNIQUE TAGS.
        CAPTIONS: 8 short English captions.
        PROMPTS: 8 highly detailed image prompts matching the concept.
        AMAZON SEARCH TERM: Leave empty ("").
        """
    else: 
        prompt = f"""You are a dark, mysterious storyteller. THEME: "{hook_theme}".
        {master_system_rules}
        NICHE: Creepy Mysteries.
        CRITICAL RULE: Build extreme suspense with a complete story arc. Give creepy details.
        VOICEOVER CTA: END EXACTLY WITH: 'ऐसे ही खूंखार और गुप्त रहस्यों के लिए चैनल को अभी सब्सक्राइब करें।'
        
        Generate a UNIQUE 2-line SEO DESCRIPTION about the mystery.
        Generate 3 UNIQUE TAGS.
        CAPTIONS: 8 short English captions.
        PROMPTS: 8 distinct dark/creepy image prompts.
        AMAZON SEARCH TERM: Leave empty ("").
        """

    prompt += """
    Return ONLY valid JSON in this exact format:
    {
      "title": "Unique Viral Title Here 🔥",
      "description": "Unique 2-3 lines description here...",
      "tags": ["tag1", "tag2", "tag3"],
      "script": "Hindi script here (Hook + Value + CTA)...",
      "captions": ["CAPTION1", "CAPTION2", "CAPTION3", "CAPTION4", "CAPTION5", "CAPTION6", "CAPTION7", "CAPTION8"],
      "prompts": ["Prompt1", "Prompt2", "Prompt3", "Prompt4", "Prompt5", "Prompt6", "Prompt7", "Prompt8"],
      "amazon_search_term": "Product name"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.9} 
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                parsed = json.loads(extract_json_safely(response.json()['choices'][0]['message']['content']))
                if parsed.get('script'):
                    print("🎯 Script, Title, Description aur Tags Ready!")
                    return (
                        parsed['script'].replace("*", ""), 
                        parsed['prompts'][:8], 
                        parsed['captions'][:8], 
                        parsed.get('amazon_search_term', 'Gadget'), 
                        parsed.get('title', 'Viral Shorts 🔥'),
                        parsed.get('description', 'Watch this amazing video!'),
                        parsed.get('tags', ['shorts', 'viral', 'trending'])
                    )
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
            # 🟢 मशीन अब मास्टर प्रॉम्प्ट से बिल्कुल परफेक्ट डेटा ला रही है
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
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                gumroad_link = "https://girisbhut.gumroad.com/l/ajhzk"
                
                final_desc = f"{dyn_desc}\n\n🚀 👉 मेरा यह पूरा 100% ऑटोमैटिक YouTube Setup अभी खरीदें:\n🔗 यहाँ क्लिक करें: {gumroad_link}\n\n📝 Script:\n{script}"
                
                upload_video(token, video_file, dyn_title, final_desc, dyn_tags, "28")
                print(f"✅ AI SELL Video Live (Passive Marketing)! Title: {dyn_title}")
                return True 

            else: 
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                final_desc = f"{dyn_desc}\n\n🔥 👉 ऐसे ही खूंखार रहस्यों के लिए सब्सक्राइब करें!\n\n📝 Script:\n{script}"
                
                upload_video(token, video_file, dyn_title, final_desc, dyn_tags, "28")
                print(f"✅ {channel_name} Video Live! Title: {dyn_title}")
                return True 
                
        # 🟢 4 घंटे की बर्बादी रोकने वाला 'स्मार्ट ब्रेक'
        except HttpError as e:
            error_content = str(e).lower()
            if "quota" in error_content or "ratelimit" in error_content or "429" in error_content:
                print(f"🚨 YOUTUBE QUOTA FULL for {channel_name}! यूट्यूब की अपलोड लिमिट खत्म हो चुकी है।")
                print("🚫 मशीन समझदार है, इसलिए 4 घंटे बर्बाद नहीं करेगी। इस चैनल को आज के लिए रोक रहे हैं।")
                break 
            else:
                print(f"🛑 YouTube API Error on {channel_name}: {e}. Dobara koshish kar rahe hain...")
                time.sleep(10)
                
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

