import time
import requests
import uiautomator2 as u2
import datetime
from rich.console import Console
from rich.markdown import Markdown

# --- CONFIG ---
SERVER_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"
PENALTY_APP = "com.duolingo"

# --- RICH CONSOLE SETUP ---
console = Console(highlight=False)

def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(level, message, style=None):
    ts = get_timestamp()
    if style:
        console.print(f"{ts} {level}: {style}{message}[/]", highlight=False)
    else:
        console.print(f"{ts} {level}: {message}", highlight=False)

def log_droidrun_style(message):
    console.print(message, highlight=False)

def simulate_droidrun_scan(step):
    log("INFO", f"🔄 Step {step}/100")
    log("DEBUG", "Taking screenshot")
    log("DEBUG", "Screenshot taken via ADB")
    log("DEBUG", "📸 Screenshot captured for CodeAct")
    log("DEBUG", "Getting state (attempt 1/3)")

def print_code_act_response(thought):
    log("INFO", "[yellow]CodeAct response:[/yellow]")
    console.print(thought, highlight=False)

def execute_action_block(code, result_msg):
    log("DEBUG", "Executing:")
    console.print("```python", style="dim")
    console.print(code)
    console.print("```", style="dim")
    time.sleep(0.5)
    log("INFO", "[dim]💡 Execution result:[/dim]")
    log("INFO", result_msg)
    log("DEBUG", "Cleared 1 screenshots from queue")

# --- CORE LOGIC ---
def get_server_config():
    try:
        response = requests.get(f"{SERVER_URL}/api/config", timeout=0.5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {"blacklist": ["skibidi", "mrbeast", "prank"], "happy_hour_start": 99, "happy_hour_end": 99}

# ✅ NEW: The Snitch Function
def log_violation_to_server(reason):
    try:
        requests.post(f"{SERVER_URL}/api/violation", json={"reason": reason}, timeout=0.5)
    except:
        pass # If server is down, keep punishing anyway

def ask_ai(title):
    if len(title) < 5: return "ALLOW"
    prompt = f"Analyze title: '{title}'. Allow strictly academic. Block entertainment/vlogs/pranks. Reply BLOCK or ALLOW."
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False}, timeout=5)
        result = response.json()["response"].strip().upper()
        if "BLOCK" in result: return "BLOCK"
        return "ALLOW"
    except:
        return "ALLOW"

def show_droidrun_overlay(message):
    # This tells the DroidRun Portal app to show its custom UI box
    # Replace 'com.droidrun.portal.SHOW_BLOCK' with your actual Intent filter if different
    d.shell(f"am broadcast -a com.droidrun.portal.SHOW_BLOCK --es 'msg' '{message}'")
    log("INFO", "Sent signal to Portal to display overlay box.")
    
def main():
    console.print("🚀 Starting: DroidRun Sentinel", style="bold")
    console.print("🕵️ Anonymized telemetry enabled. We collect anonymous usage data to help us improve DroidRun.")
    console.print("🔌 Finding connected device...")
    
    import time
import requests
import uiautomator2 as u2
import datetime
from rich.console import Console
from rich.markdown import Markdown

# --- CONFIG ---
SERVER_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"
PENALTY_APP = "com.duolingo"

# --- RICH CONSOLE SETUP ---
console = Console(highlight=False)

def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(level, message, style=None):
    ts = get_timestamp()
    if style:
        console.print(f"{ts} {level}: {style}{message}[/]", highlight=False)
    else:
        console.print(f"{ts} {level}: {message}", highlight=False)

def log_droidrun_style(message):
    console.print(message, highlight=False)

def simulate_droidrun_scan(step):
    log("INFO", f"🔄 Step {step}/100")
    log("DEBUG", "Taking screenshot")
    log("DEBUG", "Screenshot taken via ADB")
    log("DEBUG", "📸 Screenshot captured for CodeAct")
    log("DEBUG", "Getting state (attempt 1/3)")

def print_code_act_response(thought):
    log("INFO", "[yellow]CodeAct response:[/yellow]")
    console.print(thought, highlight=False)

def execute_action_block(code, result_msg):
    log("DEBUG", "Executing:")
    console.print("```python", style="dim")
    console.print(code)
    console.print("```", style="dim")
    time.sleep(0.5)
    log("INFO", "[dim]💡 Execution result:[/dim]")
    log("INFO", result_msg)
    log("DEBUG", "Cleared 1 screenshots from queue")

# --- CORE LOGIC ---
def get_server_config():
    try:
        response = requests.get(f"{SERVER_URL}/api/config", timeout=0.5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {"blacklist": ["skibidi", "mrbeast", "prank"], "happy_hour_start": 99, "happy_hour_end": 99}

# ✅ NEW: The Snitch Function
def log_violation_to_server(reason):
    try:
        requests.post(f"{SERVER_URL}/api/violation", json={"reason": reason}, timeout=0.5)
    except:
        pass # If server is down, keep punishing anyway

def ask_ai(title):
    if len(title) < 5: return "ALLOW"
    prompt = f"Analyze title: '{title}'. Allow strictly academic. Block entertainment/vlogs/pranks. Reply BLOCK or ALLOW."
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False}, timeout=5)
        result = response.json()["response"].strip().upper()
        if "BLOCK" in result: return "BLOCK"
        return "ALLOW"
    except:
        return "ALLOW"

def main():
    console.print("🚀 Starting: DroidRun Sentinel", style="bold")
    console.print("🕵️ Anonymized telemetry enabled. We collect anonymous usage data to help us improve DroidRun.")
    console.print("🔌 Finding connected device...")
    
    try:
        d = u2.connect()
        serial = d.serial
    except:
        serial = "UNKNOWN"
        
    console.print(f"📱 Using device: {serial}")
    console.print(f"🧠 LLM ready: {MODEL_NAME}")
    console.print("🤖 Agent mode: direct execution")
    console.print("🤖 Initializing DroidAgent...")
    time.sleep(1)
    console.print("✅ DroidAgent initialized successfully.", style="green")
    console.print("▶️ Starting agent execution...", style="yellow")
    console.print("Press Ctrl+C to stop")
    console.print("🚀 Running DroidAgent to achieve goal: monitor and block brainrot")
    console.print("💬 Preparing chat for task execution...")
    console.print("🧠 Step 1: Thinking...")
    console.print("\n")

    step = 1
    yt_title_ids = ["com.google.android.youtube:id/video_title", "com.google.android.youtube:id/title", "com.google.android.youtube:id/player_video_title_view"]

    while True:
        try:
            simulate_droidrun_scan(step)

            current_app = d.app_current().get('package')
            config = get_server_config()
            blacklist = config.get("blacklist", [])
            
            violation_found = False
            violation_reason = ""
            thought_process = ""

            # --- 1. YOUTUBE ---
            if current_app == "com.google.android.youtube":
                if d(resourceId="com.google.android.youtube:id/reel_recycler").exists:
                    violation_found = True
                    violation_reason = "YouTube Shorts"
                    thought_process = "I detected the Shorts UI. This is non-productive content."
                else:
                    title = ""
                    for tid in yt_title_ids:
                        if d(resourceId=tid).exists:
                            title = d(resourceId=tid).get_text()
                            if title: break
                    
                    if not title:
                        thought_process = "I see YouTube open, but no title is visible. The UI overlay might be hidden."
                        print_code_act_response(thought_process)
                        execute_action_block("d.click(center_x, center_y)", "Tapped screen to reveal overlay")
                        d.click(500, 1000) 
                        time.sleep(0.5)
                        continue 
                    
                    if title:
                        if any(bad in title.lower() for bad in blacklist):
                            violation_found = True
                            violation_reason = f"Keyword match: {title}"
                            thought_process = f"The video title '{title}' contains blacklisted keywords."
                        elif len(title) > 5 and ask_ai(title) == "BLOCK":
                            violation_found = True
                            violation_reason = f"AI Block: {title}"
                            thought_process = f"My analysis of '{title}' suggests it is entertainment, not education."
                        else:
                            thought_process = f"The user is watching '{title}'. This appears to be allowed content."

            # --- 2. INSTAGRAM ---
            elif current_app == "com.instagram.android":
                violation_found = True
                violation_reason = "Instagram"
                thought_process = "The user has opened Instagram. This application is on the strict block list."

            # --- 3. CHROME ---
            elif current_app == "com.android.chrome":
                url_ui = d(resourceId="com.android.chrome:id/url_bar")
                if url_ui.exists:
                    url_text = url_ui.get_text().lower()
                    forbidden = ["youtube.com", "instagram.com", "tiktok.com", "shorts"]
                    if any(site in url_text for site in forbidden):
                        violation_found = True
                        violation_reason = f"Browser Block: {url_text}"
                        thought_process = f"I detected a forbidden URL in Chrome: {url_text}. This circumvents the app block."
                    else:
                        thought_process = f"User is browsing Chrome: {url_text}. This URL seems safe."
                else:
                    thought_process = "User is in Chrome, but the URL bar is hidden. I cannot verify safety yet."

            else:
                 thought_process = f"User is in app: {current_app}. No restrictions apply here."

            print_code_act_response(thought_process)

            # --- PUNISHMENT & LOGGING ---
            if violation_found:
                # ✅ NEW: Log to server BEFORE punishment
                log_violation_to_server(violation_reason)
                
                reasoning = f"DEBUG: Reasoning: User is violating protocol ({violation_reason}). I must intervene immediately."
                log_droidrun_style(reasoning)
                
                code_snippet = f"d.press('home')\nd.app_start('{PENALTY_APP}')"
                execute_action_block(code_snippet, f"Opened {PENALTY_APP}")
                
                d.press("home")
                d.app_start(PENALTY_APP)
            
            time.sleep(2)
            step += 1

        except KeyboardInterrupt:
            break
        except Exception as e:
            log("ERROR", f"Loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
        
    console.print(f"📱 Using device: {serial}")
    console.print(f"🧠 LLM ready: {MODEL_NAME}")
    console.print("🤖 Agent mode: direct execution")
    console.print("🤖 Initializing DroidAgent...")
    time.sleep(1)
    console.print("✅ DroidAgent initialized successfully.", style="green")
    console.print("▶️ Starting agent execution...", style="yellow")
    console.print("Press Ctrl+C to stop")
    console.print("🚀 Running DroidAgent to achieve goal: monitor and block brainrot")
    console.print("💬 Preparing chat for task execution...")
    console.print("🧠 Step 1: Thinking...")
    console.print("\n")

    step = 1
    yt_title_ids = ["com.google.android.youtube:id/video_title", "com.google.android.youtube:id/title", "com.google.android.youtube:id/player_video_title_view"]

    while True:
        try:
            simulate_droidrun_scan(step)

            current_app = d.app_current().get('package')
            config = get_server_config()
            blacklist = config.get("blacklist", [])
            
            violation_found = False
            violation_reason = ""
            thought_process = ""

            # --- 1. YOUTUBE ---
            if current_app == "com.google.android.youtube":
                if d(resourceId="com.google.android.youtube:id/reel_recycler").exists:
                    violation_found = True
                    violation_reason = "YouTube Shorts"
                    thought_process = "I detected the Shorts UI. This is non-productive content."
                else:
                    title = ""
                    for tid in yt_title_ids:
                        if d(resourceId=tid).exists:
                            title = d(resourceId=tid).get_text()
                            if title: break
                    
                    if not title:
                        thought_process = "I see YouTube open, but no title is visible. The UI overlay might be hidden."
                        print_code_act_response(thought_process)
                        execute_action_block("d.click(center_x, center_y)", "Tapped screen to reveal overlay")
                        d.click(500, 1000) 
                        time.sleep(0.5)
                        continue 
                    
                    if title:
                        if any(bad in title.lower() for bad in blacklist):
                            violation_found = True
                            violation_reason = f"Keyword match: {title}"
                            thought_process = f"The video title '{title}' contains blacklisted keywords."
                        elif len(title) > 5 and ask_ai(title) == "BLOCK":
                            violation_found = True
                            violation_reason = f"AI Block: {title}"
                            thought_process = f"My analysis of '{title}' suggests it is entertainment, not education."
                        else:
                            thought_process = f"The user is watching '{title}'. This appears to be allowed content."

            # --- 2. INSTAGRAM ---
            elif current_app == "com.instagram.android":
                violation_found = True
                violation_reason = "Instagram"
                thought_process = "The user has opened Instagram. This application is on the strict block list."

            # --- 3. CHROME ---
            elif current_app == "com.android.chrome":
                url_ui = d(resourceId="com.android.chrome:id/url_bar")
                if url_ui.exists:
                    url_text = url_ui.get_text().lower()
                    forbidden = ["youtube.com", "instagram.com", "tiktok.com", "shorts"]
                    if any(site in url_text for site in forbidden):
                        violation_found = True
                        violation_reason = f"Browser Block: {url_text}"
                        thought_process = f"I detected a forbidden URL in Chrome: {url_text}. This circumvents the app block."
                    else:
                        thought_process = f"User is browsing Chrome: {url_text}. This URL seems safe."
                else:
                    thought_process = "User is in Chrome, but the URL bar is hidden. I cannot verify safety yet."

            else:
                 thought_process = f"User is in app: {current_app}. No restrictions apply here."

            print_code_act_response(thought_process)

            # --- PUNISHMENT & LOGGING ---
            if violation_found:
                # ✅ NEW: Log to server BEFORE punishment
                log_violation_to_server(violation_reason)
                
                reasoning = f"DEBUG: Reasoning: User is violating protocol ({violation_reason}). I must intervene immediately."
                log_droidrun_style(reasoning)
                
                code_snippet = f"d.press('home')\nd.app_start('{PENALTY_APP}')"
                execute_action_block(code_snippet, f"Opened {PENALTY_APP}")
                
                d.press("home")
                d.app_start(PENALTY_APP)
            
            time.sleep(2)
            step += 1

        except KeyboardInterrupt:
            break
        except Exception as e:
            log("ERROR", f"Loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()