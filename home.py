from flask import Blueprint, request
import os
import random
from datetime import datetime

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    dark_mode = request.cookies.get('dark_mode', 'off')
    uploads_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
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

    themes = [
        {
            "label": "Games",
            "slug": "games",
            "caption": "Favorite games & late-night sessions",
            "details": "My top picks: ARK (Survival Ascended + Survival Evolved), Viewfinder, and Definitely Not Fried Chicken. If it has dinos or clever puzzles, I am in.",
            "fallbacks": [
                "https://cdn.akamai.steamstatic.com/steam/apps/2399830/header.jpg",
                "https://cdn.akamai.steamstatic.com/steam/apps/346110/header.jpg",
                "https://cdn.akamai.steamstatic.com/steam/apps/1382070/header.jpg",
                "https://cdn.akamai.steamstatic.com/steam/apps/1036240/header.jpg",
            ],
        },
        {
            "label": "Food",
            "slug": "food",
            "caption": "Good food, always.",
            "details": "Fast food is fun, but I love cooking myself. International food is my thing, especially Asian flavors. I like plating at a high homeâ€‘cook level to make it feel special.",
            "fallbacks": [
                "https://upload.wikimedia.org/wikipedia/commons/5/54/Ramen_Bowl.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/8/8e/A_plate_of_sushi.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/6/6c/South-East_Asian_noodle_soup_in_bowl_with_spoon.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/9/9e/Sushi_Plate_%2849062536423%29.jpg",
            ],
        },
        {
            "label": "Music",
            "slug": "music",
            "caption": "Soundtrack while I build.",
            "details": "I have played guitar since I was 6. I love 80sâ€“90s the most, but modern vibes are great too. Festivals are my happy place.",
            "fallbacks": [
                "https://commons.wikimedia.org/wiki/Special:FilePath/Les_Paul_Black_Beauty_50th.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Fender_stratocaster_black.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Mick_Taylor-_John_Mayall_concert_1980s.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Santana_%2B_Zappa%2C_K%C3%B6lner_Sporthalle%2C_1980.jpg",
            ],
        },
        {
            "label": "Movies/Series",
            "slug": "movies",
            "caption": "Stories I get lost in.",
            "details": "I watch a lot, but I am not great at picking. My girlfriend finds the good ones and I end up loving most of them. I love Stranger Things, silly movies, and a good horror night.",
            "fallbacks": [
                "https://commons.wikimedia.org/wiki/Special:FilePath/Haunted_hill.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Night_of_the_Living_Dead_(1968)_-_Zombies.JPG",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Vincent_Price_in_House_on_Haunted_Hill.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Colorful,_neon_sign,_night_Fortepan_75588.jpg",
            ],
        },
        {
            "label": "Crypto",
            "slug": "crypto",
            "caption": "Builders and ideas I follow.",
            "details": "Big fan of Bitcoin (BTC) and Solana (SOL). I built Smellow's Project and CryptoJar.cc with awesome people I met on Discord.",
            "fallbacks": [
                "https://commons.wikimedia.org/wiki/Special:FilePath/Bitcoin.svg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Bitcoin_logo.svg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Solana-sol-logo-horizontal-2025.svg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Cryptocurrency_Logo.svg",
            ],
        },
        {
            "label": "Travels",
            "slug": "travels",
            "caption": "New places, new energy.",
            "details": "I love traveling and want to see the whole world. I have already visited a lot of places in Europe, and Japan is a dream destination.",
            "fallbacks": [
                "https://commons.wikimedia.org/wiki/Special:FilePath/WorldMap.svg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Airplane_Flight_Wing_flying_to_Travel_on_Vacation.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Vacation_cove_%28Unsplash%29.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Tokyo_Skyline.jpg",
            ],
        },
        {
            "label": "Photography",
            "slug": "photography",
            "caption": "Catching the little moments.",
            "details": "I recently got a phone with a great camera. I love taking photos of my surroundings and editing them.",
            "fallbacks": [
                "https://commons.wikimedia.org/wiki/Special:FilePath/MountainLandscape.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Landscape-nature-forest-trees_%2824244423731%29.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/City_Skyline_-_panoramio.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/City_Skyline_%286022299679%29.jpg",
            ],
        },
        {
            "label": "Animals",
            "slug": "animals",
            "caption": "My softer side.",
            "details": "I have a pet snake and used to keep some unusual pets like a gecko, insects, and a scorpion. Right now, the snake has the best spot at home.",
            "fallbacks": [
                "https://commons.wikimedia.org/wiki/Special:FilePath/Corn_Snake,_NPSPhoto_(9255026919).jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Heterometrus_cyaneus_Schwarzer_Asiaskorpion.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/A_praying_mantis_1.jpg",
                "https://commons.wikimedia.org/wiki/Special:FilePath/Cyrtodactylus_brevipalmatus,_Short-hand_forest_gecko.jpg",
            ],
        },
    ]

    order = [
        "crypto",
        "animals",
        "music",
        "travels",
        "food",
        "games",
        "photography",
        "movies",
    ]
    order_index = {slug: idx for idx, slug in enumerate(order)}
    themes.sort(key=lambda theme: order_index.get(theme["slug"], 999))

    def pick_image(slug, fallbacks):
        if os.path.isdir(uploads_dir):
            matches = [
                name for name in os.listdir(uploads_dir)
                if name.lower().startswith(slug.lower() + "_")
            ]
            if matches:
                return f"/static/uploads/{random.choice(matches)}"
        return random.choice(fallbacks)

    polaroids = []
    for theme in themes:
        image_url = pick_image(theme["slug"], theme["fallbacks"])
        polaroids.append(f'''
        <div class="polaroid">
            <div class="photo">
                <img src="{image_url}" alt="{theme["label"]} image">
            </div>
            <div class="caption">
                <strong>{theme["label"]}</strong>
                <span>{theme["caption"]}</span>
            </div>
            <div class="details">
                {theme.get("details", "")}
            </div>
        </div>
        ''')

    polaroids_html = "".join(polaroids)

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
            --polaroid-bg: {'#1f262d' if dark_mode == 'on' else '#fffaf2'};
            --polaroid-ink: {'#e5edf3' if dark_mode == 'on' else '#2b2f33'};
            --polaroid-muted: {'#b5c3cd' if dark_mode == 'on' else '#57646c'};
            --polaroid-frame: {'#2b343d' if dark_mode == 'on' else '#f1ebe1'};
            --dot-color: {'rgba(242, 193, 78, 0.45)' if dark_mode == 'on' else 'rgba(31, 42, 48, 0.35)'};
            --line-rgb: {'123, 223, 242' if dark_mode == 'on' else '31, 42, 48'};
            --line-alpha: {'0.18' if dark_mode == 'on' else '0.28'};
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
            padding: 0;
            position: relative;
            overflow-x: hidden;
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
            max-width: 920px;
            margin: 0 auto;
            padding: 48px 20px 64px;
        }}
        .hero {{
            display: grid;
            gap: 18px;
            align-items: center;
            text-align: left;
        }}
        .kicker {{
            letter-spacing: 0.2em;
            text-transform: uppercase;
            font-size: 12px;
            color: var(--muted);
        }}
        h1 {{
            font-family: 'Fraunces', serif;
            font-size: clamp(32px, 4vw, 52px);
            margin: 0;
        }}
        .hero p {{
            font-size: 20px;
            color: var(--muted);
            margin: 0;
            line-height: 1.6;
        }}
        .hero-list {{
            margin: 14px 0 0;
            padding-left: 18px;
            color: var(--muted);
            line-height: 1.6;
        }}
        .hero-list li {{
            margin-bottom: 6px;
        }}
        .hero-list .hero-pill {{
            list-style: none;
            padding: 0;
            margin: 0 0 10px -18px;
        }}
        .hero-list .hero-pill::marker {{
            content: "";
        }}
        .hero-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            color: var(--muted);
            font-size: 13px;
        }}
        .card {{
            background: var(--card);
            border-radius: 22px;
            padding: 28px;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
            border: 1px solid rgba(255, 255, 255, 0.08);
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
        .mood-board {{
            margin-top: 26px;
        }}
        .board-title {{
            font-size: 14px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 12px;
        }}
        .polaroid-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            overflow: visible;
        }}
        .polaroid {{
            background: var(--polaroid-bg);
            color: var(--polaroid-ink);
            padding: 12px 12px 16px;
            border-radius: 12px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
            transform: rotate(-1deg);
            transition: transform 200ms ease, box-shadow 200ms ease;
            position: relative;
        }}
        .polaroid:nth-child(2n) {{
            transform: rotate(1.2deg);
        }}
        .polaroid:hover {{
            transform: translateY(-6px) rotate(0deg) scale(1.12);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
            z-index: 5;
        }}
        .photo {{
            width: 100%;
            height: 190px;
            border-radius: 8px;
            margin-bottom: 10px;
            transition: height 200ms ease;
            background: var(--polaroid-frame);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .polaroid:hover .photo {{
            height: 240px;
        }}
        .photo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .caption strong {{
            display: block;
            font-size: 14px;
        }}
        .caption span {{
            font-size: 12px;
            color: var(--polaroid-muted);
        }}
        .details {{
            margin-top: 8px;
            font-size: 12px;
            color: var(--polaroid-muted);
            max-height: 0;
            opacity: 0;
            overflow: hidden;
            transition: max-height 200ms ease, opacity 200ms ease;
        }}
        .polaroid:hover .details {{
            max-height: 120px;
            opacity: 1;
        }}
        .actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 18px;
            border-radius: 999px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            color: #0d0f12;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
            transition: transform 200ms ease, box-shadow 200ms ease;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 16px 24px rgba(0, 0, 0, 0.3);
        }}
        .btn.secondary {{
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
        .pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            color: var(--muted);
            font-size: 13px;
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
        @media (max-width: 700px) {{
            .hero {{
                text-align: center;
            }}
            .actions {{
                justify-content: center;
            }}
        }}
        @media (max-width: 600px) {{
            .page {{
                padding: 28px 16px 48px;
            }}
            h1 {{
                font-size: clamp(26px, 7vw, 36px);
            }}
            .hero p {{
                font-size: 16px;
            }}
            .hero-list {{
                padding-left: 16px;
            }}
            .card {{
                padding: 20px;
            }}
            .actions {{
                flex-direction: column;
            }}
            .btn {{
                width: 100%;
                justify-content: center;
                padding: 10px 14px;
                font-size: 14px;
            }}
            .polaroid-grid {{
                grid-template-columns: 1fr;
            }}
            .photo {{
                height: 170px;
            }}
            .polaroid:hover .photo {{
                height: 200px;
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
        <div class="hero">
            <span class="kicker">Portfolio</span>
            <h1>Hi, I am Jesse (Jestag). Welcome to my page!</h1>
            <p>I hope you will find out more about me and get to know me a little better.</p>
            <ul class="hero-list">
                <li>I am mostly fun (xP) and pretty much an open book, so feel free to reach out and say hi.</li>
                <li>I enjoy exploring new technologies and building creative projects (mostly involving crypto).</li>
                <li>Currently learning: Python + web apps</li>
                <li>This site is a work in progress, so expect new content and updates over time.</li>
                <li>I will also be sharing some of my projects here, so stay tuned.</li>
            </ul>
        </div>
        <div style="height: 24px;"></div>
        <section class="card">
            <form method="POST" action="/toggle-dark">
                <button class="toggle-btn" type="submit">Toggle Dark Mode</button>
            </form>
            <div style="height: 14px;"></div>
            <div class="actions">
                <a class="btn" href="/about">About Me</a>
                <a class="btn secondary" href="/my-projects">My Projects</a>
            </div>
            <div class="mood-board">
                <div class="board-title">Mood Board</div>
                <div class="polaroid-grid">
                    {polaroids_html}
                </div>
            </div>
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
            <a href="/my-projects">Projects</a>
            <a href="/about">About</a>
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

