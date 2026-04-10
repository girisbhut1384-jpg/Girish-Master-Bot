# गिरीश भाई का 100% परफेक्ट गोल ऑटोमेशन (Strict Mode - No Garbage Video)
import os
import random
import requests
import asyncio
import edge_tts
import time
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx.all import loop
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. तिजोरी से आपकी चाबियाँ
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = os.environ.get("AMAZON_ID", "YOUR_AMAZON_LINK_HERE")

# 2. Gemini AI - डायरेक्ट API (सख्त चेकिंग के साथ)
def get_ai_script(topic):
    print(f"Gemini AI '{topic}' पर सोच रहा है...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_KEY}"
    prompt = f"Write a 40-second highly engaging YouTube short script in Hindi about {topic}. ONLY provide the spoken Hindi voiceover text. DO NOT use English words, brackets, or hashtags. Tell a complete story."
    
    try:
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload).json()
        raw_text = response['candidates'][0]['content']['parts'][0]['text']
        clean_text = raw_text.replace("*", "").replace("#", "").replace("[", "").replace("]", "").strip()
        
        # 🛑 सख्त पहरेदार: अगर स्क्रिप्ट बहुत छोटी है, तो कचरा वीडियो नहीं बनेगा!
        if len(clean_text) < 100:
            raise Exception(f"AI ने बहुत छोटी स्क्रिप्ट दी ({len(clean_text)} अक्षर)। कचरा वीडियो अपलोड नहीं किया जाएगा!")
            
        print(f"\n📝 [AI स्क्रिप्ट पास हो गई]: {clean_text[:100]}...\n")
        return clean_text
    except Exception as e:
        # यहाँ मशीन रुक जाएगी और एरर बता देगी, कोई बैकअप डायलॉग नहीं!
        raise Exception(f"AI स्क्रिप्ट फेल हो गई: {e}")

# 3. असली इंसानों जैसी Neural आवाज़ बनाना
def create_human_voice(text, filename="voice.mp3"):
    print("असली इंसानों जैसी Neural आवाज़ बनाई जा रही है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await communicate.save(filename)
    asyncio.run(_generate())

# 4. Pexels से असली वीडियो (सख्त स्कैनर के साथ)
def get_hd_video(query, filename):
    print(f"Pexels से '{query}' का असली वीडियो लाया जा रहा है...")
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    response = requests.get(url, headers=headers).json()
    
    valid_links = []
    for vid in response.get('videos', []):
        for file in vid.get('video_files', []):
            if file.get('file_type') == 'video/mp4':
                valid_links.append(file['link'])
                
    if not valid_links:
        raise Exception("Pexels पर सही वीडियो नहीं मिला!")
        
    # 🛑 सख्त पहरेदार: सिर्फ सही और बिना करप्ट हुआ वीडियो ही डाउनलोड होगा
    for video_url in valid_links:
        try:
            video_content = requests.get(video_url).content
            if len(video_content) < 200000: # 200KB से छोटा वीडियो कचरा होता है
                continue
                
            with open(filename, "wb") as f:
                f.write(video_content)
            
            test_clip = VideoFileClip(filename)
            test_clip.close()
            print("✅ एकदम सही, साफ और टेस्टेड वीडियो डाउनलोड हो गया!")
            return 
        except Exception:
            continue 
            
    raise Exception("Pexels के सारे वीडियो करप्ट निकले, मशीन को रोक दिया गया है!")

# 5. वीडियो और आवाज़ को जोड़ना
def make_video(script_text, raw_vid, final_vid):
    create_human_voice(script_text, "voice.mp3")
    time.sleep(2) # फाइल सेव होने के लिए सेफ्टी ब्रेक
    
    print("वीडियो और आवाज़ को जोड़ा जा रहा है...")
    video = VideoFileClip(raw_vid)
    audio = AudioFileClip("voice.mp3")
    
    if video.duration < audio.duration:
        video = loop(video, duration=audio.duration)
        
    final = video.set_audio(audio).subclip(0, audio.duration)
    final.write_videofile(final_vid, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast", logger=None)
    
    video.close()
    audio.close()
    final.close()

# 6. यूट्यूब पर डायरेक्ट अपलोड
def upload_video(token, filename, title, description, tags, category):
    print(f"यूट्यूब चैनल पर '{title}' अपलोड हो रहा है...")
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
    print(f"✅ सफलता! वीडियो लाइव है: https://www.youtube.com/watch?v={response['id']}\n")

# -- चैनल 1: Girish AI Gadgets --
def run_gadgets_channel():
    try:
        print("--- 📱 Girish AI Gadgets (Strict Goal Mode) ---")
        script = get_ai_script("a highly advanced futuristic AI tech gadget")
        get_hd_video("tech gadget", "raw_gadget.mp4")
        make_video(script, "raw_gadget.mp4", "final_gadget.mp4")
        desc = script + f"\n\n👉 Buy Now (Amazon Link): {AMAZON_ID}\n#gadgets #tech #shorts"
        upload_video(TOKEN_GADGETS, "final_gadget.mp4", "Future Tech is Here! 🤯 #shorts #tech", desc, ["shorts", "tech", "gadgets"], "28")
    except Exception as e:
        print(f"❌ Gadgets चैनल में एरर आया: {e}")
        print("⚠️ कचरा वीडियो अपलोड होने से रोक दिया गया है!")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    try:
        print("--- 🌌 Mystic Universe (Strict Goal Mode) ---")
        script = get_ai_script("a mind-blowing dark secret of the universe or black hole")
        get_hd_video("space universe", "raw_mystic.mp4")
        make_video(script, "raw_mystic.mp4", "final_mystic.mp4")
        desc = script + "\n\n#space #universe #mystery #shorts"
        upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "Universe Secret Revealed! 🌌 #shorts #space", desc, ["shorts", "space", "universe"], "28")
    except Exception as e:
        print(f"❌ Mystic चैनल में एरर आया: {e}")
        print("⚠️ कचरा वीडियो अपलोड होने से रोक दिया गया है!")

# 7. मेन स्विच
if __name__ == "__main__":
    print("🚀 STRICT PRO AI इंजन स्टार्ट... (सिर्फ परफेक्ट वीडियो ही अपलोड होंगे)")
    run_gadgets_channel()
    run_mystic_channel()
    print("🎯 आज का काम खत्म!")
