# ==============================================================================
# 👑 TITAN EMPIRE ENGINE: HIGH-RETENTION AUTOMATION SYSTEM (ULTIMATE VERSION)
# ==============================================================================

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
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 🛠️ PIL ANTIALIAS BUG PATCH: वीडियो एडिटर को क्रैश होने से बचाने के लिए बाईपास
if not hasattr(Image, 'Resampling'):
    Image.Resampling = getattr(Image, 'LANCZOS', 1)
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

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
TOKEN_EMPIRE = os.environ.get("YOUTUBE_TOKEN_EMPIRE")
TOKEN_WEALTH = os.environ.get("YOUTUBE_TOKEN_WEALTH")
TOKEN_ZEROTOUCH = os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH")

if not GROQ_KEY:
    print("❌ Error: GROQ_API_KEY nahi mili!")
    sys.exit(1)

GADGET_HOOKS = ["Hidden Amazon Tech", "Must-Have Smart Gadgets", "Genius Kitchen Tools", "Car Gadgets You Need", "Cool Room Tech"]
AI_SELL_HOOKS = ["Free AI Tools 2026", "AI Video Editing Hacks", "Secret Websites Nobody Knows", "Smart Work vs Hard Work", "AI Tools for Students", "Time Saving Tech"]

def extract_json_safely(raw_text):
    match = re.search(r'\{[\s\S]*\}', str(raw_text).strip())
    return match.group(0) if match else "{}"

def get_script_and_prompts(hook_theme, category):
    print(f"\n✅ AI Engine Master Prompt ke sath Content likh raha hai: {hook_theme}")
    
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
    else:
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
    style_modifier = ", cinematic photography, highly detailed, 8k, hyperrealistic, strictly still life, no faces"
    
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
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try: 
        font = ImageFont.truetype("Roboto-Black.ttf", 110)
    except: 
        font = ImageFont.load_default()
        
    wrapped_text = textwrap.fill(text.upper(), width=16) 
    
    try:
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        text_w, text_h = draw.textsize(wrapped_text, font=font)
        
    x, y = (canvas_w - text_w) // 2, (canvas_h - text_h) // 2
    draw.multiline_text((x, y), wrapped_text, font=font, fill="#FFE81F", stroke_width=14, stroke_fill="black", align='center')
    
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
    print("🎬 Alex Hormozi स्टाइल में तेज़ पेसिंग और क्रॉसफ़ेड के साथ रेंडर हो रहा है...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    img_duration = 2.0 
    clips = []
    current_time = 0.0
    idx = 0
    
    while current_time < audio_duration:
        img_path = image_files[idx % len(image_files)]
        fixed_img_path = f"fixed_{idx}.jpg"
        process_image_for_video(img_path, fixed_img_path)
        
        remaining_time = audio_duration - current_time
        current_clip_duration = min(img_duration, remaining_time)
        
        base_clip = ImageClip(fixed_img_path).set_duration(current_clip_duration)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.06 * t)
        
        cap_text = captions[idx % len(captions)] if captions else ""
        if cap_text.strip():
            try:
                txt_clip = create_centered_text_clip(cap_text, current_clip_duration)
                txt_clip = txt_clip.set_position(('center', 0.8), relative=True) 
                
                final_clip = CompositeVideoClip(
                    [zoomed_clip.set_position(('center', 'center')), txt_clip], 
                    size=(1080, 1920)
                ).set_duration(current_clip_duration)
            except:
                final_clip = zoomed_clip
        else:
            final_clip = zoomed_clip
            
        if idx > 0:
            final_clip = final_clip.crossfadein(0.3)
            
        clips.append(final_clip)
        current_time += current_clip_duration
        idx += 1
        
    video = concatenate_videoclips(clips, padding=-0.3, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    
    main_audio.close()
    video.close()
    final.close()

# 🧹 नया फंक्शन: फ्लॉप/लो-व्यूज वीडियो को डिलीट करने वाला क्लीनर
def cleanup_low_view_videos(token, channel_name):
    print(f"\n🧹 {channel_name} की ऑटो-सफाई शुरू: 7 दिन पुराने और <100 व्यूज वाले वीडियो ढूँढ रहे हैं...")
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    
    try:
        credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
        youtube = build("youtube", "v3", credentials=credentials)
        
        # चैनल की 'Uploads' प्लेलिस्ट का ID निकालना
        channel_res = youtube.channels().list(mine=True, part="contentDetails").execute()
        if not channel_res.get("items"):
            return
        uploads_playlist_id = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        # पिछले 50 अपलोड्स निकालना
        playlist_res = youtube.playlistItems().list(playlistId=uploads_playlist_id, part="snippet", maxResults=50).execute()
        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist_res.get("items", [])]
        
        if not video_ids:
            print("🤷‍♂️ कोई वीडियो नहीं मिला।")
            return
            
        # वीडियो के आंकड़े (Views और Date) निकालना
        videos_res = youtube.videos().list(id=",".join(video_ids), part="snippet,statistics").execute()
        
        now = datetime.utcnow()
        deleted_count = 0
        
        for video in videos_res.get("items", []):
            vid_id = video["id"]
            title = video["snippet"]["title"]
            published_at_str = video["snippet"]["publishedAt"]
            
            # तारीख को कैलकुलेट करना
            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
            views = int(video["statistics"].get("viewCount", 0))
            days_old = (now - published_at).days
            
            # शर्त: अगर 7 दिन पुराना है और 100 से कम व्यूज हैं
            if days_old >= 7 and views < 100:
                print(f"🗑️ कबाड़ हटा रहे हैं: '{title}' (पुराना: {days_old} दिन, व्यूज: {views})")
                youtube.videos().delete(id=vid_id).execute()
                deleted_count += 1
                
        print(f"✅ {channel_name} की सफाई पूरी! कुल {deleted_count} फ्लॉप वीडियो डिलीट किए गए।")
        
    except HttpError as e:
        if "quota" in str(e).lower():
            print(f"🚨 {channel_name} का सफाई कोटा खत्म, आगे बढ़ रहे हैं।")
        else:
            print(f"⚠️ सफाई में यूट्यूब API एरर: {e}")
    except Exception as e:
        print(f"⚠️ सफाई में एरर: {e}")

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

def run_channel_safely(channel_name, token, hook_list, category="AI_SELL"):
    if not token:
        print(f"⚠️ {channel_name} ka token nahi mila. Isko skip kar rahe hain.")
        return False
        
    print(f"\n==============================================")
    print(f"🚀 STARTING CHANNEL: {channel_name}")
    print(f"==============================================")
    
    # सबसे पहले फ्लॉप वीडियो की सफाई करना
    cleanup_low_view_videos(token, channel_name)
    
    for attempt in range(5):
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
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, voice_file)
                make_video(image_files, captions, video_file, voice_file)
                
                gumroad_link = "https://girisbhut.gumroad.com/l/ajhzk"
                
                final_desc = f"{dyn_desc}\n\n🚀 👉 मेरा यह पूरा 100% ऑटोमैटिक YouTube Setup अभी खरीदें:\n🔗 यहाँ क्लिक करें: {gumroad_link}\n\n📝 Script:\n{script}"
                
                upload_video(token, video_file, dyn_title, final_desc, dyn_tags, "28")
                print(f"✅ AI SELL Video Live (Passive Marketing)! Title: {dyn_title}")
                return True 
                
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
    # ✅ MYSTERY CHANNEL को यहाँ से पूरी तरह हटा दिया गया है
    channels = [
        ("GIRISH AI GADGET", TOKEN_GADGET, GADGET_HOOKS, "GADGET"),
        ("FACELESS AI WEALTH", TOKEN_WEALTH, AI_SELL_HOOKS, "AI_SELL"),             
        ("AI AUTO PILOT EMPIRE", TOKEN_EMPIRE, AI_SELL_HOOKS, "AI_SELL"),         
        ("ZEROTOUCH AI CREATOR", TOKEN_ZEROTOUCH, AI_SELL_HOOKS, "AI_SELL")       
    ]
    
    for name, token, hooks, cat in channels:
        run_channel_safely(name, token, hooks, cat)
        time.sleep(15)
        
    print("\n✅ सभी 4 चैनलों का काम खत्म हो गया है बॉस!")
