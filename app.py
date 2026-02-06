

from flask import Flask, request, redirect, make_response
import os
from pathlib import Path
from home import home_bp
from about import about_bp
from projects import projects_bp
from admin import admin_bp

def load_env_file():
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

load_env_file()

app = Flask(__name__)

@app.route('/toggle-dark', methods=['POST'])
def toggle_dark():
    dark_mode = request.cookies.get('dark_mode', 'off')
    new_mode = 'off' if dark_mode == 'on' else 'on'
    resp = make_response(redirect(request.referrer or '/'))
    resp.set_cookie('dark_mode', new_mode, max_age=60*60*24*365)
    return resp

# Register Blueprints for each page
app.register_blueprint(home_bp)
app.register_blueprint(about_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
