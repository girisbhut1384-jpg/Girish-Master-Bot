# गिरीश भाई का 2-इन-1 ऑटोमेशन एम्पायर (Gadgets + Mystic Universe)
import os
import random
import requests
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. तिजोरी से चाबियाँ निकालना
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
CLIENT_ID = "768932543756-30vbto7a15hqosjmpnbh99bfkbfsngj1.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_GADGETS = os.environ.get("YOUTUBE_REFRESH_TOKEN")
TOKEN_MYSTIC = os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC")
AMAZON_ID = os.environ.get("AMAZON_ID", "YOUR_AMAZON_LINK_HERE")

# 2. Gemini AI से स्क्रिप्ट लिखवाना (सख्त नियमों के साथ)
def get_ai_script(topic):
    print(f"Gemini AI '{topic}' पर स्क्रिप्ट लिख रहा है...")
    genai.configure(api_key=GEMINI_KEY)
    # सबसे स्टेबल और फास्ट दिमाग
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    prompt = f"Write a 30-second YouTube short script in Hindi about {topic}. ONLY provide the spoken Hindi voiceover text. DO NOT use English words, DO NOT use asterisks (*), brackets [], or hashtags. Just plain Hindi text."
    response = model.generate_content(prompt)
    
    # टेक्स्ट की सफाई ताकि आवाज़ वाली मशीन न अटके
    clean_text = response.text.replace("*", "").replace("#", "").replace("[", "").replace("]", "").strip()
    print(f"\n📝 [AI की लिखी स्क्रिप्ट]: {clean_text}\n")
    return clean_text

# 3. Pexels से असली HD वीडियो लाना
def get_hd_video(query, filename):
    print(f"Pexels से '{query}' का वीडियो लाया जा रहा है...")
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    response = requests.get(url, headers=headers).json()
    video_url = random.choice(response['videos'])['video_files'][0]['link']
    
    video_content = requests.get(video_url).content
    with open(filename, "wb") as f:
        f.write(video_content)

# 4. वीडियो और AI आवाज़ को जोड़ना (बुलेटप्रूफ सिस्टम)
def make_video(script_text, raw_vid, final_vid):
    print("AI आवाज़ बनाई जा रही है...")
    
    # अगर स्क्रिप्ट खाली आ जाए, तो बैकअप आवाज़
    if not script_text or len(script_text) < 5:
        script_text = "यह एक बहुत ही शानदार वीडियो है, इसे आखिर तक जरूर देखें और लाइक करें।"
        
    tts = gTTS(text=script_text, lang='hi', slow=False)
    tts.save("voice.mp3")
    
    print("वीडियो और आवाज़ को जोड़ा जा रहा है...")
    video = VideoFileClip(raw_vid)
    audio = AudioFileClip("voice.mp3")
    final = video.set_audio(audio).subclip(0, audio.duration)
    final.write_videofile(final_vid, codec="libx264", audio_codec="aac", fps=24, preset="ultrafast")

# 5. यूट्यूब पर डायरेक्ट अपलोड
def upload_video(token, filename, title, description, tags, category):
    print(f"यूट्यूब चैनल पर '{title}' अपलोड हो रहा है...")
    credentials = Credentials(
        token=None, refresh_token=token, client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, token_uri="https://oauth2.googleapis.com/token"
    )
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
    print(f"सफलता! वीडियो लाइव है: https://www.youtube.com/watch?v={response['id']}\n")

# -- चैनल 1: Girish AI Gadgets --
def run_gadgets_channel():
    print("--- 📱 Girish AI Gadgets चैनल चालू ---")
    script = get_ai_script("a cool AI or Tech Gadget")
    get_hd_video("tech gadget", "raw_gadget.mp4")
    make_video(script, "raw_gadget.mp4", "final_gadget.mp4")
    desc = script + f"\n\n👉 Buy Now (Amazon Link): {AMAZON_ID}\n#gadgets #ai #tech"
    upload_video(TOKEN_GADGETS, "final_gadget.mp4", "Unbelievable AI Gadget! 🤯 #shorts #tech", desc, ["shorts", "tech", "gadgets"], "28")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    print("--- 🌌 Mystic Universe चैनल चालू ---")
    script = get_ai_script("a mysterious space fact or universe secret")
    get_hd_video("space universe", "raw_mystic.mp4")
    make_video(script, "raw_mystic.mp4", "final_mystic.mp4")
    desc = script + "\n\n#space #universe #mystery #shorts"
    upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "Mind-Blowing Space Fact! 🌌 #shorts #space", desc, ["shorts", "space", "universe"], "28")

# 6. मेन स्विच
if __name__ == "__main__":
    try:
        run_gadgets_channel()
        run_mystic_channel()
        print("🎉 बधाई गिरीश भाई! दोनों चैनलों पर ऑटोमैटिक वीडियो डल गए! 🚀")
    except Exception as e:
        print(f"एरर आया: {e}")
