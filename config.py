"""Configuration loaded from environment (.env). Sane defaults for local dev."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent


class Config:
    # SECRET_KEY signs the session cookie & CSRF token. MUST be set in production.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")

    # Local dev uses SQLite. On Vercel, Postgres is used automatically when
    # POSTGRES_URL is set (see app/db.py); the SQLite path below is only a
    # fallback and points at writable /tmp on serverless.
    _sqlite_default = "/tmp/futureacad.db" if os.environ.get("VERCEL") else str(BASE_DIR / "instance" / "futureacad.db")
    DATABASE = os.environ.get("DATABASE", _sqlite_default)

    # Admin dashboard credentials.
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "futureacad")

    # Optional SMTP — if SMTP_HOST is set, new leads trigger an email notification.
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
    SMTP_FROM = os.environ.get("SMTP_FROM", "no-reply@futureacad.ae")
    LEAD_NOTIFY = os.environ.get("LEAD_NOTIFY")  # recipient for lead notifications

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Set to True automatically when served over HTTPS in production.
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
