# गिरीश भाई का अल्टीमेट मास्टर कोड V3.3 (Full Screen + Zoom In + Smart Amazon SEO)
import os
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, CompositeVideoClip
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_loop import audio_loop
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. तिजोरी से चाबियाँ
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = os.environ.get("AMAZON_ID", "YOUR_AMAZON_LINK_HERE")

if not AMAZON_ID.startswith("http"):
    AMAZON_ID = "https://" + AMAZON_ID

# 2. Gemini AI - (JSON Mode + Gadget Name Extractor)
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n🧠 Gemini AI '{topic}' पर स्क्रिप्ट सोच रहा है...")
    
    active_model = "models/gemini-1.5-flash" 
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
        models_data = requests.get(list_url).json()
        for m in models_data.get('models', []):
            if 'flash' in m.get('name', '') and 'generateContent' in m.get('supportedGenerationMethods', []):
                active_model = m['name']
                break
    except Exception:
        pass
        
    url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={GEMINI_KEY}"
    
    prompt = f"Write a 40-second engaging YouTube short script in Hindi about {topic}. Start with a mind-blowing hook. "
    if is_gadget:
        prompt += "End the Hindi script EXACTLY with: 'इसे खरीदने का लिंक नीचे कमेंट और डिस्क्रिप्शन में दिया गया है।'. "
    
    prompt += """
    IMPORTANT: You must return ONLY a raw JSON format.
    {
      "script": "Your full spoken Hindi voiceover text here...",
      "prompts": [
        "A highly realistic 4k cinematic image of...",
        "A detailed 3D render of...",
        "A hyper-realistic scene of...",
        "A beautiful cinematic lighting shot of..."
      ],
      "gadget_name": "Write the exact short product name here (e.g., Wipro Smart Bulb). If not a gadget, leave empty."
    }
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload).json()
    
    try:
        clean_text = response['candidates'][0]['content']['parts'][0]['text'].strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3].strip()
        elif clean_text.startswith("```"):
             clean_text = clean_text[3:-3].strip()
             
        data = json.loads(clean_text)
        hindi_script = data['script'].replace("*", "").replace("#", "")
        image_prompts = data['prompts'][:4]
        gadget_name = data.get('gadget_name', '')
        print(f"✅ [AI स्क्रिप्ट तैयार]: {hindi_script[:60]}...")
        return hindi_script, image_prompts, gadget_name
    except Exception as e:
        raise Exception(f"❌ Gemini JSON एरर: {e}")

# 3. Pollinations AI (जिद्दी डाउनलोडर)
def fetch_ai_images(prompts):
    print("🎨 Pollinations AI से तस्वीरें बनाई जा रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) 
    
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        
        for attempt in range(5): 
            try:
                res = requests.get(url, timeout=60) 
                if res.status_code == 200 and len(res.content) > 20000: 
                    with open(filename, "wb") as f:
                        f.write(res.content)
                    image_files.append(filename)
                    print(f"   ✅ सीन {i+1} सफल!")
                    time.sleep(2)
                    break 
                else:
                    time.sleep(5)
            except Exception:
                time.sleep(5)
                
    if len(image_files) == 0:
        raise Exception("भयंकर एरर: एक भी तस्वीर नहीं बन पाई!")
    return image_files

# 4. असली इंसानों जैसी आवाज़ 
def create_human_voice(text, filename):
    print("🎙️ आवाज़ बनाई जा रही है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await communicate.save(filename)
    asyncio.run(_generate())

# 5. मास्टर एडिटिंग (100% Full Screen + Zoom in)
def make_video(image_files, final_vid, audio_file):
    print("🎬 प्रो-लेवल एडिटिंग (Full Screen + Zoom)...")
    
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    time_per_image = audio_duration / len(image_files)
    
    clips = []
    for img in image_files:
        base_clip = ImageClip(img)
        
        # 🛑 बॉक्स को हटाकर 100% फुल स्क्रीन करना
        w, h = base_clip.size
        if w / h > 1080 / 1920:
            base_clip = base_clip.resize(height=1920)
        else:
            base_clip = base_clip.resize(width=1080)
            
        base_clip = base_clip.crop(x_center=base_clip.size[0]/2, y_center=base_clip.size[1]/2, width=1080, height=1920)
        base_clip = base_clip.set_duration(time_per_image)
        
        # 🛑 10% का धीरे-धीरे ज़ूम-इन इफ़ेक्ट
        zoomed_clip = base_clip.resize(lambda t: 1 + 0.1 * (t / time_per_image))
        
        final_clip = CompositeVideoClip([zoomed_clip.set_position(('center', 'center'))], size=(1080, 1920))
        final_clip = final_clip.set_duration(time_per_image)
        clips.append(final_clip)
        
    video = concatenate_videoclips(clips, method="compose")
    
    final_audio = main_audio
    if os.path.exists("bg_music.mp3"):
        bg_music = AudioFileClip("bg_music.mp3").fx(volumex, 0.1) 
        if bg_music.duration < main_audio.duration:
            bg_music = bg_music.fx(audio_loop, duration=main_audio.duration)
        else:
            bg_music = bg_music.subclip(0, main_audio.duration)
        final_audio = CompositeAudioClip([main_audio, bg_music])
        
    final = video.set_audio(final_audio).subclip(0, audio_duration)
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    
    main_audio.close()
    video.close()
    final.close()

# 6. यूट्यूब अपलोड
def upload_video(token, filename, title, description, tags, category):
    print(f"🚀 यूट्यूब पर वीडियो अपलोड हो रहा है...")
    credentials = Credentials(token=None, refresh_token=token, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token")
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "tags": tags, "categoryId": category},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        },
        media_body=MediaFileUpload(filename, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"✅ वीडियो लाइव है: https://www.youtube.com/watch?v={response['id']}\n")

# -- चैनल 1: Girish AI Gadgets --
def run_gadgets_channel():
    try:
        print("--- 📱 Girish AI Gadgets ---")
        script, prompts, gadget_name = get_script_and_prompts("a real, highly useful smart home gadget available on Amazon India under 1000 rupees", is_gadget=True)
        image_files = fetch_ai_images(prompts)
        create_human_voice(script, "voice_gadget.mp3")
        time.sleep(3)
        make_video(image_files, "final_gadget.mp4", "voice_gadget.mp3")
        
        # 🛑 डिस्क्रिप्शन में पक्का प्रोडक्ट का नाम
        if gadget_name:
            desc = f"🔥 👉 मेरी अमेज़न दुकान का लिंक: {AMAZON_ID}\n🔍 अमेज़न पर यह नाम सर्च करें: {gadget_name}\n\n{script}\n\n#gadgets #smarthome #amazonfinds"
        else:
            desc = f"🔥 👉 इसे यहाँ से खरीदें: {AMAZON_ID}\n\n{script}\n\n#gadgets #smarthome #amazonfinds"
            
        upload_video(TOKEN_GADGETS, "final_gadget.mp4", "Useful Amazon Gadget Under ₹1000! 🤯 #shorts", desc, ["shorts", "gadgets", "amazon finds"], "28")
    except Exception as e:
        print(f"❌ Gadgets चैनल एरर: {e}")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    try:
        print("--- 🌌 Mystic Universe ---")
        script, prompts, _ = get_script_and_prompts("a highly mysterious secret of the universe", is_gadget=False)
        image_files = fetch_ai_images(prompts)
        create_human_voice(script, "voice_mystic.mp3")
        time.sleep(3)
        make_video(image_files, "final_mystic.mp4", "voice_mystic.mp3")
        
        desc = f"{script}\n\n#space #universe #mystery #shorts"
        upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "The Biggest Space Secret! 🌌 #shorts", desc, ["shorts", "space", "universe"], "28")
    except Exception as e:
        print(f"❌ Mystic चैनल एरर: {e}")

# 7. मेन स्विच
if __name__ == "__main__":
    print("🚀 V3.3 AI इंजन स्टार्ट...")
    run_gadgets_channel()
    print("\n⏳ 60 सेकंड का ब्रेक...\n")
    time.sleep(60)
    run_mystic_channel()
    print("🎯 दोनों चैनलों का काम पूरा हो गया!")
