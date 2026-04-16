# गिरीश भाई का V8.0 मास्टर कोड (Bulletproof JSON Extractor)
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

import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from google import genai  
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.config import change_settings

# 🛑 1. इमेजमैजिक सिक्योरिटी दीवार हटाना
print("🔓 सिक्योरिटी दीवार हटाई जा रही है...")
os.system("sudo sed -i '/pattern=\"@\\*\"/d' /etc/ImageMagick-6/policy.xml")

# 🛑 2. लिनक्स के ऑफिशियल हिंदी फॉन्ट
print("📦 सिस्टम के अंदर ऑफिशियल हिंदी फॉन्ट इंस्टॉल हो रहे हैं...")
os.system("sudo apt-get update -y")
os.system("sudo apt-get install -y fonts-indic fonts-noto-core")

sys_fonts = glob.glob("/usr/share/fonts/**/*.ttf", recursive=True)
hindi_fonts = [f for f in sys_fonts if "Devanagari" in f or "Samyak" in f or "Gargi" in f or "Nakula" in f]
FONT_PATH = hindi_fonts[0] if hindi_fonts else (sys_fonts[0] if sys_fonts else "Arial")
print(f"✅ परफेक्ट फॉन्ट मिल गया: {FONT_PATH}")

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    sys.exit(1)

client = genai.Client(api_key=GEMINI_KEY)
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")

GADGET_TOPICS = [
    "स्मार्ट किचन हैक्स गैजेट्स", "मच्छर भगाने वाला हाई-टेक गैजेट", "कमरे को स्मार्ट बनाने वाली लाइट्स", 
    "कार के लिए सीक्रेट गैजेट", "स्टूडेंट्स के लिए जादुई पेन/गैजेट", "सर्दियों के लिए पोर्टेबल हीटर गैजेट"
]

MYSTIC_TOPICS = [
    "बरमूडा ट्राएंगल का सबसे नया सच", "मिस्र के पिरामिडों के नीचे क्या है?", "क्या एलियंस पृथ्वी पर आ चुके हैं?",
    "समुद्र की सबसे गहरी जगह का रहस्य", "समय यात्रा (Time Travel) के असली सबूत", "ब्लैक होल के अंदर की दुनिया"
]

def get_fallback_script(prompt, model_name):
    print(f"   👉 बैकअप इंजन चालू: {model_name}...")
    url = "https://text.pollinations.ai/"
    data = {
        "messages": [
            {"role": "system", "content": "You are a professional YouTube script writer. Respond ONLY with raw, valid JSON. Do not add markdown or explanations."},
            {"role": "user", "content": prompt}
        ],
        "model": model_name,
        "jsonMode": True
    }
    response = requests.post(url, json=data, timeout=60)
    response.raise_for_status()
    
    resp_text = response.text.strip()
    
    # अगर जवाब API के डिब्बे में है, तो पहले डिब्बा खोलें
    try:
        parsed = json.loads(resp_text)
        if "choices" in parsed and len(parsed["choices"]) > 0:
            resp_text = parsed["choices"][0]["message"]["content"]
        elif "content" in parsed:
            resp_text = parsed["content"]
    except:
        pass
        
    return resp_text

def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n✅ AI स्क्रिप्ट तैयार कर रहा है: {topic}")
    
    prompt = f"Write a VIRAL YouTube short script in Hindi about: {topic}. Start with a shocking hook. STRICTLY 50-60 words. "
    if is_gadget: 
        prompt += "End EXACTLY with: 'खरीदने का लिंक चैनल के बायो में है।'. "
    else: 
        prompt += "End EXACTLY with: 'रहस्यमयी किताबें खरीदने का लिंक बायो में है।'. "
    
    prompt += """
    IMPORTANT: For the 'prompts' array, describe the scene. 
    Add exactly this to the end of EVERY image prompt: ", hyper-realistic, 8k resolution, shot on DSLR, lifelike photography, extreme detail, NO TEXT, textless, no words, no letters".
    Return ONLY JSON:
    {
      "script": "Hindi voiceover text...",
      "captions": ["शॉकिंग सच! 😲", "क्या आपको पता है?", "खतरनाक गैजेट 🔥", "लिंक बायो में है!", "कैप्शन 5", "कैप्शन 6", "कैप्शन 7", "कैप्शन 8"],
      "prompts": ["Image 1 prompt...", "Image 2 prompt...", "...", "...", "...", "...", "...", "..."],
      "gadget_name": "Amazon search name or empty."
    }
    """
    
    clean_text = None
    
    engines = [
        {"type": "gemini", "name": "gemini-2.0-flash"},
        {"type": "gemini", "name": "gemini-1.5-flash"},
        {"type": "fallback", "name": "openai"},  
        {"type": "fallback", "name": "llama"},   
        {"type": "fallback", "name": "mistral"}  
    ]
    
    for engine in engines:
        try:
            if engine["type"] == "gemini":
                print(f"   👉 मेन इंजन ट्राई कर रहा हूँ: {engine['name']}...")
                response = client.models.generate_content(model=engine['name'], contents=prompt)
                if response.text:
                    clean_text = response.text.strip()
                    print(f"   ✅ {engine['name']} ने जवाब दिया!")
                    break
            else:
                clean_text = get_fallback_script(prompt, engine['name']).strip()
                if clean_text:
                    print(f"   ✅ बैकअप इंजन ({engine['name']}) ने जवाब दिया!")
                    break
        except Exception as e:
            print(f"   ❌ {engine['name']} फेल हुआ। अगले इंजन पर जा रहा हूँ...")
            continue 
            
    if not clean_text: 
        raise Exception("चारों इंजन फेल! इंटरनेट पूरी तरह डाउन है।")
        
    # 🛑 सबसे आख़िरी और पक्का समाधान (Bulletproof Extractor)
    # AI कुछ भी दे, हम सिर्फ { से } तक का हिस्सा काट कर निकालेंगे
    start_idx = clean_text.find('{')
    end_idx = clean_text.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        clean_text = clean_text[start_idx:end_idx+1]
    else:
        raise Exception(f"AI के जवाब में कोई JSON नहीं मिला: {clean_text[:100]}")

    try:
        data = json.loads(clean_text)
    except json.JSONDecodeError:
        raise Exception(f"AI का डाटा खराब है: {clean_text[:100]}...")

    script = data.get('script', data.get('Script', ''))
    if not script:
         raise Exception(f"AI ने 'script' नहीं लिखी! डाटा: {clean_text[:100]}...")

    return script.replace("*", ""), data.get('prompts', [])[:8], data.get('captions', [])[:8], data.get('gadget_name', '')

def fetch_ai_images(prompts):
    print("✅ हाई-क्वालिटी 8K तस्वीरें जनरेट हो रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        for _ in range(3): 
            try:
                res = requests.get(url, timeout=40) 
                if res.status_code == 200: 
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    image_files.append(filename)
                    break
            except Exception: 
                time.sleep(3)
    return image_files

def create_human_voice(text, filename):
    print("✅ प्रोफेशनल वॉइसओवर रिकॉर्ड हो रहा है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+10%")
        await communicate.save(filename)
    asyncio.run(_generate())

def make_video(image_files, captions, final_vid, audio_file):
    print("✅ फाइनल वीडियो रेंडर हो रहा है...")
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    
    clips = []
    for i, img in enumerate(image_files):
        base_clip = ImageClip(img)
        w, h = base_clip.size
        
        if w / h > 1080 / 1920: 
            base_clip = base_clip.resize(height=1920)
        else: 
            base_clip = base_clip.resize(width=1080)
            
        base_clip = base_clip.crop(x_center=base_clip.size[0]/2, y_center=base_clip.size[1]/2, width=1080, height=1920)
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.05 * (t / time_per_image)).set_duration(time_per_image)
        
        txt_clip = TextClip(
            captions[i], 
            fontsize=85, 
            color='yellow', 
            bg_color='black', 
            font=FONT_PATH, 
            method='caption', 
            size=(900, None)
        )
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(time_per_image).margin(bottom=300, opacity=0)
        
        final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center')), txt_clip], size=(1080, 1920)).set_duration(time_per_image)
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    final = video.set_audio(main_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    main_audio.close()
    video.close()
    final.close()

def upload_video(token, filename, title, description, tags, category):
    print("✅ यूट्यूब पर वीडियो अपलोड किया जा रहा है...")
    credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={"snippet": {"title": title, "description": description, "tags": tags, "categoryId": category}, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}},
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )
    request.execute()

def run_channel_safely(channel_type):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            if channel_type == "GADGETS":
                print(f"\n--- 📱 GADGETS चैनल की प्रोसेसिंग चालू है ---")
                topic = random.choice(GADGET_TOPICS)
                script, prompts, captions, gadget_name = get_script_and_prompts(topic, is_gadget=True)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_gadget.mp3")
                make_video(image_files, captions, "final_gadget.mp4", "voice_gadget.mp3")
                desc = f"🔥 👉 गैजेट खरीदने का लिंक चैनल के Bio में है!\n🔍 अमेज़न पर सर्च करें: {gadget_name}\n\n{script}"
                upload_video(TOKEN_GADGETS, "final_gadget.mp4", f"🤯 {gadget_name} #shorts", desc, ["shorts", "gadgets", "amazon finds"], "28")
                print("🏆 GADGETS चैनल पर वीडियो सफलतापूर्वक लाइव हो गया!")
                return True 
                
            elif channel_type == "MYSTIC":
                print(f"\n--- 🌌 MYSTIC चैनल की प्रोसेसिंग चालू है ---")
                topic = random.choice(MYSTIC_TOPICS)
                script, prompts, captions, _ = get_script_and_prompts(topic, is_gadget=False)
                image_files = fetch_ai_images(prompts)
                create_human_voice(script, "voice_mystic.mp3")
                make_video(image_files, captions, "final_mystic.mp4", "voice_mystic.mp3")
                desc = f"🔥 👉 रहस्यमयी किताबें और गैजेट्स का लिंक चैनल के Bio में है!\n\n{script}"
                upload_video(TOKEN_MYSTIC, "final_mystic.mp4", f"🤯 {topic} #shorts", desc, ["shorts", "mystery", "facts"], "28")
                print("🏆 MYSTIC चैनल पर वीडियो सफलतापूर्वक लाइव हो गया!")
                return True 
                
        except Exception as e: 
            print(f"🛑 मेन एरर: {e}")
            print(f"⚠️ सिस्टम रीस्टार्ट हो रहा है... (Attempt {attempt+1}/{max_attempts})")
            time.sleep(15) 
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 V8.0 मास्टर ऑटोमेशन चालू हो गया है...")
    run_channel_safely("GADGETS")
    print("\n⏳ चैनल स्विच हो रहा है...\n")
    time.sleep(30)
    run_channel_safely("MYSTIC")
    print("\n🎯 आज का काम पूरा हुआ! मशीन स्लीप मोड में जा रही है।")
