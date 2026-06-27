# FutureAcad.ae

Full-stack site for **FutureAcad** — a Deep Tech Initiative by Rooman (Dubai).
A cinematic, WebGL-driven frontend with a Flask backend that captures leads and
serves a password-protected admin dashboard.

## Stack
- **Frontend** — vanilla HTML/CSS/JS, Three.js (neural world), GSAP + ScrollTrigger, Lenis. No build step.
- **Backend** — Python / Flask, SQLite (zero-config), server-rendered Jinja templates.

## Project layout
```
.
├── run.py                # dev entrypoint
├── config.py             # env-driven config
├── requirements.txt
├── .env.example          # copy to .env
├── instance/             # SQLite db (auto-created, gitignored)
└── app/
    ├── __init__.py       # app factory, error pages, security headers
    ├── routes.py         # public pages + /api/contact
    ├── admin.py          # /admin login, dashboard, CSV export
    ├── db.py             # SQLite (leads table)
    ├── utils.py          # CSRF + email helpers
    ├── data.py           # ecosystem project list
    ├── templates/        # base, index, about, services, work, contact, admin/*
    └── static/
        ├── css/          # styles.css (site) · admin.css
        ├── js/           # world.js · site.js · home.js · contact.js
        └── img/          # logos, favicons
```

## Run locally (Windows / macOS / Linux)
```bash
# 1. create + activate a virtualenv
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 2. install
pip install -r requirements.txt

# 3. configure
copy .env.example .env         # then edit SECRET_KEY + ADMIN_PASSWORD

# 4. run
python run.py
```
Open **http://127.0.0.1:5000**. Admin: **http://127.0.0.1:5000/admin**
(default `admin` / `futureacad` — change in `.env`).

## Pages
| Route | Page |
|-------|------|
| `/` | Cinematic home (6-scene journey) |
| `/about` | About |
| `/services` | Services |
| `/work` | Live platforms |
| `/contact` | Contact form |
| `/admin` | Leads dashboard (login required) |
| `/api/contact` | `POST` JSON — stores a lead |
| `/healthz` | Health check |

## Leads
Contact submissions are validated (server + client), protected by a CSRF token
and a honeypot, **stored in the database, and emailed** to `LEAD_NOTIFY`.
View/export them at `/admin`.

The data layer auto-selects its backend:
- **Local** → SQLite (`instance/futureacad.db`), zero setup.
- **Vercel** → Postgres, used automatically whenever `POSTGRES_URL` is present.

## Deploy to Vercel (Postgres + email)

1. **Push to GitHub**, then in Vercel: *Add New → Project → import the repo.*
   The included `vercel.json` + `api/index.py` configure the Python build.

2. **Add Postgres** — in the project, *Storage → Create → Postgres* (free tier),
   connect it to the project. Vercel injects `POSTGRES_URL` automatically; the
   app creates the `leads` table on first boot.

3. **Set Environment Variables** (Project → Settings → Environment Variables):
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | output of `python -c "import secrets;print(secrets.token_hex(32))"` |
   | `ADMIN_USERNAME` | your admin user |
   | `ADMIN_PASSWORD` | a strong password |
   | `SESSION_COOKIE_SECURE` | `1` |
   | `SMTP_HOST` | `smtp.gmail.com` |
   | `SMTP_PORT` | `587` |
   | `SMTP_USER` | your Gmail address |
   | `SMTP_PASSWORD` | Gmail **App Password** (16 chars) |
   | `SMTP_FROM` | your Gmail address |
   | `LEAD_NOTIFY` | inbox that should receive leads |

4. **Deploy.** Every contact submission is saved to Postgres **and** emailed to
   `LEAD_NOTIFY`. Admin dashboard + CSV export run against Postgres.

> CLI alternative: `npm i -g vercel && vercel` (then `vercel --prod`).

## Deploy elsewhere (Render / Railway / VPS)
Runs as a normal WSGI app — SQLite works with a persistent disk:
```bash
gunicorn "app:create_app()" -b 0.0.0.0:8000   # Linux
waitress-serve --listen=0.0.0.0:8000 "app:create_app"   # Windows
```
