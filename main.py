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

from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

print("🔓 सिक्योरिटी दीवार हटाई जा रही है...")
os.system("sudo rm -f /etc/ImageMagick-6/policy.xml")
os.system("sudo rm -f /etc/ImageMagick-7/policy.xml")

print("📦 सिस्टम के अंदर ऑफिशियल हिंदी फॉन्ट इंस्टॉल हो रहे हैं...")
os.system("sudo apt-get update -y")
os.system("sudo apt-get install -y fonts-indic fonts-noto-core libraqm-dev")

sys_fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
hindi_fonts = [f for f in sys_fonts if "Devanagari" in f or "Samyak" in f or "Gargi" in f or "Nakula" in f]
FONT_PATH = hindi_fonts[0] if hindi_fonts else (sys_fonts[0] if sys_fonts else "Arial")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_KEY:
    print("❌ एरर: GROQ_API_KEY नहीं मिली!")
    sys.exit(1)

CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

GADGET_TOPICS = ["स्मार्ट किचन गैजेट", "मच्छर भगाने वाला इलेक्ट्रॉनिक गैजेट", "स्मार्ट रूम लाइट्स", "कार के लिए गैजेट", "पोर्टेबल हीटर गैजेट"]
MYSTIC_TOPICS = ["बरमूडा ट्राएंगल का रहस्य", "मिस्र के पिरामिडों का सच", "समुद्र की सबसे गहरी जगह", "ब्लैक होल का रहस्य", "क्या एलियंस हैं?"]

def extract_json_safely(raw_text):
    raw_text = str(raw_text).strip()
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if match:
        return match.group(0)
    return "{}"

def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n✅ 70B AI इंजन स्क्रिप्ट तैयार कर रहा है: {topic}")
    
    prompt = f"""You are an expert YouTube Shorts director. Generate a highly logical JSON response for a short video about: "{topic}".

    REQUIREMENTS:
    1. SCRIPT: Write a 50-60 word Hindi script. It MUST make logical sense. No random or meaningless words.
    2. CAPTIONS: 8 short, meaningful Hindi captions summarizing the current sentence.
    3. PROMPTS (English): 8 image generation prompts. Each prompt MUST visually match the exact sentence being spoken.
    """

    if is_gadget:
        prompt += """
    - SCRIPT ENDING: The script MUST end EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'
    - IMAGE STRICT RULES: Describe ONLY the physical gadget/product. 
    - CRITICAL BAN: NO HUMANS, NO FACES, NO PEOPLE, NO ANIMALS.
    - Add exactly this to the end of EVERY image prompt: ", highly detailed product photography, 8k resolution, macro close-up, modern studio lighting, STRICTLY NO HUMANS, NO FACES, NO ANIMALS, NO TEXT, textless"
        """
    else:
        prompt += """
    - SCRIPT ENDING: The script MUST end EXACTLY with: 'रहस्यमयी किताबें खरीदने का लिंक बायो में है।'
    - IMAGE STRICT RULES: Describe realistic cinematic scenes that match the mystery exactly. 
    - CRITICAL BAN: NO HUMANS, NO FACES, NO ANIMALS, NO TIGERS, NO LIONS. ONLY LANDSCAPES, SHIPS, PLANETS, OR MYSTERIOUS OBJECTS.
    - Add exactly this to the end of EVERY image prompt: ", cinematic masterpiece, hyper-realistic, 8k resolution, mysterious atmosphere, extreme detail, NO HUMANS, NO ANIMALS, NO TEXT, textless"
        """

    prompt += """
    Return ONLY valid JSON format exactly like this (NO conversational text outside JSON):
    {
      "topic": "topic name",
      "script": "Hindi script here...",
      "captions": ["caption 1", "caption 2", "caption 3", "caption 4", "caption 5", "caption 6", "caption 7", "caption 8"],
      "prompts": ["Image 1 prompt", "Image 2 prompt", "Image 3 prompt", "Image 4 prompt", "Image 5 prompt", "Image 6 prompt", "Image 7 prompt", "Image 8 prompt"],
      "gadget_name": "Amazon search name of the gadget (or empty if mystery)"
    }
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile"]
    
    for model_name in models_to_try:
        print(f"🔄 ट्राइंग पावरफुल मॉडल: {model_name}...")
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a precise JSON generator. Output only perfectly formatted JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2 
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=50)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                clean_json = extract_json_safely(content)
                parsed_data = json.loads(clean_json)
                
                script = parsed_data.get('script', '')
                if script and len(parsed_data.get('prompts', [])) >= 4:
                    print(f"🎯 सफलता! {model_name} ने एकदम सही और लॉजिकल स्क्रिप्ट दी।")
                    return script.replace("*", ""), parsed_data.get('prompts', [])[:8], parsed_data.get('captions', [])[:8], parsed_data.get('gadget_name', '')
            else:
                print(f"⚠️ {model_name} फेल (Status: {response.status_code}).")
        except Exception as e:
            print(f"⚠️ {model_name} में एरर: {e}")
            time.sleep(2)
            
    raise Exception("🚨 70B मॉडल्स फेल हो गए! कृपया बाद में कोशिश करें।")

def fetch_ai_images(prompts):
    print("✅ हाई-क्वालिटी तस्वीरें जनरेट हो रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        
        success = False
        for attempt in range(3): 
            try:
                res = requests.get(url, timeout=30) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    image_files.append(filename)
                    success = True
                    break
            except Exception: 
                time.sleep(3)
        if not success:
            print(f"⚠️ तस्वीर {i} स्किप की गई।")
    return image_files

def create_human_voice(text, filename):
    print("✅ वॉइसओवर रिकॉर्ड हो रहा है...")
    async def _generate():
        for attempt in range(3):
            try:
                communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
                await communicate.save(filename)
                return True
            except Exception as e:
                await asyncio.sleep(5)
        raise Exception("वॉइस सर्वर डाउन है।")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_generate())

# 🟢 नया 100% परफेक्ट हिंदी टेक्स्ट जनरेटर
def create_hindi_text_clip(text, font_path, duration):
    canvas_w, canvas_h = 1080, 400
    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype(font_path, 80)
    except:
        font = ImageFont.load_default()
        
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except Exception:
        text_width, text_height = draw.textsize(text, font=font)
        
    x = (canvas_w - text_width) // 2
    y = (canvas_h - text_height) // 2
    
    pad_x, pad_y = 30, 20
    draw.rectangle([x - pad_x, y - pad_y, x + text_width + pad_x, y + text_height + pad_y], fill=(0, 0, 0, 200))
    draw.text((x, y), text, font=font, fill="yellow")
    
    temp_filename = f"temp_caption_{random.randint(10000, 99999)}.png"
    img.save(temp_filename)
    return ImageClip(temp_filename).set_duration(duration)

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ वीडियो रेंडर हो रहा है...")
    if not image_files:
        raise Exception("तस्वीरें नहीं मिलीं!")
        
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    clips = []
    
    for i, img_path in enumerate(image_files):
        base_clip = ImageClip(img_path)
        w, h = base_clip.size
        if w / h > 1080 / 1920: 
            base_clip = base_clip.resize(height=1920)
        else: 
            base_clip = base_clip.resize(width=1080)
            
        base_clip = base_clip.crop(x_center=base_clip.size[0]/2, y_center=base_clip.size[1]/2, width=1080, height=1920)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.05 * (t / time_per_image)).set_duration(time_per_image)
        
        cap_text = captions[i] if i < len(captions) else ""
        cap_text = cap_text.strip()
        
        if cap_text:
            try:
                # 🟢 ImageMagick की जगह Pillow से परफेक्ट हिंदी टेक्स्ट 
                txt_clip = create_hindi_text_clip(cap_text, FONT_PATH, time_per_image)
                txt_clip = txt_clip.set_position(('center', 'bottom')).margin(bottom=300, opacity=0)
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
            except Exception as e:
                print(f"⚠️ कैप्शन एरर: {e}")
                final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=(1080, 1920)).set_duration(time_per_image)
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
    for attempt in range(3):
        try:
            if channel_type == "GADGETS":
                print(f"\n--- 📱 GADGETS चैनल प्रोसेसिंग ---")
                topic = random.choice(GADGET_TOPICS)
                script, prompts, captions, gadget_name = get_script_and_prompts(topic, is_gadget=True)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {gadget_name}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 {gadget_name} #shorts", desc, ["shorts", "gadgets", "amazon finds"], "28")
                print("✅ GADGETS वीडियो लाइव हो गया।")
                return True 
                
            elif channel_type == "MYSTIC":
                print(f"\n--- 🌌 MYSTIC चैनल प्रोसेसिंग ---")
                topic = random.choice(MYSTIC_TOPICS)
                script, prompts, captions, _ = get_script_and_prompts(topic, is_gadget=False)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 रहस्यमयी किताबें और गैजेट्स का लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 {topic} #shorts", desc, ["shorts", "mystery", "facts"], "28")
                print("✅ MYSTIC वीडियो लाइव हो गया।")
                return True 
                
        except Exception as e: 
            print(f"🛑 एरर: {e}. रीस्टार्ट हो रहा है...")
            time.sleep(15) 
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 70B प्रो-इंजन चालू हो गया है...")
    run_channel_safely("GADGETS")
    time.sleep(30)
    run_channel_safely("MYSTIC")
    print("\n🎯 काम पूरा हुआ।")
