import time
import datetime
import requests
import uiautomator2 as u2

# --- CONFIG ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"
PENALTY_APP = "com.duolingo"

# 🕒 TIME SETTINGS (24-Hour Format)
HAPPY_HOUR_START = 16  # 4 PM
HAPPY_HOUR_END = 17    # 5 PM

# 📊 STATS
VIOLATION_COUNT = 0

BLACKLIST = [
    "skibidi", "prank", "brainrot", "challenge", 
    "sex", "hot", "kiss", "dance", "girl"
]
BANNED_SITES = ["instagram.com", "youtube.com", "tiktok.com"]

def is_happy_hour():
    """Returns True if current time is between 4 PM and 5 PM"""
    current_hour = datetime.datetime.now().hour
    # Check if we are in the allowed window (e.g., 16:00 to 16:59)
    if HAPPY_HOUR_START <= current_hour < HAPPY_HOUR_END:
        return True
    return False

def log_step(step, content):
    print(f"🔄 Step {step}/15")
    print(f"[yellow]CodeAct response:[/yellow]")
    print(f"Thought: {content}")
    time.sleep(0.5)

def ask_ai(title):
    if len(title) < 5: return "YES"
    prompt = f"Is the video title '{title}' educational? Answer YES or NO."
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME, "prompt": prompt, "stream": False
        })
        return response.json()["response"].strip().upper()
    except:
        return "YES"

def punish(d, reason):
    global VIOLATION_COUNT
    VIOLATION_COUNT += 1
    
    print(f"\n🚨 PUNISHMENT #{VIOLATION_COUNT}: {reason}")
    print(f"📉 Social Credit Score: {-10 * VIOLATION_COUNT}")
    
    d.press("home")
    time.sleep(0.3)
    try:
        d.app_start(PENALTY_APP)
        print("🦉 Duolingo Launched!")
    except:
        pass

def main():
    print("🚀 Initializing DroidRun (TIME TRACKER MODE)...")
    try:
        d = u2.connect()
        print(f"✅ Connected to: {d.serial}")
    except:
        print("❌ Connection failed.")
        return

    print(f"🕒 Happy Hour set for: {HAPPY_HOUR_START}:00 - {HAPPY_HOUR_END}:00")
    print("🛡️  SENTINEL ACTIVE.")
    step_count = 1

    while True:
        try:
            # 1. CHECK TIME FIRST
            if is_happy_hour():
                # If it's happy hour, we skip ALL checks
                print(f"🟢 Happy Hour Active ({datetime.datetime.now().strftime('%H:%M')}). Enjoy your brainrot.")
                time.sleep(5) # Sleep longer to save battery
                continue

            current_app = d.app_current()['package']
            
            # --- YOUTUBE ---
            if current_app == "com.google.android.youtube":
                # Shorts
                if d(resourceId="com.google.android.youtube:id/reel_recycler").exists or \
                   d(resourceId="com.google.android.youtube:id/reel_player_page_fragment").exists:
                    log_step(step_count, "Detected Shorts outside Happy Hour.")
                    punish(d, "Shorts (Not 4pm yet!)")
                    step_count += 1
                    continue

                # Titles
                title_ui = d(resourceId="com.google.android.youtube:id/title")
                if title_ui.exists:
                    title = title_ui.get_text()
                    
                    if any(bad in title.lower() for bad in BLACKLIST):
                        punish(d, f"Keyword Blocked: {title}")
                        step_count += 1
                        continue
                        
                    if len(title) > 5:
                        print(f"👀 Watching: {title[:40]}...") 
                        verdict = ask_ai(title)
                        if "NO" in verdict:
                            punish(d, f"AI Blocked: {title}")
                            step_count += 1

            # --- INSTAGRAM ---
            elif current_app == "com.instagram.android":
                if d(resourceId="com.instagram.android:id/clips_video_container").exists or \
                   d(resourceId="com.instagram.android:id/reel_viewer_root").exists:
                    punish(d, "Instagram Reels")
                    step_count += 1

            # --- CHROME ---
            elif current_app == "com.android.chrome":
                url_ui = d(resourceId="com.android.chrome:id/url_bar")
                if url_ui.exists:
                    url_text = url_ui.get_text().lower()
                    if any(site in url_text for site in BANNED_SITES):
                        punish(d, "Banned Website")
                        step_count += 1
            
            time.sleep(0.5)

        except Exception:
            pass

if __name__ == "__main__":
    main()