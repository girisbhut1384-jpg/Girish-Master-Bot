import os
import random
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("="*85)
print("🎯 🧬 THE ULTIMATE 5-CHANNEL VIDEO PRODUCTION ENGINE (MAIN.PY) 🧬 🎯")
print("="*85)

# ==========================================
# 🔑 गिटहब सीक्रेट्स से ऑटोमैटिक चाबियां लेना
# ==========================================
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# आपके 5 चैनलों के टोकन जो गिटहब सीक्रेट्स में सुरक्षित हैं
channel_tokens = {
    "MYSTERY CHANNEL": os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC"),
    "AI AUTO PILOT EMPIRE": os.environ.get("YOUTUBE_TOKEN_EMPIRE"),
    "GIRISH AI GADGET": os.environ.get("YOUTUBE_TOKEN_GADGET"),
    "HEALTH & AYURVEDA": os.environ.get("YOUTUBE_TOKEN_HEALTH"),
    "ZEROTOUCH AI CREATOR": os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH")
}

# ==========================================
# 📝 40-सेकंड की हाई-रिटेंशन कहानी (वायरल स्क्रिप्ट्स)
# ==========================================
stories = [
    {
        "title": "चिल्लाती हुई तिजोरी का रहस्य",
        "script": "क्या आप जानते हैं कि दुनिया में एक ऐसी तिजोरी भी है जो हर रात ठीक दो बजे अपने आप खुल जाती है? वैज्ञानिकों ने सालों रिसर्च की, कैमरे लगाए, लेकिन रहस्य नहीं खुला। सबसे हैरान करने वाली बात यह है कि इसके अंदर कोई खजाना नहीं, बल्कि सिर्फ एक खाली पुरानी डायरी रखी है। इसके आखिरी पन्ने पर क्या लिखा है, जानना चाहते हैं? नीचे कमेंट में पार्ट 2 लिखें!",
        "keyword": "mystery dark vault"
    },
    {
        "title": "अमीरी का सबसे गुप्त नियम",
        "script": "दुनिया के 99% अमीर लोग रात को सोने से पहले एक खास काम करते हैं, जिसे 'द सीक्रेट स्क्रिप्टिंग' कहा जाता है। वे कल होने वाली जीतों को आज ही अपनी डायरी में लिख लेते हैं। यह कोई जादू नहीं, बल्कि आपके दिमाग को री-वायर करने की वैज्ञानिक तकनीक है। आज रात से ही इसे आजमाएं और तीन दिन में खुद चमत्कार देखें। ऐसे ही सीक्रेट्स के लिए सब्सक्राइब करें!",
        "keyword": "wealth luxury success"
    },
    {
        "title": "मानव शरीर का सबसे बड़ा झूठ",
        "script": "हमें बचपन से सिखाया गया है कि हमारा दिमाग सिर्फ 10 प्रतिशत काम करता है, लेकिन यह विज्ञान का सबसे बड़ा झूठ है। असल में, जब आप गहरी नींद में होते हैं, तब भी आपका दिमाग एक सुपरकंप्यूटर से ज्यादा तेजी से आपकी पुरानी यादों को फिल्टर कर रहा होता है। आपकी एक छोटी सी आदत आपके दिमाग की ताकत को 10 गुना बढ़ा सकती है। जानिए कैसे, हमारे अगले वीडियो में!",
        "keyword": "human brain science"
    }
]

# ==========================================
# 🖼️ इमेज और 🎙️ ऑडियो जनरेशन इंजन
# ==========================================
def create_media_assets(story):
    print(f"\n🎬 चुनी गई कहानी: {story['title']}")
    
    # 1. ऑडियो बनाना (gTTS)
    print("🎙️ आवाज रिकॉर्ड की जा रही है...")
    audio_path = "voice.mp3"
    tts = gTTS(text=story['script'], lang='hi', slow=False)
    tts.save(audio_path)
    
    # 2. इमेज डाउनलोड करना
    print("📸 हाई-क्वालिटी बैकग्राउंड इमेज डाउनलोड की जा रही है...")
    image_path = "background.jpg"
    # Unsplash से रैंडम 1080x1920 इमेज
    image_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1080&auto=format&fit=crop"
    
    response = requests.get(image_url)
    with open(image_path, 'wb') as file:
        file.write(response.content)
        
    return audio_path, image_path

# ==========================================
# 🎬 वीडियो एडिटिंग और सिंकिंग इंजन (MoviePy)
# ==========================================
def render_video(audio_path, image_path):
    print("\n🖥️ वीडियो रेंडरिंग चालू: इमेज और आवाज को परफेक्ट सिंक किया जा रहा है...")
    output_path = "final_viral_shorts.mp4"
    
    # ऑडियो फाइल लोड करें
    audio_clip = AudioFileClip(audio_path)
    
    # इमेज को लोड करें और ऑडियो की लंबाई के बराबर सेट करें
    image_clip = ImageClip(image_path)
    image_clip = image_clip.set_duration(audio_clip.duration)
    
    # यूट्यूब शॉर्ट्स का साइज (1080x1920)
    image_clip = image_clip.resize(height=1920, width=1080)
    
    # इमेज और ऑडियो को मिला दें
    video_clip = image_clip.set_audio(audio_clip)
    
    # फाइनल mp4 बनाएं (24 FPS)
    video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    print(f"✅ वीडियो 100% परफेक्ट बन गया है: {output_path}")
    
    return output_path, audio_clip.duration

# ==========================================
# 🚀 यूट्यूब ऑटो-अपलोडर इंजन
# ==========================================
def upload_to_youtube(video_file, story_title, story_tags, channel_name, refresh_token):
    if not refresh_token:
        print(f"⚠️ {channel_name} का टोकन नहीं मिला। इसे छोड़ रहे हैं।")
        return

    print(f"\n📡 {channel_name} पर वीडियो अपलोड किया जा रहा है...")
    
    # क्रेडेंशियल्स बनाना
    credentials = Credentials(
        None,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token"
    )
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    # वीडियो का डेटा
    body = {
        "snippet": {
            "title": f"{story_title} #shorts #viral",
            "description": f"{story_title}\n\nरोजाना ऐसे ही रहस्यों और जानकारी के लिए सब्सक्राइब करें!\n#shorts #trending",
            "tags": story_tags.split(" "),
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public", # सीधे पब्लिक करने के लिए
            "selfDeclaredMadeForKids": False
        }
    }
    
    # अपलोड कमांड
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    try:
        response = request.execute()
        print(f"🟢 सफलता! {channel_name} पर वीडियो लाइव हो गया: https://youtu.be/{response['id']}")
    except Exception as e:
        print(f"🔴 अपलोड फेल हुआ {channel_name}: {e}")

# ==========================================
# ⚙️ मेन एग्जीक्यूशन (इंजन स्टार्ट)
# ==========================================
if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("🛑 एरर: गिटहब सीक्रेट्स में CLIENT_ID या GOOGLE_CLIENT_SECRET नहीं मिला!")
        exit(1)
        
    # 1. कहानी चुनें
    selected_story = random.choice(stories)
    
    # 2. एसेट्स (आवाज और फोटो) बनाएं
    audio_file, image_file = create_media_assets(selected_story)
    
    # 3. फाइनल वीडियो बनाएं
    final_video, duration = render_video(audio_file, image_file)
    print(f"⏱️ वीडियो की कुल लंबाई: {round(duration, 2)} सेकंड")
    
    # 4. पांचों चैनलों पर अपलोड करें
    for channel, token in channel_tokens.items():
        upload_to_youtube(final_video, selected_story['title'], selected_story['keyword'], channel, token)
        
    print("\n" + "="*85)
    print("🏆 मिशन 100% सक्सेसफुल! सभी प्रक्रियाएं पूरी हो गईं।")
    print("="*85)
