import time
import requests
import droidrun as dr
import datetime
from rich.console import Console

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

# --- CORE LOGIC ---
def get_protocol():
    """Syncs with the DroidRun Command Center."""
    try:
        response = requests.get(f"{SERVER_URL}/api/config", timeout=0.8)
        return response.json()
    except:
        return {"blacklist": [], "is_happy": False}

def report_threat(reason):
    """Logs the violation to the DroidRun dashboard."""
    try:
        requests.post(f"{SERVER_URL}/api/violation", json={"reason": reason}, timeout=0.8)
    except:
        pass

def ai_analysis(title):
    """Uses LLM to detect brainrot content."""
    prompt = f"Analyze title: '{title}'. Reply BLOCK for entertainment/vlogs/pranks. Reply ALLOW for education. One word only."
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False}, timeout=5)
        return r.json()["response"].strip().upper()
    except:
        return "ALLOW"

def main():
    console.print("🚀 [bold]DroidRun Native Sentinel[/bold] initialized.", style="green")
    
    # Initialize the native DroidRun bridge
    # Unlike u2, this doesn't restart the Accessibility Service
    agent = dr.Agent(health_check=False)
    
    if not agent.is_connected():
        console.print("❌ Failed to bind to DroidRun Service. Check ADB.", style="red")
        return

    console.print(f"📱 Sentinel Active on: {agent.device_serial}")
    console.print("▶️ Protocol: Monitoring for Brainrot...")

    step = 1
    while True:
        try:
            # 1. Fetch current instructions from server
            protocol = get_protocol()
            
            # If in Happy Hour, the agent enters 'Observational' mode
            if protocol.get("is_happy"):
                log("INFO", "Ceasefire Active. Agent in Standby.", style="dim cyan")
                time.sleep(10)
                continue

            # 2. Inspect the foreground app
            # Native DroidRun inspects the layout without 'freezing' the UI
            app_state = agent.get_foreground_state()
            current_app = app_state.package
            
            violation = False
            reason = ""

            # --- TARGET: YOUTUBE ---
            if current_app == "com.google.android.youtube":
                # Check for Shorts (Native ID detection)
                if agent.exists(resourceId="com.google.android.youtube:id/reel_recycler"):
                    violation, reason = True, "YouTube Shorts"
                else:
                    title = agent.find(resourceId="com.google.android.youtube:id/title").text()
                    if title:
                        if any(bad in title.lower() for bad in protocol.get("blacklist", [])):
                            violation, reason = True, f"Keyword: {title}"
                        elif ai_analysis(title) == "BLOCK":
                            violation, reason = True, f"AI Decision: {title}"

            # --- TARGET: INSTAGRAM ---
            elif current_app == "com.instagram.android":
                violation, reason = True, "Instagram Restrictions"

            # --- TARGET: CHROME (URL Detection) ---
            elif current_app == "com.android.chrome":
                url = agent.find(resourceId="com.android.chrome:id/url_bar").text()
                if url and "shorts" in url.lower():
                    violation, reason = True, "Browser Bypass: Shorts"

            # --- INTERVENTION ---
            if violation:
                log("WARNING", f"Threat Neutralized: {reason}", style="bold red")
                report_threat(reason)
                
                # Command the device to move to safety
                agent.press_home()
                agent.launch(PENALTY_APP)
                log("INFO", f"User redirected to {PENALTY_APP}")

            time.sleep(2)
            step += 1

        except KeyboardInterrupt:
            break
        except Exception as e:
            log("ERROR", f"Sentinel Loop Glitch: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()