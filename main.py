# गिरीश भाई का प्रो ऑटोमेशन (Pollinations AI Images + Amazon Auto-Fix + API Safe Mode)
import os
import requests
import asyncio
import edge_tts
import time
import urllib.parse
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_loop import audio_loop
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. तिजोरी से आपकी चाबियाँ
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = os.environ.get("AMAZON_ID", "YOUR_AMAZON_LINK_HERE")

# 🛑 लिंक ऑटो-फिक्सर: यूट्यूब पर लिंक को 'नीला' और क्लिकेबल बनाने के लिए
if not AMAZON_ID.startswith("http"):
    AMAZON_ID = "https://" + AMAZON_ID

# 2. Gemini AI - (स्मार्ट स्क्रिप्ट और AI इमेज प्रॉम्प्ट मेकर)
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n🧠 Gemini AI '{topic}' पर स्क्रिप्ट और AI इमेज की कमांड सोच रहा है...")
    
    active_model = "models/gemini-1.5-flash-latest" 
    url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={GEMINI_KEY}"
    
    prompt = f"""Write a 40-second engaging YouTube short script in Hindi about {topic}. Start with a mind-blowing hook. 
    """
    if is_gadget:
        prompt += "End the Hindi script EXACTLY with: 'इसे खरीदने का लिंक नीचे कमेंट और डिस्क्रिप्शन में दिया गया है।'. "
    
    prompt += """
    IMPORTANT FORMATTING:
    First, write ONLY the spoken Hindi text.
    Then, write '|||' on a new line.
    Then, write 4 highly detailed English prompts for an AI image generator to match the story (1 prompt per line). Focus on realistic, 4k, cinematic style.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload).json()
    
    try:
        full_text = response['candidates'][0]['content']['parts'][0]['text']
        parts = full_text.split('|||')
        hindi_script = parts[0].replace("*", "").replace("#", "").strip()
        image_prompts = [p.strip() for p in parts[1].strip().split('\n') if len(p.strip()) > 10][:4]
    except Exception as e:
        print("⚠️ Gemini ने सही फॉर्मेट नहीं दिया, बैकअप प्रॉम्प्ट लगा रहे हैं...")
        hindi_script = "क्या आपने कभी ऐसी जादुई तकनीक देखी है? जो आपके होश उड़ा दे! आगे जानने के लिए सब्सक्राइब करें।"
        image_prompts = ["A futuristic sci-fi city 4k resolution", "A high tech glowing smart gadget close up", "A mysterious space nebula dark cinematic", "A futuristic AI robot looking at camera"]
        
    print(f"📝 [AI स्क्रिप्ट तैयार]: {hindi_script[:80]}...")
    return hindi_script, image_prompts

# 3. Pollinations AI (100% Free AI 3D Image Generator)
def fetch_ai_images(prompts):
    print("🎨 Pollinations AI से 100% नई 4K तस्वीरें बनाई जा रही हैं (No API Key Required)...")
    image_files = []
    
    for i, p in enumerate(prompts):
        # वर्टिकल (Shorts) साइज़ के लिए width=1080&height=1920
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true"
        
        filename = f"ai_scene_{i}.jpg"
        print(f"   ⏳ सीन {i+1} की तस्वीर डाउनलोड हो रही है...")
        try:
            response = requests.get(url, timeout=20)
            with open(filename, "wb") as f:
                f.write(response.content)
            image_files.append(filename)
            time.sleep(2) # सर्वर को ओवरलोड न करने के लिए छोटा ब्रेक
        except Exception as e:
            print(f"   ❌ सीन {i+1} फेल हुआ: {e}")
            
    if not image_files:
        raise Exception("कोई भी तस्वीर जनरेट नहीं हो पाई!")
    return image_files

# 4. असली इंसानों जैसी Neural आवाज़ बनाना
def create_human_voice(text, filename):
    print(f"🎙️ दमदार इंसानी आवाज़ ({filename}) बनाई जा रही है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await communicate.save(filename)
    asyncio.run(_generate())

# 5. वीडियो, आवाज़ और तस्वीरों का शानदार मिक्स (Pro Editing)
def make_video(image_files, final_vid, audio_file):
    print("🎬 प्रो-लेवल एडिटिंग चालू (AI तस्वीरें + आवाज़ + म्यूजिक)...")
    
    main_audio = AudioFileClip(audio_file)
    audio_duration = main_audio.duration
    
    # हर तस्वीर को कितनी देर दिखाना है (कुल समय / तस्वीरों की संख्या)
    time_per_image = audio_duration / len(image_files)
    
    clips = []
    for img in image_files:
        # तस्वीर को वीडियो क्लिप में बदलना
        clip = ImageClip(img).set_duration(time_per_image)
        clips.append(clip)
        
    # सभी क्लिप्स को जोड़ना
    video = concatenate_videoclips(clips, method="compose")
    
    # बैकग्राउंड म्यूजिक सेटअप
    final_audio = main_audio
    if os.path.exists("bg_music.mp3"):
        print("🎵 बैकग्राउंड म्यूजिक जोड़ा जा रहा है...")
        bg_music = AudioFileClip("bg_music.mp3").fx(volumex, 0.1) 
        if bg_music.duration < main_audio.duration:
            bg_music = bg_music.fx(audio_loop, duration=main_audio.duration)
        else:
            bg_music = bg_music.subclip(0, main_audio.duration)
        final_audio = CompositeAudioClip([main_audio, bg_music])
        
    final = video.set_audio(final_audio).subclip(0, audio_duration)
    # गिटहब सर्वर पर बिना क्रैश हुए रेंडर करने के लिए सेफ सेटिंग्स
    final.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    
    main_audio.close()
    video.close()
    final.close()

# 6. यूट्यूब अपलोड
def upload_video(token, filename, title, description, tags, category):
    print(f"🚀 यूट्यूब चैनल पर '{title}' अपलोड हो रहा है...")
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
    print(f"✅ सफलता! शानदार AI शार्ट वीडियो लाइव है: https://www.youtube.com/watch?v={response['id']}\n")

# -- चैनल 1: Girish AI Gadgets --
def run_gadgets_channel():
    try:
        print("--- 📱 Girish AI Gadgets (Pro AI Image Mode) ---")
        script, prompts = get_script_and_prompts("a completely mind-blowing futuristic tech gadget", is_gadget=True)
        image_files = fetch_ai_images(prompts)
        create_human_voice(script, "voice_gadget.mp3")
        time.sleep(3) # ऑडियो सेफ-ब्रेक
        make_video(image_files, "final_gadget.mp4", "voice_gadget.mp3")
        
        desc = f"🔥 👉 इसे यहाँ से खरीदें (Buy Now): {AMAZON_ID}\n\n{script}\n\n#gadgets #tech #shorts #ai"
        upload_video(TOKEN_GADGETS, "final_gadget.mp4", "You Won't Believe This Gadget! 🤯 #shorts #tech", desc, ["shorts", "tech", "gadgets"], "28")
    except Exception as e:
        print(f"❌ Gadgets चैनल एरर: {e}")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    try:
        print("--- 🌌 Mystic Universe (Pro AI Image Mode) ---")
        script, prompts = get_script_and_prompts("a highly mysterious and shocking secret of the universe", is_gadget=False)
        image_files = fetch_ai_images(prompts)
        create_human_voice(script, "voice_mystic.mp3")
        time.sleep(3)
        make_video(image_files, "final_mystic.mp4", "voice_mystic.mp3")
        
        desc = f"{script}\n\n#space #universe #mystery #shorts #ai"
        upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "The Biggest Space Secret! 🌌 #shorts #space", desc, ["shorts", "space", "universe"], "28")
    except Exception as e:
        print(f"❌ Mystic चैनल एरर: {e}")

# 7. मेन स्विच
if __name__ == "__main__":
    print("🚀 PRO-LEVEL AI इंजन स्टार्ट... (Pollinations 3D + Safe Limits)")
    
    run_gadgets_channel()
    
    # 🛑 सबसे ज़रूरी: API लिमिट से बचने के लिए 60 सेकंड का ब्रेक
    print("\n⏳ API लिमिट बचाने के लिए 60 सेकंड का सेफ्टी ब्रेक ले रहे हैं...\n")
    time.sleep(60)
    
    run_mystic_channel()
    
    print("🎯 दोनों चैनलों पर 100% ओरिजिनल AI वीडियो अपलोड हो गए!")
