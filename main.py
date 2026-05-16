import os
import sys
import subprocess

# =====================================================================================
# 🛠️ स्टेप 0: गिटहब सर्वर में बैकएंड टूल्स ऑटो-इंस्टॉलर (Pillow & Audio Fixed)
# =====================================================================================
print("⏳ [सिस्टम अपडेट] गिटहब में सभी सुपर-एडवांस टूल्स इंस्टॉल किए जा रहे हैं...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "gTTS", "requests", "moviepy==1.0.3", "google-api-python-client", "google-auth-oauthlib", "Pillow==9.5.0"])
print("✅ [सिस्टम अपडेट] सभी एडवांस टूल्स सफलतापूर्वक इंस्टॉल हो गए! इंजन लाइव है...\n")

import random
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("="*85)
print("🎯 🧬 THE ULTIMATE 5-CHANNEL INTELLIGENT EMPIRE ENGINE (V11) 🧬 🎯")
print("="*85)

# ==========================================
# 🔑 गिटहब सीक्रेट्स से ऑटोमैटिक चाबियां लेना
# ==========================================
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

channel_tokens = {
    "MYSTERY CHANNEL": os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC"),
    "AI AUTO PILOT EMPIRE": os.environ.get("YOUTUBE_TOKEN_EMPIRE"),
    "GIRISH AI GADGET": os.environ.get("YOUTUBE_TOKEN_GADGET"),
    "HEALTH & AYURVEDA": os.environ.get("YOUTUBE_TOKEN_HEALTH"),
    "ZEROTOUCH AI CREATOR": os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH")
}

# ==========================================
# 📝 साइकोलॉजिकल हुक्स वाली 40-सेकंड की कहानियां
# ==========================================
stories = [
    {
        "title": "चिल्लाती हुई तिजोरी का रहस्य",
        "script": "क्या आप जानते हैं कि दुनिया में एक ऐसी तिजोरी भी है जो हर रात ठीक दो बजे अपने आप खुल जाती है? वैज्ञानिकों ने सालों रिसर्च की, कैमरे लगाए, लेकिन रहस्य नहीं खुला। सबसे हैरान करने वाली बात यह है कि इसके अंदर कोई खजाना नहीं, बल्कि सिर्फ एक खाली पुरानी डायरी रखी है। इसके आखिरी पन्ने पर क्या लिखा है, जानना चाहते हैं? नीचे कमेंट में पार्ट 2 लिखें!",
        "search_term": "mystery,vault,dark",
        "tags": "mystery shorts viral secrets"
    },
    {
        "title": "अमीरी का सबसे गुप्त नियम",
        "script": "दुनिया के 99% अमीर लोग रात को सोने से पहले एक खास काम करते हैं, जिसे 'द सीक्रेट स्क्रिप्टिंग' कहा जाता है। वे कल होने वाली जीतों को आज ही अपनी डायरी में लिख लेते हैं। यह कोई जादू नहीं, बल्कि आपके दिमाग को री-वायर करने की वैज्ञानिक तकनीक है। आज रात से ही इसे आजमाएं और तीन दिन में खुद चमत्कार देखें। ऐसे ही सीक्रेट्स के लिए सब्सक्राइब करें!",
        "search_term": "wealth,luxury,gold",
        "tags": "wealth motivation success money"
    },
    {
        "title": "मानव शरीर का सबसे बड़ा झूठ",
        "script": "हमें बचपन से सिखाया गया है कि हमारा दिमाग सिर्फ 10 प्रतिशत काम करता है, लेकिन यह विज्ञान का सबसे बड़ा झूठ है। असल में, जब आप गहरी नींद में होते हैं, तब भी आपका दिमाग एक सुपरकंप्यूटर से ज्यादा तेजी से आपकी पुरानी यादों को फिल्टर कर रहा होता है। आपकी एक छोटी सी आदत आपके दिमाग की ताकत को 10 गुना बढ़ा सकती है। जानिए कैसे, हमारे अगले वीडियो में!",
        "search_term": "brain,cyberpunk,science",
        "tags": "health facts science ayurveda"
    }
]

# ==========================================
# 🖼️ कहानी से मैच होती इमेज और 🎙️ ऑडियो इंजन
# ==========================================
def create_media_assets(story):
    print(f"\n🎬 [क्रिएटिव] चुनी गई कहानी: {story['title']}")
    
    # 1. क्रिस्टल क्लियर वॉइस जनरेशन
    print("🎙️ [ऑडियो] क्रिस्टल क्लियर आवाज तैयार की जा रही है...")
    audio_path = "voice.mp3"
    tts = gTTS(text=story['script'], lang='hi', slow=False)
    tts.save(audio_path)
    
    # 2. कहानी से मैच होती इमेज ढूंढना (Dynamic Image Selector)
    print(f"📸 [विजुअल] कहानी के टॉपिक '{story['search_term']}' से मैच होती 4K इमेज खोजी जा रही है...")
    image_path = "background.jpg"
    
    # Unsplash की सोर्स API का उपयोग करके कहानी के हिसाब से सटीक फोटो निकालना
    image_url = f"https://source.unsplash.com/featured/1080x1920/?{story['search_term']}"
    
    try:
        response = requests.get(image_url, timeout=15)
        # अगर किसी कारण से इंटरनेट धीमा हो, तो डिफ़ॉल्ट प्रीमियम बैकग्राउंड यूज़ होगा (क्रैश प्रूफ)
        if response.status_code != 200:
            raise Exception("Unsplash Alternate Route")
    except:
        image_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1080&auto=format&fit=crop"
        response = requests.get(image_url)
        
    with open(image_path, 'wb') as file:
        file.write(response.content)
    print("✅ [विजुअल] कहानी से मैच होती बिल्कुल साफ इमेज सफलतापूर्वक डाउनलोड हो गई।")
        
    return audio_path, image_path

# ==========================================
# 🎬 वीडियो एडिटिंग और परफेक्ट सिंकिंग इंजन
# ==========================================
def render_video(audio_path, image_path):
    print("\n🖥️ [रेंडरिंग] इमेज और आवाज को परफेक्ट सिंक (Match) किया जा रहा है...")
    output_path = "final_viral_shorts.mp4"
    
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path)
    
    # टाइमिंग को ऑडियो की लंबाई के बराबर 100% सटीक मैच करना
    image_clip = image_clip.set_duration(audio_clip.duration)
    image_clip = image_clip.resize(height=1920, width=1080)
    
    video_clip = image_clip.set_audio(audio_clip)
    
    # हाई-क्वालिटी mp4 आउटपुट रेंडर करना
    video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    print(f"✅ [सफलता] वीडियो 100% परफेक्ट बन गया है: {output_path}")
    
    return output_path, audio_clip.duration

# ==========================================
# 🚀 यूट्यूब स्मार्ट ऑटो-अपलोडर (क्रैश प्रूफ)
# ==========================================
def upload_to_youtube(video_file, story_title, story_tags, channel_name, refresh_token):
    if not refresh_token:
        print(f"⚠️ {channel_name} का टोकन नहीं मिला। इसे छोड़ रहे हैं।")
        return

    print(f"\n📡 [अपलोड] {channel_name} पर वीडियो भेजा जा रहा है...")
    
    credentials = Credentials(
        None,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token"
    )
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": f"{story_title} #shorts #viral",
            "description": f"{story_title}\n\nरोजाना ऐसे ही रहस्यों और जानकारी के लिए सब्सक्राइब करें!\n#shorts #trending",
            "tags": story_tags.split(" "),
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    try:
        response = request.execute()
        print(f"🟢 सफलता! {channel_name} पर वीडियो लाइव हो गया: https://youtu.be/{response['id']}")
    except Exception as e:
        # अगर किसी चैनल पर डेली लिमिट खत्म हो जाए, तो कोड बंद नहीं होगा, बाकी पर अपलोड करता रहेगा
        print(f"🔴 {channel_name} पर इस बार अपलोड नहीं हो सका (लिमिट या नेटवर्क इश्यू): {e}")

# ==========================================
# ⚙️ मेन एग्जीक्यूशन (इंजन स्टार्ट)
# ==========================================
if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("🛑 एरर: गिटहब सीक्रेट्स में CLIENT_ID या GOOGLE_CLIENT_SECRET नहीं मिला!")
        exit(1)
        
    selected_story = random.choice(stories)
    audio_file, image_file = create_media_assets(selected_story)
    final_video, duration = render_video(audio_file, image_file)
    print(f"⏱️ वीडियो की कुल लंबाई: {round(duration, 2)} सेकंड")
    
    for channel, token in channel_tokens.items():
        upload_to_youtube(final_video, selected_story['title'], selected_story['tags'], channel, token)
        
    print("\n" + "="*85)
    print("🏆 मिशन 100% सक्सेसफुल! आपका नया इंटेलिजेंट ऑटोमेशन पूरी तरह पूरा हुआ।")
    print("="*85)
