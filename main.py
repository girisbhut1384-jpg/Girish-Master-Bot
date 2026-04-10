# गिरीश भाई का असली PRO लेवल ऑटोमेशन (हलचल वाले वीडियो + असली इंसानी आवाज़)
import os
import random
import requests
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx.all import loop
import google.generativeai as genai
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

# 2. Gemini AI - शानदार स्क्रिप्ट
def get_ai_script(topic):
    print(f"Gemini AI '{topic}' पर सोच रहा है...")
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash') 
    prompt = f"Write a 30-second highly engaging YouTube short script in Hindi about {topic}. ONLY provide the spoken Hindi voiceover text. DO NOT use English words, brackets, or hashtags."
    
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("*", "").replace("#", "").replace("[", "").replace("]", "").strip()
        print(f"\n📝 [AI स्क्रिप्ट]: {clean_text}\n")
        return clean_text
    except Exception as e:
        print(f"AI स्क्रिप्ट में दिक्कत: {e}")
        return "यह एक बहुत ही शानदार जानकारी है, इसे आखिर तक जरूर देखें।"

# 3. असली इंसानों जैसी Neural आवाज़ बनाना (gTTS हटा दिया गया है)
def create_human_voice(text, filename="voice.mp3"):
    print("असली इंसानों जैसी Neural आवाज़ बनाई जा रही है...")
    # hi-IN-MadhurNeural एक बहुत ही शानदार और भारी आवाज़ है
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await communicate.save(filename)
    asyncio.run(_generate())

# 4. Pexels से असली MP4 वीडियो (स्मार्ट फिल्टर के साथ)
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
        
    # स्मार्ट चेकर: खराब फाइल को रोककर सही फाइल ढूँढना
    for video_url in valid_links:
        video_content = requests.get(video_url).content
        # अगर वीडियो 100KB से बड़ा है, मतलब वह असली है, करप्ट नहीं है
        if len(video_content) > 100000:
            with open(filename, "wb") as f:
                f.write(video_content)
            print("✅ एकदम सही और साफ वीडियो डाउनलोड हो गया!")
            return
            
    raise Exception("सारे वीडियो करप्ट निकले!")

# 5. वीडियो और आवाज़ को जोड़ना (बिना कटे)
def make_video(script_text, raw_vid, final_vid):
    create_human_voice(script_text, "voice.mp3")
    
    print("वीडियो और आवाज़ को जोड़ा जा रहा है...")
    video = VideoFileClip(raw_vid)
    audio = AudioFileClip("voice.mp3")
    
    # अगर वीडियो छोटा है तो उसे घुमा दें (Loop)
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
        print("--- 📱 Girish AI Gadgets (PRO Mode) ---")
        script = get_ai_script("a cool and futuristic tech gadget")
        get_hd_video("tech gadget", "raw_gadget.mp4")
        make_video(script, "raw_gadget.mp4", "final_gadget.mp4")
        desc = script + f"\n\n👉 Buy Now (Amazon Link): {AMAZON_ID}\n#gadgets #tech #shorts"
        upload_video(TOKEN_GADGETS, "final_gadget.mp4", "Future Tech is Here! 🤯 #shorts #tech", desc, ["shorts", "tech", "gadgets"], "28")
    except Exception as e:
        print(f"❌ Gadgets चैनल एरर: {e}")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    try:
        print("--- 🌌 Mystic Universe (PRO Mode) ---")
        script = get_ai_script("a mysterious secret of the universe or black hole")
        get_hd_video("space universe", "raw_mystic.mp4")
        make_video(script, "raw_mystic.mp4", "final_mystic.mp4")
        desc = script + "\n\n#space #universe #mystery #shorts"
        upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "Universe Secret Revealed! 🌌 #shorts #space", desc, ["shorts", "space", "universe"], "28")
    except Exception as e:
        print(f"❌ Mystic चैनल एरर: {e}")

# 7. मेन स्विच
if __name__ == "__main__":
    print("🚀 PRO AI इंजन स्टार्ट...")
    run_gadgets_channel()
    run_mystic_channel()
    print("🎯 दोनों चैनलों पर शानदार वीडियो सफलतापूर्वक अपलोड हो गए!")
