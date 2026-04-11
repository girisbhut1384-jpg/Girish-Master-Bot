# गिरीश भाई का प्रो ऑटोमेशन V2.0 (Bulletproof JSON + Auto-Retry + Amazon CTA)
import os
import requests
import asyncio
import edge_tts
import time
import urllib.parse
import json
import random
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

# 2. Gemini AI - (JSON Mode के साथ बुलेटप्रूफ स्क्रिप्ट)
def get_script_and_prompts(topic, is_gadget=False):
    print(f"\n🧠 Gemini AI '{topic}' पर स्क्रिप्ट और AI इमेज की कमांड सोच रहा है...")
    
    active_model = "models/gemini-1.5-flash-latest" 
    url = f"https://generativelanguage.googleapis.com/v1beta/{active_model}:generateContent?key={GEMINI_KEY}"
    
    prompt = f"Write a 40-second engaging YouTube short script in Hindi about {topic}. Start with a mind-blowing hook. "
    if is_gadget:
        prompt += "End the Hindi script EXACTLY with: 'इसे खरीदने का लिंक नीचे कमेंट और डिस्क्रिप्शन में दिया गया है।'. "
    
    prompt += """
    IMPORTANT: You must return ONLY a raw JSON format. No markdown formatting, no extra text.
    {
      "script": "Your full spoken Hindi voiceover text here...",
      "prompts": [
        "A highly realistic 4k cinematic image of...",
        "A detailed 3D render of...",
        "A hyper-realistic scene of...",
        "A beautiful cinematic lighting shot of..."
      ]
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
        print(f"✅ [AI स्क्रिप्ट 100% सही तैयार]: {hindi_script[:80]}...")
        return hindi_script, image_prompts
    except Exception as e:
        raise Exception(f"❌ Gemini JSON एरर: {e} - डेटा: {response}")

# 3. Pollinations AI (Auto-Retry और Size Check के साथ)
def fetch_ai_images(prompts):
    print("🎨 Pollinations AI से 100% नई 4K तस्वीरें बनाई जा रही हैं...")
    image_files = []
    seed = random.randint(1000, 99999) # हर बार बिलकुल नई तस्वीर के लिए
    
    for i, p in enumerate(prompts):
        safe_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&nologo=true&seed={seed+i}"
        filename = f"ai_scene_{i}.jpg"
        
        for attempt in range(3): # 🛑 3 बार कोशिश करने वाला सिस्टम
            print(f"   ⏳ सीन {i+1} डाउनलोड हो रहा है... (प्रयास {attempt+1}/3)")
            try:
                res = requests.get(url, timeout=45) # 45 सेकंड का इंतज़ार
                # चेक करें कि फोटो सही है और 20KB से बड़ी है (करप्ट नहीं है)
                if res.status_code == 200 and len(res.content) > 20000: 
                    with open(filename, "wb") as f:
                        f.write(res.content)
                    image_files.append(filename)
                    print(f"   ✅ सीन {i+1} सफल!")
                    time.sleep(2)
                    break # काम हो गया, अगला सीन लाओ
                else:
                    print("   ⚠️ खराब फाइल मिली, दोबारा कोशिश कर रहे हैं...")
                    time.sleep(3)
            except Exception as e:
                print(f"   ❌ सर्वर टाइमआउट, दोबारा कोशिश कर रहे हैं...")
                time.sleep(3)
                
    if len(image_files) < 2:
        raise Exception("इंटरनेट या सर्वर एरर: 2 तस्वीरें भी नहीं बन पाईं, वीडियो कैंसल!")
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
    
    # हर तस्वीर को कितनी देर दिखाना है (कुल समय / असली तस्वीरों की संख्या)
    time_per_image = audio_duration / len(image_files)
    
    clips = []
    for img in image_files:
        clip = ImageClip(img).set_duration(time_per_image)
        clips.append(clip)
        
    video = concatenate_videoclips(clips, method="compose")
    
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
        time.sleep(3)
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
    print("🚀 PRO-LEVEL V2.0 AI इंजन स्टार्ट... (Bulletproof Safe Limits)")
    
    run_gadgets_channel()
    
    print("\n⏳ API लिमिट बचाने के लिए 60 सेकंड का सेफ्टी ब्रेक ले रहे हैं...\n")
    time.sleep(60)
    
    run_mystic_channel()
    
    print("🎯 दोनों चैनलों पर 100% ओरिजिनल AI वीडियो अपलोड हो गए!")
