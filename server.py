from flask import Flask, render_template_string, request, jsonify, redirect
import json
import os
import datetime
import random

app = Flask(__name__)
DATA_FILE = "parent_settings.json"

# --- DEFAULT SETTINGS ---
default_data = {
    "happy_hour_start": "16:00", 
    "happy_hour_end": "17:00",
    "blacklist": ["skibidi", "prank", "brainrot", "sex", "hot", "kiss"],
    "violations": [],
    "last_reset": datetime.date.today().isoformat()
}

AGENT_QUOTES = [
    "Discipline is the bridge between goals and accomplishment.",
    "I am watching, so you don't have to.",
    "Productivity is being protected.",
    "The scroll has been halted.",
    "Focus is the new currency."
]

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(default_data)
        return default_data
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Reset violations daily
    today_str = datetime.date.today().isoformat()
    if data.get("last_reset") != today_str:
        data["violations"] = []
        data["last_reset"] = today_str
        save_data(data)
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def is_ceasefire_active(start_str, end_str):
    """The 'Wise' Time Check: Handles midnight crossing and minute precision."""
    try:
        now = datetime.datetime.now().time()
        start = datetime.time.fromisoformat(start_str)
        end = datetime.time.fromisoformat(end_str)
        if start <= end:
            return start <= now <= end
        else: # Midnight crossover
            return now >= start or now <= end
    except:
        return False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DroidRun Command</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; color: #212529; font-family: 'Inter', sans-serif; }
        .navbar { background-color: #ffffff; border-bottom: 1px solid #eaeaea; padding: 1rem 0; }
        .brand-text { letter-spacing: -0.5px; font-weight: 800; color: #000; }
        .card { border: 1px solid #eaeaea; border-radius: 16px; background: #fff; }
        .btn-primary { background-color: #000; color: #fff; border: none; padding: 12px; border-radius: 8px; font-weight: 600; }
        .btn-primary:hover { background-color: #333; }
        .quote-box { background: #f8f9fa; border-left: 4px solid #000; padding: 1rem; font-style: italic; color: #555; }
        .badge-live { background-color: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; font-weight: 600; }
    </style>
    
    <script>
        // SMART REFRESH: Only reloads if you aren't currently editing a protocol
        setInterval(function() {
            const activeTag = document.activeElement.tagName;
            if (activeTag !== 'INPUT' && activeTag !== 'TEXTAREA') {
                window.location.reload();
            }
        }, 5000); 
    </script>
</head>
<body class="pb-5">
    <nav class="navbar mb-5">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center" href="#">
                <span style="font-size: 1.5rem;">🤖</span> 
                <span class="ms-2 brand-text">DroidRun <span class="text-muted fw-normal" style="font-size: 0.9rem;">/ Command Center</span></span>
            </a>
            <span class="badge badge-live rounded-pill px-3 py-2">● AGENT ONLINE</span>
        </div>
    </nav>

    <div class="container">
        <div class="row mb-4">
            <div class="col-12">
                <div class="quote-box rounded">"{{ quote }}"</div>
            </div>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-md-6">
                <div class="card h-100 p-4">
                    <div class="text-muted small text-uppercase fw-bold mb-1">Interventions</div>
                    <h2 class="mb-0 display-4 fw-bold">{{ data.violations|length }}</h2>
                    <span class="text-danger small fw-bold">actions taken today</span>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card h-100 p-4">
                    <div class="text-muted small text-uppercase fw-bold mb-1">Agent Protocol</div>
                    {% if is_happy %}
                        <h3 class="mb-0 fw-bold text-success">Happy Hour</h3>
                        <small class="text-muted">Status: <span class="fw-bold">Observing</span></small>
                    {% else %}
                        <h3 class="mb-0 fw-bold text-primary">Parental Control ON</h3>
                        <small class="text-muted">Status: <span class="fw-bold">Intervening</span></small>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-md-5">
                <div class="card p-4">
                    <h5 class="fw-bold mb-4">Agent Instructions</h5>
                    <form action="/update" method="post">
                        <div class="mb-4">
                            <label class="form-label fw-bold small text-uppercase">Ceasefire Window</label>
                            <div class="input-group">
                                <input type="time" class="form-control bg-light" name="start" value="{{ data.happy_hour_start }}">
                                <span class="input-group-text bg-light border-0">to</span>
                                <input type="time" class="form-control bg-light" name="end" value="{{ data.happy_hour_end }}">
                            </div>
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-bold small text-uppercase">Target Keywords</label>
                            <textarea class="form-control bg-light" name="blacklist" rows="5" placeholder="Comma separated...">{{ ', '.join(data.blacklist) }}</textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 shadow-sm">Update Protocols</button>
                    </form>
                </div>
            </div>

            <div class="col-md-7">
                <div class="card">
                    <div class="p-4 border-bottom d-flex justify-content-between">
                        <h5 class="fw-bold mb-0">Mission Log</h5>
                        <span class="badge bg-light text-dark border">Real-Time</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="bg-light">
                                <tr>
                                    <th class="ps-4">Timestamp</th>
                                    <th>Threat</th>
                                    <th class="text-end pe-4">Outcome</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for v in data.violations|reverse %}
                                <tr>
                                    <td class="ps-4 text-secondary small fw-bold">{{ v.time }}</td>
                                    <td class="fw-semibold">{{ v.reason }}</td>
                                    <td class="text-end pe-4"><span class="badge bg-danger rounded-pill px-3">Halted</span></td>
                                </tr>
                                {% endfor %}
                                {% if data.violations|length == 0 %}
                                <tr><td colspan="3" class="text-center text-muted p-5"><em>Target is complying with directives.</em></td></tr>
                                {% endif %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    data = load_data() 
    is_happy = is_ceasefire_active(data['happy_hour_start'], data['happy_hour_end'])
    quote = random.choice(AGENT_QUOTES)
    return render_template_string(HTML_TEMPLATE, data=data, is_happy=is_happy, quote=quote)

@app.route('/update', methods=['POST'])
def update_settings():
    data = load_data()
    data['happy_hour_start'] = request.form['start']
    data['happy_hour_end'] = request.form['end']
    data['blacklist'] = [x.strip() for x in request.form['blacklist'].split(',') if x.strip()]
    save_data(data)
    return redirect('/')

@app.route('/api/config')
def get_config():
    data = load_data()
    data['is_happy'] = is_ceasefire_active(data['happy_hour_start'], data['happy_hour_end'])
    return jsonify(data)

@app.route('/api/violation', methods=['POST'])
def log_violation():
    data = load_data()
    violation = request.json
    violation['time'] = datetime.datetime.now().strftime("%I:%M %p") 
    data['violations'].append(violation)
    save_data(data)
    return jsonify({"status": "logged"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)