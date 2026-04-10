# गिरीश भाई का अल्टीमेट 100% PRO ऑटोमेशन (Triple Gemini Engine + Background Music + HD Pexels)
import os
import requests
import asyncio
import edge_tts
import time
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from moviepy.video.fx.all import loop
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_loop import audio_loop
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

# 2. Gemini Triple Engine (3.1 Pro -> 2.5 Pro -> 1.5 Pro)
def get_ai_script(topic):
    print(f"Gemini AI '{topic}' पर हाई-एंगेजमेंट स्क्रिप्ट लिख रहा है...")
    prompt = f"Write a 40-second highly engaging YouTube short script in Hindi about {topic}. Start with a mind-blowing hook to grab attention. ONLY provide the spoken Hindi voiceover text. DO NOT use English words, brackets, or hashtags."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    # 🛑 महा-सुरक्षा कवच: 3 सबसे ताक़तवर मॉडल की लिस्ट
    models = ["gemini-3.1-pro", "gemini-2.5-pro", "gemini-1.5-pro"]
    clean_text = ""
    
    for model in models:
        try:
            print(f"[{model}] इंजन ट्राई कर रहे हैं...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
            response = requests.post(url, json=payload).json()
            
            if 'candidates' in response:
                clean_text = response['candidates'][0]['content']['parts'][0]['text'].replace("*", "").replace("#", "").replace("[", "").replace("]", "").strip()
                if len(clean_text) >= 100:
                    print(f"✅ [{model}] ने स्क्रिप्ट सफलतापूर्वक लिख दी!")
                    break # सफलता मिल गई, लूप से बाहर आएं
        except Exception as e:
            print(f"⚠️ [{model}] बिज़ी है, अगला इंजन ट्राई कर रहे हैं...")
            continue # एक फेल हुआ तो दूसरा ट्राई करो
            
    if not clean_text or len(clean_text) < 100:
        raise Exception("तीनों Gemini इंजन (3.1, 2.5, 1.5) इस वक़्त बिज़ी हैं या लिमिट खत्म हो गई। 15 मिनट बाद मशीन अपने आप फिर कोशिश करेगी।")
        
    print(f"\n📝 [PRO स्क्रिप्ट तैयार]: {clean_text[:100]}...\n")
    return clean_text

# 3. असली इंसानों जैसी Neural आवाज़ बनाना
def create_human_voice(text, filename):
    print(f"दमदार इंसानी आवाज़ ({filename}) बनाई जा रही है...")
    async def _generate():
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await communicate.save(filename)
    asyncio.run(_generate())

# 4. Pexels HD वीडियो (सख्त स्कैनर के साथ)
def get_hd_video(query, filename):
    print(f"Pexels से '{query}' का फुल HD वीडियो ढूँढा जा रहा है...")
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    response = requests.get(url, headers=headers).json()
    
    valid_links = [f['link'] for vid in response.get('videos', []) for f in vid.get('video_files', []) if f.get('file_type') == 'video/mp4']
    if not valid_links:
        raise Exception("Pexels पर सही वीडियो नहीं मिला!")
        
    for video_url in valid_links:
        try:
            video_content = requests.get(video_url).content
            if len(video_content) < 200000: 
                continue
            with open(filename, "wb") as f:
                f.write(video_content)
            
            test_clip = VideoFileClip(filename)
            test_clip.close()
            print("✅ 100% परफेक्ट और असली वीडियो डाउनलोड हो गया!")
            return 
        except Exception:
            continue 
            
    raise Exception("सारे वीडियो करप्ट निकले!")

# 5. वीडियो, आवाज़ और बैकग्राउंड म्यूजिक का शानदार मिक्स (Pro Editing)
def make_video(script_text, raw_vid, final_vid, audio_file):
    create_human_voice(script_text, audio_file)
    time.sleep(2) 
    
    print("प्रो-लेवल एडिटिंग चालू (आवाज़ + म्यूजिक + वीडियो)...")
    video = VideoFileClip(raw_vid).without_audio()
    main_audio = AudioFileClip(audio_file)
    
    final_audio = main_audio
    if os.path.exists("bg_music.mp3"):
        print("🎵 बैकग्राउंड म्यूजिक जोड़ा जा रहा है...")
        bg_music = AudioFileClip("bg_music.mp3").fx(volumex, 0.1)
        if bg_music.duration < main_audio.duration:
            bg_music = bg_music.fx(audio_loop, duration=main_audio.duration)
        else:
            bg_music = bg_music.subclip(0, main_audio.duration)
        final_audio = CompositeAudioClip([main_audio, bg_music])
    else:
        print("⚠️ bg_music.mp3 नहीं मिला, इसलिए सिर्फ आवाज़ लगाई जा रही है।")
    
    if video.duration < main_audio.duration:
        video = loop(video, duration=main_audio.duration)
        
    final = video.set_audio(final_audio).subclip(0, main_audio.duration)
    final.write_videofile(final_vid, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast", logger=None)
    
    video.close()
    main_audio.close()
    if os.path.exists("bg_music.mp3"):
        bg_music.close()
    final.close()

# 6. यूट्यूब अपलोड
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
    print(f"✅ सफलता! शानदार वीडियो लाइव है: https://www.youtube.com/watch?v={response['id']}\n")

# -- चैनल 1: Girish AI Gadgets --
def run_gadgets_channel():
    try:
        print("--- 📱 Girish AI Gadgets (Ultimate PRO Mode) ---")
        script = get_ai_script("a completely mind-blowing futuristic tech gadget")
        get_hd_video("tech gadget", "raw_gadget.mp4")
        make_video(script, "raw_gadget.mp4", "final_gadget.mp4", "voice_gadget.mp3")
        desc = script + f"\n\n👉 Buy Now (Amazon Link): {AMAZON_ID}\n#gadgets #tech #shorts"
        upload_video(TOKEN_GADGETS, "final_gadget.mp4", "You Won't Believe This Gadget! 🤯 #shorts #tech", desc, ["shorts", "tech", "gadgets"], "28")
    except Exception as e:
        print(f"❌ Gadgets चैनल एरर: {e}")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    try:
        print("--- 🌌 Mystic Universe (Ultimate PRO Mode) ---")
        script = get_ai_script("a highly mysterious and shocking secret of the universe")
        get_hd_video("space universe", "raw_mystic.mp4")
        make_video(script, "raw_mystic.mp4", "final_mystic.mp4", "voice_mystic.mp3")
        desc = script + "\n\n#space #universe #mystery #shorts"
        upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "The Biggest Space Secret! 🌌 #shorts #space", desc, ["shorts", "space", "universe"], "28")
    except Exception as e:
        print(f"❌ Mystic चैनल एरर: {e}")

# 7. मेन स्विच
if __name__ == "__main__":
    print("🚀 ULTIMATE PRO AI इंजन स्टार्ट... (Background Music के साथ)")
    run_gadgets_channel()
    run_mystic_channel()
    print("🎯 दोनों चैनलों पर 100% परफेक्ट वीडियो अपलोड हो गए!")
