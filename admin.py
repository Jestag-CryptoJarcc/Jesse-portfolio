from flask import Blueprint, request, redirect, make_response, url_for
from werkzeug.utils import secure_filename
import os
import time

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

def is_authed(req):
    return req.cookies.get('admin_auth') == '1' and bool(get_admin_password())

def get_admin_password():
    password = os.getenv('ADMIN_PASSWORD', '')
    if password:
        return password.strip()
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return ''
    try:
        with open(env_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() == "ADMIN_PASSWORD":
                    return value.strip().strip('"').strip("'")
    except OSError:
        return ''
    return ''

def allowed_file(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

def list_uploaded_files():
    uploads_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
    if not os.path.isdir(uploads_dir):
        return "<p class=\"msg\">No uploads yet.</p>"
    files = [
        f for f in os.listdir(uploads_dir)
        if os.path.isfile(os.path.join(uploads_dir, f))
        and not f.startswith(".")
        and allowed_file(f)
    ]
    if not files:
        return "<p class=\"msg\">No uploads yet.</p>"
    cards = []
    for name in sorted(files, reverse=True):
        theme = name.split("_", 1)[0] if "_" in name else "unknown"
        url = url_for('static', filename=f"uploads/{name}")
        cards.append(f'''
        <div class="upload-card">
            <img src="{url}" alt="{name}">
            <div class="meta">
                <div><strong>{theme}</strong></div>
                <div>{name}</div>
                <form method="POST" action="/admin/delete">
                    <input type="hidden" name="filename" value="{name}">
                    <button class="delete-btn" type="submit">Delete</button>
                </form>
            </div>
        </div>
        ''')
    return "".join(cards)

@admin_bp.route('/admin')
def admin():
    password_set = bool(get_admin_password())
    dark_mode = request.cookies.get('dark_mode', 'off')
    if not is_authed(request):
        return render_admin_page(f'''
        <div class="card">
            <h2>Admin Login</h2>
            <p class="msg">{'Set ADMIN_PASSWORD in your environment first.' if not password_set else 'Enter password to continue.'}</p>
            <p class="msg">Password loaded: {"yes" if password_set else "no"}</p>
            <form method="POST" action="/admin/login">
                <input type="password" name="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        </div>
        ''', dark_mode)
    return admin_panel("")

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    password = request.form.get('password', '')
    if password and password.strip() == get_admin_password():
        resp = make_response(redirect('/admin'))
        resp.set_cookie('admin_auth', '1', max_age=60*60*6)
        return resp
    return admin_panel("Wrong password.")

@admin_bp.route('/admin/upload', methods=['POST'])
def admin_upload():
    if not is_authed(request):
        return redirect('/admin')
    theme = request.form.get('theme', '').strip().lower()
    files = request.files.getlist('file')
    if not files or all(f.filename == '' for f in files):
        return admin_panel("No files selected.")

    uploads_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    saved = 0
    skipped = 0
    for file in files:
        if not file or file.filename == '':
            continue
        if not allowed_file(file.filename):
            skipped += 1
            continue
        safe_name = secure_filename(file.filename)
        timestamp = int(time.time() * 1000)
        filename = f"{theme}_{timestamp}_{safe_name}"
        file.save(os.path.join(uploads_dir, filename))
        saved += 1
    msg = f"Uploaded {saved} file(s)." + (f" Skipped {skipped} invalid file(s)." if skipped else "")
    return admin_panel(msg)

@admin_bp.route('/admin/logout')
def admin_logout():
    resp = make_response(redirect('/admin'))
    resp.set_cookie('admin_auth', '', max_age=0)
    return resp

@admin_bp.route('/admin/delete', methods=['POST'])
def admin_delete():
    if not is_authed(request):
        return redirect('/admin')
    filename = request.form.get('filename', '').strip()
    if not filename:
        return admin_panel("No file specified.")
    uploads_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
    file_path = os.path.join(uploads_dir, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return admin_panel(f"Deleted {filename}")
        except OSError:
            return admin_panel("Failed to delete file.")
    return admin_panel("File not found.")

def admin_panel(message):
    if not is_authed(request):
        password_set = bool(get_admin_password())
        return render_admin_page(f'''
        <div class="card">
            <h2>Admin Login</h2>
            <p class="msg">{message or ('Set ADMIN_PASSWORD in your environment first.' if not password_set else 'Enter password to continue.')}</p>
            <form method="POST" action="/admin/login">
                <input type="password" name="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        </div>
        ''', request.cookies.get('dark_mode', 'off'))
    uploads = list_uploaded_files()
    return render_admin_page(f'''
    <div class="card">
        <div class="card-header">
            <h2>Admin Upload</h2>
            <a class="logout" href="/admin/logout">Logout</a>
        </div>
        <p class="msg">{message}</p>
        <form class="upload-form" method="POST" action="/admin/upload" enctype="multipart/form-data">
            <div class="field">
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
            </div>
            <div class="dropzone" id="dropzone">
                <div class="dz-title">Drag & drop images here</div>
                <div class="dz-sub">or click to choose files (JPG, PNG, WEBP)</div>
                <input id="file-input" type="file" name="file" multiple />
            </div>
            <div class="previews" id="previews"></div>
            <button type="submit">Upload</button>
        </form>
        <p>Uploaded images will appear in the home page mood board for their theme.</p>
    </div>
    <div class="card">
        <div class="card-header">
            <h2>Uploaded Images</h2>
        </div>
        <div class="uploads-grid">
            {uploads}
        </div>
    </div>
    <script>
        const dropzone = document.getElementById('dropzone');
        const input = document.getElementById('file-input');
        const previews = document.getElementById('previews');

        dropzone.addEventListener('click', () => input.click());
        dropzone.addEventListener('dragover', (e) => {{
            e.preventDefault();
            dropzone.classList.add('hover');
        }});
        dropzone.addEventListener('dragleave', () => dropzone.classList.remove('hover'));
        dropzone.addEventListener('drop', (e) => {{
            e.preventDefault();
            dropzone.classList.remove('hover');
            input.files = e.dataTransfer.files;
            renderPreviews();
        }});
        input.addEventListener('change', renderPreviews);

        function renderPreviews() {{
            previews.innerHTML = '';
            const files = Array.from(input.files || []);
            files.forEach(file => {{
                const reader = new FileReader();
                reader.onload = (e) => {{
                    const div = document.createElement('div');
                    div.className = 'preview';
                    div.innerHTML = `<img src="${'{'}e.target.result{'}'}" alt="preview"><span>${'{'}file.name{'}'}</span>`;
                    previews.appendChild(div);
                }};
                reader.readAsDataURL(file);
            }});
        }}
    </script>
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
            margin-bottom: 18px;
        }}
        .card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }}
        .logout {{
            font-size: 12px;
            text-decoration: none;
            color: var(--outline-text);
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid var(--outline-border);
            background: var(--outline-bg);
        }}
        .logout:hover {{
            text-decoration: underline;
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
        .upload-form {{
            display: grid;
            gap: 14px;
        }}
        .field label {{
            font-size: 13px;
            color: var(--muted);
        }}
        .dropzone {{
            border: 2px dashed var(--outline-border);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            background: var(--outline-bg);
            cursor: pointer;
        }}
        .dropzone.hover {{
            border-color: var(--accent-2);
        }}
        .dropzone input {{
            display: none;
        }}
        .dz-title {{
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .dz-sub {{
            color: var(--muted);
            font-size: 12px;
        }}
        .previews {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
        }}
        .preview {{
            border: 1px solid var(--outline-border);
            border-radius: 12px;
            overflow: hidden;
            background: var(--outline-bg);
            text-align: center;
            font-size: 11px;
            color: var(--muted);
        }}
        .preview img {{
            width: 100%;
            height: 90px;
            object-fit: cover;
            display: block;
        }}
        .preview span {{
            display: block;
            padding: 6px;
            word-break: break-word;
        }}
        .uploads-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
        }}
        .upload-card {{
            border: 1px solid var(--outline-border);
            border-radius: 14px;
            overflow: hidden;
            background: var(--outline-bg);
        }}
        .upload-card img {{
            width: 100%;
            height: 120px;
            object-fit: cover;
            display: block;
        }}
        .upload-card .meta {{
            padding: 8px 10px;
            font-size: 11px;
            color: var(--muted);
            display: grid;
            gap: 6px;
        }}
        .upload-card form {{
            margin: 0;
        }}
        .delete-btn {{
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid var(--outline-border);
            background: var(--outline-bg);
            color: var(--outline-text);
            font-size: 11px;
            cursor: pointer;
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
