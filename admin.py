from flask import Blueprint, request, redirect, make_response
from werkzeug.utils import secure_filename
import os
import time

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

def is_authed(req):
    return req.cookies.get('admin_auth') == '1'

def get_admin_password():
    return os.getenv('ADMIN_PASSWORD', '')

def allowed_file(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

@admin_bp.route('/admin')
def admin():
    password_set = bool(get_admin_password())
    dark_mode = request.cookies.get('dark_mode', 'off')
    if not is_authed(request):
        return render_admin_page(f'''
        <div class="card">
            <h2>Admin Login</h2>
            <p class="msg">{'Set ADMIN_PASSWORD in your environment first.' if not password_set else 'Enter password to continue.'}</p>
            <form method="POST" action="/admin/login">
                <input type="password" name="password" placeholder="Password" {'disabled' if not password_set else ''}>
                <button type="submit" {'disabled' if not password_set else ''}>Login</button>
            </form>
        </div>
        ''', dark_mode)
    return admin_panel("")

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    password = request.form.get('password', '')
    if password and password == get_admin_password():
        resp = make_response(redirect('/admin'))
        resp.set_cookie('admin_auth', '1', max_age=60*60*6)
        return resp
    return admin_panel("Wrong password.")

@admin_bp.route('/admin/upload', methods=['POST'])
def admin_upload():
    if not is_authed(request):
        return redirect('/admin')
    theme = request.form.get('theme', '').strip().lower()
    file = request.files.get('file')
    if not file or file.filename == '':
        return admin_panel("No file selected.")
    if not allowed_file(file.filename):
        return admin_panel("Only JPG, PNG, WEBP allowed.")

    uploads_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    safe_name = secure_filename(file.filename)
    timestamp = int(time.time())
    filename = f"{theme}_{timestamp}_{safe_name}"
    file.save(os.path.join(uploads_dir, filename))
    return admin_panel(f"Uploaded {filename}")

def admin_panel(message):
    if not is_authed(request):
        password_set = bool(get_admin_password())
        return render_admin_page(f'''
        <div class="card">
            <h2>Admin Login</h2>
            <p class="msg">{message or ('Set ADMIN_PASSWORD in your environment first.' if not password_set else 'Enter password to continue.')}</p>
            <form method="POST" action="/admin/login">
                <input type="password" name="password" placeholder="Password" {'disabled' if not password_set else ''}>
                <button type="submit" {'disabled' if not password_set else ''}>Login</button>
            </form>
        </div>
        ''', request.cookies.get('dark_mode', 'off'))
    return render_admin_page(f'''
    <div class="card">
        <h2>Admin Upload</h2>
        <p class="msg">{message}</p>
        <form method="POST" action="/admin/upload" enctype="multipart/form-data">
            <label>Theme</label>
            <select name="theme">
                <option value="crypto">crypto</option>
                <option value="animals">animals</option>
                <option value="music">music</option>
                <option value="travels">travels</option>
                <option value="food">food</option>
                <option value="games">games</option>
                <option value="photography">photography</option>
                <option value="movies">movies/series</option>
            </select>
            <input type="file" name="file" />
            <button type="submit">Upload</button>
        </form>
        <p>Uploaded images will appear in the home page mood board for their theme.</p>
    </div>
    ''', request.cookies.get('dark_mode', 'off'))

def render_admin_page(content, dark_mode):
    return f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        body {{
            --bg-1: {'#0f1418' if dark_mode == 'on' else '#f7f4ef'};
            --bg-2: {'#0b0f12' if dark_mode == 'on' else '#f0ede7'};
            --card: {'#12181e' if dark_mode == 'on' else '#ffffff'};
            --ink: {'#e9f1f7' if dark_mode == 'on' else '#1f2a30'};
            --muted: {'#9fb1bd' if dark_mode == 'on' else '#5a6a73'};
            --accent: {'#f2c14e' if dark_mode == 'on' else '#d96b24'};
            --accent-2: {'#7bdff2' if dark_mode == 'on' else '#4c9ff0'};
            --outline-bg: {'rgba(255, 255, 255, 0.08)' if dark_mode == 'on' else 'rgba(0, 0, 0, 0.04)'};
            --outline-border: {'rgba(255, 255, 255, 0.28)' if dark_mode == 'on' else 'rgba(0, 0, 0, 0.2)'};
            --outline-text: {'#e9f1f7' if dark_mode == 'on' else '#1f2a30'};
            background: radial-gradient(1200px 600px at 10% -10%, var(--accent-2), transparent 45%),
                        radial-gradient(900px 500px at 110% 10%, var(--accent), transparent 50%),
                        linear-gradient(160deg, var(--bg-1), var(--bg-2));
            color: var(--ink);
            font-family: 'Space Grotesk', system-ui, sans-serif;
            min-height: 100vh;
            margin: 0;
            padding: 32px 16px 48px;
        }}
        .card {{
            max-width: 720px;
            margin: 0 auto;
            padding: 26px;
            border-radius: 20px;
            border: 1px solid var(--outline-border);
            background: var(--card);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);
        }}
        h2 {{
            font-family: 'Fraunces', serif;
            margin: 0 0 10px;
        }}
        label {{
            font-size: 13px;
            color: var(--muted);
        }}
        input, select {{
            width: 100%;
            padding: 10px 12px;
            margin: 10px 0 14px;
            border-radius: 12px;
            border: 1px solid var(--outline-border);
            background: var(--outline-bg);
            color: var(--outline-text);
            font-family: inherit;
        }}
        button {{
            padding: 10px 16px;
            border-radius: 999px;
            border: 1px solid var(--outline-border);
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color: #0d0f12;
            font-weight: 600;
            cursor: pointer;
        }}
        .msg {{
            color: var(--muted);
            margin-bottom: 12px;
        }}
    </style>
    {content}
    '''
