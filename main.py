import os, json, requests, time
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# अभी के २ चैनल
CHANNELS = [
    {"name": "Mystic Universe", "topic": "Space Mystery", "link": "https://www.amazon.in/s?k=telescope&tag=girishbhut07-21"},
    {"name": "Girish AI Gadgets", "topic": "Future Tech", "link": "https://www.amazon.in/s?k=smart+gadgets&tag=girishbhut07-21"}
]

def main_engine():
    tg_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    try:
        # १. वीडियो रेंडरिंग (HD Quality)
        for ch in CHANNELS:
            video_name = f"{ch['name']}.mp4"
            bg = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=8)
            txt = TextClip(f"{ch['topic']}\nCheck Link in Bio!", fontsize=70, color='white', size=(900, None), method='caption')
            final_vid = CompositeVideoClip([bg, txt.set_position('center').set_duration(8)])
            final_vid.write_videofile(video_name, fps=24, codec="libx264")

            # २. टेलीग्राम पर रिपोर्ट
            msg = f"🚀 **सफलता!** {ch['name']} का वीडियो तैयार है।\n🛒 अफ़िलिएट लिंक: {ch['link']}"
            requests.get(f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown")
            
    except Exception as e:
        requests.get(f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text=❌ एरर: {str(e)}")

if __name__ == "__main__":
    main_engine()
