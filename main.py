import os, json, random, requests, asyncio, edge_tts, time, urllib.parse, re
from PIL import Image
if not hasattr(Image, 'Resampling'): Image.Resampling = getattr(Image, 'LANCZOS', 1)
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🛡️ बैच 2: 100% Perfect Video Engine (Gadgets & AI Sales)")

GROQ_KEY = os.environ.get("GROQ_API_KEY")
CLIENT_ID = "768932543756-7e17ufdmt7r67urc9krua7t69vps6h57.apps.googleusercontent.com"
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

CHANNELS_CONFIG = {
    "GADGET_PRO": {"token": os.environ.get("TOKEN_GADGET"), "category": "28", "tags": ["gadgets"], "style": "high tech product photography, neon lights, 8k", "hooks": ["स्मार्ट गैजेट्स"]},
    "AI_AUTOMATION_HUB": {"token": os.environ.get("TOKEN_AI1"), "category": "27", "tags": ["ai"], "style": "futuristic cyberpunk, money raining, 8k", "hooks": ["AI से पैसे कमाएं"]},
    "CREATOR_AI_SETUP": {"token": os.environ.get("TOKEN_AI2"), "category": "27", "tags": ["youtube ai"], "style": "professional studio setup, neon, 8k", "hooks": ["यूट्यूब ऑटोमेशन"]},
    "FUTURE_TECH_AI": {"token": os.environ.get("TOKEN_AI3"), "category": "27", "tags": ["tech"], "style": "sci-fi, artificial intelligence brain, 8k", "hooks": ["भविष्य का AI"]},
    "EXTRA_CHANNEL": {"token": os.environ.get("TOKEN_EXTRA"), "category": "27", "tags": ["viral"], "style": "cinematic, 8k", "hooks": ["अद्भुत रहस्य"]}
}

def get_script(hook):
    url, headers = "https://api.groq.com/openai/v1/chat/completions", {"Authorization": f"Bearer {GROQ_KEY}"}
    prompt = f"Write a 5-scene Hindi YouTube Shorts script about: '{hook}'. Format JSON: {{\"title\": \"...\", \"scenes\": [{{\"text\": \"...\", \"prompt\": \"English image prompt\"}}]}}"
    res = requests.post(url, headers=headers, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}).json()
    return json.loads(re.search(r'\{[\s\S]*\}', res['choices'][0]['message']['content']).group(0))

def get_images(scenes, style):
    imgs = []
    for i, s in enumerate(scenes):
        for attempt in range(5): # Strict Quality Check Loop
            try:
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(s['prompt'] + ', ' + style)}?width=1080&height=1920&nologo=true"
                r = requests.get(url, timeout=60)
                if r.status_code == 200 and len(r.content) > 50000:
                    with open(f"img_{i}.jpg", "wb") as f: f.write(r.content)
                    imgs.append(f"img_{i}.jpg"); break
            except: time.sleep(5)
    if len(imgs) != len(scenes): raise Exception("Image Quality Check Failed")
    return imgs

def create_voice(text):
    asyncio.run(edge_tts.Communicate(text, "hi-IN-MadhurNeural").save("v.mp3"))

def assemble_and_upload(imgs, scenes, token, title):
    create_voice(" ".join([s['text'] for s in scenes]))
    audio = AudioFileClip("v.mp3")
    dur = audio.duration / len(imgs)
    clips = []
    for img_path in imgs:
        base = ImageClip(img_path).set_duration(dur).resize((1080, 1920))
        zoom = base.resize(lambda t: 1 + 0.05 * (t/dur))
        clips.append(zoom)
    final = concatenate_videoclips(clips, method="compose").set_audio(audio)
    final.write_videofile("out.mp4", fps=24, preset="ultrafast", logger=None)
    
    creds = Credentials(token=None, refresh_token=token, token_uri="https://oauth2.googleapis.com/token", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    build("youtube", "v3", credentials=creds).videos().insert(
        part="snippet,status", body={"snippet": {"title": f"{title} #shorts", "description": "Subscribe for more details!"}, "status": {"privacyStatus": "public"}},
        media_body=MediaFileUpload("out.mp4", resumable=True)
    ).execute()

def run():
    for ch, cfg in CHANNELS_CONFIG.items():
        try:
            data = get_script(random.choice(cfg['hooks']))
            imgs = get_images(data['scenes'], cfg['style'])
            assemble_and_upload(imgs, data['scenes'], cfg['token'], data['title'])
        except Exception as e: print(f"Error in {ch}: {e}")

if __name__ == "__main__": run()
