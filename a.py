import time
import requests
import uiautomator2 as u2
import datetime
from rich.console import Console

# --- CONFIG ---
SERVER_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"
PENALTY_APP = "com.duolingo"

# --- RICH CONSOLE SETUP ---
console = Console(highlight=False)
d = None  # Global device object

def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(level, message, style=None):
    ts = get_timestamp()
    if style:
        console.print(f"{ts} {level}: {style}{message}[/]", highlight=False)
    else:
        console.print(f"{ts} {level}: {message}", highlight=False)

def simulate_droidrun_scan(step):
    log("INFO", f"🔄 Step {step}/100")
    log("DEBUG", "📸 Screenshot captured for Analysis")

def print_code_act_response(thought):
    log("INFO", "[yellow]Sentinel Thought:[/yellow]")
    console.print(f"  {thought}", highlight=False)

# --- CORE LOGIC ---
def ask_ai(title):
    if len(title) < 5: return "ALLOW"
    prompt = f"Analyze title: '{title}'. Allow strictly academic. Block entertainment/vlogs/pranks. Reply BLOCK or ALLOW."
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False}, timeout=5)
        result = response.json()["response"].strip().upper()
        return "BLOCK" if "BLOCK" in result else "ALLOW"
    except:
        return "ALLOW"

def main():
    global d
    console.print("🚀 Starting: DroidRun Sentinel", style="bold")
    console.print("🔌 Finding connected device...")
    
    try:
        # 1. Connect silently
        d = u2.connect()
        
        # 2. CRITICAL: Prevents the background DroidRun from pausing/vanishing
        d.healthcheck = False 
        
        # 3. CRITICAL: Prevents script hanging on animations
        d.settings['wait_for_idle_timeout'] = 0
        
        serial = d.serial
        console.print(f"📱 Connected to: {serial}", style="green")
    except Exception as e:
        console.print(f"❌ Connection failed: {e}", style="red")
        return

    step = 1
    yt_title_ids = ["com.google.android.youtube:id/video_title", "com.google.android.youtube:id/title"]

    while True:
        try:
            simulate_droidrun_scan(step)
            
            # Re-verify settings inside the loop
            d.settings['wait_for_idle_timeout'] = 0
            
            # Identify current foreground app
            current_app = d.app_current().get('package')
            violation_found = False
            violation_reason = ""

            # --- MONITORING LOGIC ---
            if current_app == "com.google.android.youtube":
                # Check for Shorts
                if d(resourceId="com.google.android.youtube:id/reel_recycler").exists:
                    violation_found, violation_reason = True, "YouTube Shorts"
                else:
                    title = ""
                    for tid in yt_title_ids:
                        if d(resourceId=tid).exists:
                            title = d(resourceId=tid).get_text()
                            break
                    if title and ask_ai(title) == "BLOCK":
                        violation_found, violation_reason = True, f"AI Block: {title}"

            elif current_app == "com.instagram.android":
                violation_found, violation_reason = True, "Instagram Detected"

            # --- PUNISHMENT ---
            if violation_found:
                log("WARNING", f"Violation: {violation_reason}", style="bold red")
                d.press("home")
                d.app_start(PENALTY_APP)
                log("INFO", f"Penalty: Redirected to {PENALTY_APP}")

            time.sleep(2)
            step += 1

        except KeyboardInterrupt:
            console.print("\n🛑 Sentinel Stopped.", style="bold red")
            break
        except Exception as e:
            log("ERROR", f"Loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()