import os
import sys
import subprocess

# =====================================================================================
# 🛠️ स्टेप 0: गिटहब सर्वर में बैकएंड टूल्स ऑटो-इंस्टॉलर (The Ultimate NumPy Array Fix)
# =====================================================================================
print("⏳ [सिस्टम अपडेट] गिटहब में सभी सुपर-एडवांस टूल्स इंस्टॉल किए जा रहे हैं...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "gTTS", "requests", "moviepy==1.0.3", "Pillow==9.5.0", "opencv-python", "numpy"])
print("✅ [सिस्टम अपडेट] सभी एडवांस टूल्स सफलतापूर्वक इंस्टॉल हो गए! इंजन लाइव है...\n")

import random
import requests
import cv2
import numpy as np  # 👈 इमेज एरर को जड़ से खत्म करने वाला मास्टर टूल
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("="*85)
print("🎯 🧬 THE ULTIMATE DYNAMIC NUMPY IMAGE EMPIRE ENGINE (V14.2) 🧬 🎯")
print("="*85)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# आपकी गिटहब तिजोरी के हिसाब से 5 एक्टिव चैनल्स
channel_tokens = {
    "MYSTERY CHANNEL": os.environ.get("YOUTUBE_REFRESH_TOKEN_MYSTIC"),
    "AI AUTO PILOT EMPIRE": os.environ.get("YOUTUBE_TOKEN_EMPIRE"),
    "GIRISH AI GADGET": os.environ.get("YOUTUBE_TOKEN_GADGET"),
    "ZEROTOUCH AI CREATOR": os.environ.get("YOUTUBE_TOKEN_ZEROTOUCH"),
    "FACELESS AI WEALTH": os.environ.get("YOUTUBE_TOKEN_WEALTH")
}

# 📝 कहानियां और उनके लिए बिल्कुल सटीक सर्च टर्म्स
stories = [
    {
        "title": "चिल्लाती हुई तिजोरी का रहस्य",
        "script": "क्या आप जानते हैं कि दुनिया में एक ऐसी तिजोरी भी है जो हर रात ठीक दो बजे अपने आप खुल जाती है? वैज्ञानिकों ने सालों रिसर्च की, कैमरे लगाए, लेकिन रहस्य नहीं खुला। सबसे हैरान करने वाली बात यह है कि इसके अंदर कोई खजाना नहीं, बल्कि सिर्फ एक खाली पुरानी डायरी रखी है। इसके आखिरी पन्ने पर क्या लिखा है, जानना चाहते हैं? नीचे कमेंट में पार्ट 2 लिखें!",
        "search_term": "mystery vault",
        "tags": "mystery shorts viral secrets"
    },
    {
        "title": "अमीरी का सबसे गुप्त नियम",
        "script": "दुनिया के 99% अमीर लोग रात को सोने से पहले एक खास काम करते हैं, जिसे 'द सीक्रेट स्क्रिप्टिंग' कहा जाता है। वे कल होने वाली जीतों को आज ही अपनी डायरी में लिख लेते हैं। यह कोई जादू नहीं, बल्कि आपके दिमाग को री-वायर करने की वैज्ञानिक तकनीक है। आज रात से ही इसे आजमाएं और तीन दिन में खुद चमत्कार देखें। ऐसे ही सीक्रेट्स के लिए सब्सक्राइब करें!",
        "search_term": "wealth luxury",
        "tags": "wealth motivation success money"
    },
    {
        "title": "मानव शरीर का सबसे बड़ा झूठ",
        "script": "हमें बचपन से सिखाया गया है कि हमारा दिमाग सिर्फ 10 प्रतिशत काम करता है, लेकिन यह विज्ञान का सबसे बड़ा झूठ है। असल में, जब आप गहरी नींद में होते हैं, तब भी आपका दिमाग एक सुपरकंप्यूटर से ज्यादा तेजी से आपकी पुरानी यादों को फिल्टर कर रहा होता है। आपकी एक छोटी सी आदत आपके दिमाग की ताकत को 10 गुना बढ़ा सकती है। जानिए कैसे, हमारे अगले वीडियो में!",
        "search_term": "human brain science",
        "tags": "health facts science ayurveda"
    }
]

# 🖼️ पिक्सल्स API से हर बार कहानी के हिसाब से अलग इमेज लाने का लॉजिक
def fetch_dynamic_image(keyword):
    print(f"📸 [इमेज सर्च] टॉपिक '{keyword}' के लिए लाइव फोटो खोजी जा रही है...")
    temp_path = "background.jpg"
    final_path = "clean_background.jpg"
    
    if PEXELS_API_KEY:
        # रैंडम पेज सर्च ताकि कभी भी फोटो रिपीट न हो
        random_page = random.randint(1, 5)
        url = f"https://api.pexels.com/v1/search?query={keyword}&orientation=portrait&per_page=1&page={random_page}"
        headers = {"Authorization": PEXELS_API_KEY}
        try:
            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()
            if data.get("photos"):
                img_url = data["photos"][0]["src"]["large2x"]
                img_res = requests.get(img_url, timeout=10)
                with open(temp_path, 'wb') as f:
                    f.write(img_res.content)
                
                # OpenCV से री-साइज करना ताकि साइज परफेक्ट रहे
                img = cv2.imread(temp_path)
                if img is not None:
                    img_resized = cv2.resize(img, (1080, 1920))
                    cv2.imwrite(final_path, img_resized)
                    print("✅ [सफलता] पिक्सल्स से कहानी से मैच होती बिल्कुल फ्रेश इमेज मिल गई!")
                    return final_path
        except Exception as e:
            print(f"⚠️ पिक्सल्स सर्च में दिक्कत आई: {e}। बैकअप रूट चालू कर रहे हैं...")

    # फुलप्रूफ बैकअप रूट
    backup_url = f"https://images.unsplash.com/featured/1080x1920/?{keyword}&sig={random.randint(1, 10000)}"
    img_res = requests.get(backup_url)
    with open(temp_path, 'wb') as f:
        f.write(img_res.content)
    img = cv2.imread(temp_path)
    img_resized = cv2.resize(img, (1080, 1920))
    cv2.imwrite(final_path, img_resized)
    return final_path

def create_media_assets(story):
    print(f"\n🎬 [क्रिएटिव] चुनी गई कहानी: {story['title']}")
    print("🎙️ [ऑडियो] क्रिस्टल क्लियर आवाज तैयार की जा रही है...")
    audio_path = "voice.mp3"
    tts = gTTS(text=story['script'], lang='hi', slow=False)
    tts.save(audio_path)
    
    image_path = fetch_dynamic_image(story['search_term'])
    return audio_path, image_path

def render_video(audio_path, image_path):
    print("\n🖥️ [रेंडरिंग] इमेज ऐरे और आवाज को परफेक्ट सिंक किया जा रहा है...")
    output_path = "final_viral_shorts.mp4"
    
    # 🔥 पिलो एरर को कुचलने का असली कोड: OpenCV से NumPy ऐरे में बदलना
    raw_img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
    
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(rgb_img).set_duration(audio_clip.duration)
    
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    print(f"✅ [सफलता] वीडियो 100% परफेक्ट बन गया है: {output_path}")
    return output_path, audio_clip.duration

def upload_to_youtube(video_file, story_title, story_tags, channel_name, refresh_token):
    if not refresh_token:
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
            "description": f"{story_title}\n\n#shorts #trending",
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
        print(f"🔴 {channel_name} पर अपलोड फेल: {e}")

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("🛑 एरर: क्रेडेंशियल्स गायब हैं!")
        exit(1)
        
    selected_story = random.choice(stories)
    audio_file, image_file = create_media_assets(selected_story)
    final_video, duration = render_video(audio_file, image_file)
    
    for channel, token in channel_tokens.items():
        upload_to_youtube(final_video, selected_story['title'], selected_story['tags'], channel, token)
        
    print("\n" + "="*85)
    print("🏆 मिशन सक्सेसफुल! 5-चैनल डायनामिक इमेज एम्पायर पूरी तरह लाइव है।")
    print("="*85)
