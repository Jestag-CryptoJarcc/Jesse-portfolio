from flask import Blueprint, request
from datetime import datetime
import os

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/my-projects')
def my_projects():
    dark_mode = request.cookies.get('dark_mode', 'off')
    site_dir = os.path.dirname(__file__)
    site_files = ["app.py", "home.py", "about.py", "projects.py"]
    existing_files = [os.path.join(site_dir, f) for f in site_files if os.path.exists(os.path.join(site_dir, f))]
    if existing_files:
        created_ts = min(os.path.getmtime(f) for f in existing_files)
        updated_ts = max(os.path.getmtime(f) for f in existing_files)
    else:
        created_ts = updated_ts = datetime.now().timestamp()
    created_at = datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d %H:%M")
    updated_at = datetime.fromtimestamp(updated_ts).strftime("%Y-%m-%d %H:%M")
    style = f'''
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
            --dot-color: {'rgba(242, 193, 78, 0.45)' if dark_mode == 'on' else 'rgba(31, 42, 48, 0.35)'};
            --line-rgb: {'123, 223, 242' if dark_mode == 'on' else '31, 42, 48'};
            --line-alpha: {'0.18' if dark_mode == 'on' else '0.28'};
            --outline-bg: {'rgba(255, 255, 255, 0.08)' if dark_mode == 'on' else 'rgba(0, 0, 0, 0.04)'};
            --outline-border: {'rgba(255, 255, 255, 0.28)' if dark_mode == 'on' else 'rgba(0, 0, 0, 0.2)'};
            --outline-text: {'#e9f1f7' if dark_mode == 'on' else '#1f2a30'};
            --card-border: {'rgba(255, 255, 255, 0.08)' if dark_mode == 'on' else 'rgba(0, 0, 0, 0.14)'};
            --card-shadow: {'0 18px 50px rgba(0, 0, 0, 0.28)' if dark_mode == 'on' else '0 18px 40px rgba(15, 20, 24, 0.18)'};
            background: radial-gradient(1200px 600px at 10% -10%, var(--accent-2), transparent 45%),
                        radial-gradient(900px 500px at 110% 10%, var(--accent), transparent 50%),
                        linear-gradient(160deg, var(--bg-1), var(--bg-2));
            color: var(--ink);
            font-family: 'Space Grotesk', system-ui, sans-serif;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }}
        #bg-canvas {{
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }}
        .page {{
            position: relative;
            z-index: 1;
        }}
        .page {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 48px 20px 64px;
        }}
        h1 {{
            font-family: 'Fraunces', serif;
            font-size: clamp(28px, 3.5vw, 44px);
            margin: 0 0 12px;
        }}
        .lead {{
            color: var(--muted);
            font-size: 18px;
            margin: 0 0 24px;
        }}
        .card {{
            background: var(--card);
            border-radius: 22px;
            padding: 26px;
            box-shadow: var(--card-shadow);
            border: 1px solid var(--card-border);
            animation: floatIn 700ms ease both;
        }}
        .footer {{
            margin-top: 26px;
            padding: 12px 12px 4px;
            border-top: 1px solid var(--outline-border);
            font-size: 12px;
            color: var(--muted);
        }}
        .footer-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px 14px;
            align-items: center;
            justify-content: space-between;
        }}
        .footer-right {{
            text-align: right;
            margin-left: auto;
        }}
        .footer-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .footer a {{
            color: var(--outline-text);
            text-decoration: none;
            padding: 2px 0;
            border-bottom: 1px solid transparent;
        }}
        .footer a:hover {{
            border-bottom-color: var(--outline-text);
        }}
        .quote {{
            font-style: italic;
            opacity: 0.8;
            transition: opacity 600ms ease;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }}
        .section-title {{
            font-size: 14px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--muted);
            margin: 18px 0 10px;
        }}
        .link-card {{
            background: {'rgba(255, 255, 255, 0.06)' if dark_mode == 'on' else 'rgba(0, 0, 0, 0.03)'};
            border-radius: 16px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border: 1px solid var(--card-border);
            transition: transform 200ms ease, border-color 200ms ease;
        }}
        .link-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.2);
        }}
        .chip {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 14px;
            border-radius: 999px;
            text-decoration: none;
            font-weight: 600;
            color: #0d0f12;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
        }}
        .chip.secondary {{
            background: var(--outline-bg);
            color: var(--outline-text);
            border: 1px solid var(--outline-border);
        }}
        .toggle-btn {{
            background: var(--outline-bg);
            color: var(--outline-text);
            border: 1px solid var(--outline-border);
            border-radius: 999px;
            padding: 8px 14px;
            font-weight: 600;
            cursor: pointer;
        }}
        .home-link {{
            margin-top: 18px;
            display: inline-flex;
        }}
        @keyframes floatIn {{
            from {{
                opacity: 0;
                transform: translateY(18px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        @media (max-width: 600px) {{
            .page {{
                padding: 28px 16px 48px;
            }}
            .card {{
                padding: 20px;
            }}
            .grid {{
                grid-template-columns: 1fr;
            }}
            .footer-row {{
                flex-direction: column;
                align-items: flex-start;
                gap: 6px;
            }}
            .footer-right {{
                text-align: left;
            }}
        }}
    </style>
    '''
    return style + f'''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <canvas id="bg-canvas" aria-hidden="true"></canvas>
    <main class="page">
        <section class="card">
            <form method="POST" action="/toggle-dark">
                <button class="toggle-btn" type="submit">Toggle Dark Mode</button>
            </form>
            <div style="height: 14px;"></div>
            <h1>Projects & Socials</h1>
            <p class="lead">A quick index of what I am building and the places I am active.</p>

            <div class="section-title">Smellow's Project</div>
            <div class="grid">
                <div class="link-card">
                    <strong>Website</strong>
                    <span style="color: var(--muted);">Main hub</span>
                    <a class="chip" href="https://smellowsproject.com" target="_blank">Open Site</a>
                </div>
                <div class="link-card">
                    <strong>X</strong>
                    <span style="color: var(--muted);">Updates and announcements</span>
                    <a class="chip secondary" href="https://x.com/SmellowsProject" target="_blank">View X</a>
                </div>
                <div class="link-card">
                    <strong>Discord</strong>
                    <span style="color: var(--muted);">Community chat</span>
                    <a class="chip secondary" href="https://discord.gg/smlo" target="_blank">Join Discord</a>
                </div>
            </div>

            <div class="section-title">CryptoJar.cc</div>
            <div class="grid">
                <div class="link-card">
                    <strong>Website</strong>
                    <span style="color: var(--muted);">App and info</span>
                    <a class="chip" href="https://cryptojar.cc/app/" target="_blank">Open Site</a>
                </div>
                <div class="link-card">
                    <strong>X</strong>
                    <span style="color: var(--muted);">News and features</span>
                    <a class="chip secondary" href="https://x.com/CryptoJarcc" target="_blank">View X</a>
                </div>
                <div class="link-card">
                    <strong>Discord</strong>
                    <span style="color: var(--muted);">Community chat</span>
                    <a class="chip secondary" href="https://discord.gg/cjar" target="_blank">Join Discord</a>
                </div>
            </div>

            <div class="section-title">Primary</div>
            <div class="grid">
                <div class="link-card">
                    <strong>GitHub</strong>
                    <span style="color: var(--muted);">Code and experiments</span>
                    <a class="chip" href="https://github.com/Jestag-CryptoJarcc" target="_blank">Visit GitHub</a>
                </div>
            </div>

            <a class="home-link chip secondary" href="/">Home</a>
        </section>
    </main>
    <footer class="footer">
        <div class="footer-row">
            <div>Created: {created_at} · Last updated: {updated_at}</div>
            <div class="footer-right">
                <div class="quote" id="crypto-quote">Building the future, one block at a time.</div>
                <div style="height: 4px;"></div>
                <div>Built with Flask</div>
            </div>
        </div>
        <div style="height: 6px;"></div>
        <div class="footer-links">
            <a href="https://discord.gg/smlo" target="_blank">Smellow's Project Discord</a>
            <a href="https://discord.gg/cjar" target="_blank">CryptoJar.cc Discord</a>
            <a href="/about">About</a>
            <a href="/">Home</a>
        </div>
    </footer>
    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        let dots = [];
        let width = 0;
        let height = 0;

        function resizeCanvas() {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            const count = Math.min(90, Math.floor((width * height) / 18000));
            dots = Array.from({{ length: count }}, () => ({{
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                r: 1.2 + Math.random() * 1.2
            }}));
        }}

        function draw() {{
            const styles = getComputedStyle(document.body);
            const dotColor = styles.getPropertyValue('--dot-color').trim();
            const lineRgb = styles.getPropertyValue('--line-rgb').trim();
            const lineAlpha = parseFloat(styles.getPropertyValue('--line-alpha')) || 0.2;
            ctx.clearRect(0, 0, width, height);
            const maxDist = 140;

            for (let i = 0; i < dots.length; i++) {{
                const d = dots[i];
                d.x += d.vx;
                d.y += d.vy;
                if (d.x < 0 || d.x > width) d.vx *= -1;
                if (d.y < 0 || d.y > height) d.vy *= -1;
            }}

            for (let i = 0; i < dots.length; i++) {{
                const a = dots[i];
                for (let j = i + 1; j < dots.length; j++) {{
                    const b = dots[j];
                    const dx = a.x - b.x;
                    const dy = a.y - b.y;
                    const dist = Math.hypot(dx, dy);
                    if (dist < maxDist) {{
                        const alpha = 1 - dist / maxDist;
                        ctx.strokeStyle = 'rgba(' + lineRgb + ',' + (alpha * lineAlpha) + ')';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(a.x, a.y);
                        ctx.lineTo(b.x, b.y);
                        ctx.stroke();
                    }}
                }}
            }}

            for (let i = 0; i < dots.length; i++) {{
                const d = dots[i];
                ctx.fillStyle = dotColor;
                ctx.beginPath();
                ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
                ctx.fill();
            }}

            requestAnimationFrame(draw);
        }}

        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();
        draw();
    </script>
    <script>
        const quotes = [
            "Building the future, one block at a time.",
            "Slow and steady wins the chain.",
            "Curiosity is the best wallet.",
            "Be early, be humble, keep learning.",
            "Every block is progress.",
            "Community makes the network stronger.",
            "Think long-term, build long-term.",
            "Good tech, good people, good vibes.",
            "Keep building, keep shipping.",
            "Trust the process, not the hype.",
            "Learning compounds faster than interest.",
            "Small steps, strong network.",
            "Ship fast, fix faster.",
            "Patience is a superpower.",
            "Ideas are cheap, execution is rare.",
            "Stay curious, stay kind.",
            "Progress beats perfection.",
            "Make it simple, make it strong."
        ];
        const quoteEl = document.getElementById('crypto-quote');
        let qi = Math.floor(Math.random() * quotes.length);
        quoteEl.textContent = quotes[qi];
        setInterval(() => {{
            quoteEl.style.opacity = '0';
            setTimeout(() => {{
                let next = Math.floor(Math.random() * quotes.length);
                if (quotes.length > 1) {{
                    while (next === qi) {{
                        next = Math.floor(Math.random() * quotes.length);
                    }}
                }}
                qi = next;
                quoteEl.textContent = quotes[qi];
                quoteEl.style.opacity = '0.8';
            }}, 600);
        }}, 6000);
    </script>
    '''
