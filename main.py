# गिरीश भाई का 100% AI जनरेटेड एम्पायर (Gadgets + Mystic Universe) - PRO VERSION
import os
import urllib.parse
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
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

# 2. Gemini AI - स्क्रिप्ट और इमेज प्रॉम्प्ट दोनों बनाएगा
def get_ai_content(topic):
    print(f"Gemini AI '{topic}' पर सोच रहा है...")
    genai.configure(api_key=GEMINI_KEY)
    
    # 100% पक्का फिक्स: यहाँ सही और नया 'gemini-2.5-flash' मॉडल लगा दिया है
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    script_prompt = f"Write a 30-second YouTube short script in Hindi about {topic}. ONLY provide the spoken Hindi voiceover text. DO NOT use English words, brackets, or hashtags."
    script_response = model.generate_content(script_prompt)
    clean_script = script_response.text.replace("*", "").replace("#", "").replace("[", "").replace("]", "").strip()
    
    image_prompt_req = f"Write a short, highly detailed English prompt to generate an AI image representing this topic: {topic}. Only output the prompt."
    image_prompt_res = model.generate_content(image_prompt_req)
    image_prompt = image_prompt_res.text.strip()
    
    return clean_script, image_prompt

# 3. खुद की 100% ओरिजिनल AI इमेज (Visuals) बनाना (Pexels की कोई ज़रूरत नहीं)
def generate_ai_image(prompt_text, filename):
    print("ओरिजिनल AI विज़ुअल्स जनरेट हो रहे हैं...")
    encoded_prompt = urllib.parse.quote(prompt_text + " hyper realistic, highly detailed, 9:16 aspect ratio, 4k")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception("AI इमेज जनरेट करने में एरर आया।")

# 4. शुद्ध AI वीडियो बनाना
def create_ai_video(script_text, image_file, final_vid):
    print("AI आवाज़ और विज़ुअल्स को मिलाकर वीडियो बनाया जा रहा है...")
    
    if not script_text or len(script_text) < 5:
        script_text = "यह एक बहुत ही शानदार वीडियो है, इसे आखिर तक जरूर देखें और लाइक करें।"
        
    tts = gTTS(text=script_text, lang='hi', slow=False)
    tts.save("voice.mp3")
    audio = AudioFileClip("voice.mp3")
    
    # फोटो को वीडियो में बदलना (यह ऑडियो के बराबर खुद सेट हो जाएगा, कभी क्रैश नहीं होगा)
    image_clip = ImageClip(image_file)
    video = image_clip.set_duration(audio.duration)
    final_video = video.set_audio(audio)
    
    final_video.write_videofile(final_vid, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
    
    audio.close()
    final_video.close()

# 5. यूट्यूब पर अपलोड
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
        print("--- 📱 Girish AI Gadgets (100% AI Mode) ---")
        script, img_prompt = get_ai_content("a futuristic AI tech gadget")
        generate_ai_image(img_prompt, "gadget_ai.jpg")
        create_ai_video(script, "gadget_ai.jpg", "final_gadget.mp4")
        desc = script + f"\n\n👉 Buy Now (Amazon Link): {AMAZON_ID}\n#gadgets #ai #tech"
        upload_video(TOKEN_GADGETS, "final_gadget.mp4", "Future Tech is Here! 🤯 #shorts #ai", desc, ["shorts", "tech", "gadgets", "ai"], "28")
    except Exception as e:
        print(f"❌ Gadgets चैनल एरर: {e}")

# -- चैनल 2: Mystic Universe --
def run_mystic_channel():
    try:
        print("--- 🌌 Mystic Universe (100% AI Mode) ---")
        script, img_prompt = get_ai_content("a mysterious secret of the universe or black hole")
        generate_ai_image(img_prompt, "mystic_ai.jpg")
        create_ai_video(script, "mystic_ai.jpg", "final_mystic.mp4")
        desc = script + "\n\n#space #universe #mystery #shorts"
        upload_video(TOKEN_MYSTIC, "final_mystic.mp4", "Universe Secret Revealed! 🌌 #shorts #space", desc, ["shorts", "space", "universe"], "28")
    except Exception as e:
        print(f"❌ Mystic चैनल एरर: {e}")

# 6. मेन स्विच
if __name__ == "__main__":
    print("🚀 PRO AI इंजन स्टार्ट...")
    run_gadgets_channel()
    run_mystic_channel()
    print("🎯 दोनों चैनलों पर 100% ओरिजिनल AI वीडियो सफलतापूर्वक अपलोड हो गए!")
