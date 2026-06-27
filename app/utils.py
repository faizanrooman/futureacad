"""Small helpers: CSRF tokens and best-effort email notification."""
import hmac
import secrets
import smtplib
from email.message import EmailMessage
from flask import session, current_app


def ensure_csrf():
    """Return the session CSRF token, creating one if needed."""
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def valid_csrf(token):
    expected = session.get("csrf")
    return bool(expected) and bool(token) and hmac.compare_digest(expected, token)


def send_lead_email(lead):
    """Notify the team about a new lead. No-op unless SMTP is configured.
    Never raises — email failure must not break the submission."""
    cfg = current_app.config
    host = cfg.get("SMTP_HOST")
    to = cfg.get("LEAD_NOTIFY")
    if not host or not to:
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = f"New FutureAcad lead — {lead['name']} ({lead['interest']})"
        msg["From"] = cfg["SMTP_FROM"]
        msg["To"] = to
        msg.set_content(
            "New strategy-session enquiry:\n\n"
            f"Name:     {lead['name']}\n"
            f"Email:    {lead['email']}\n"
            f"Company:  {lead['company'] or '-'}\n"
            f"Interest: {lead['interest']}\n\n"
            f"Message:\n{lead['message']}\n"
        )
        with smtplib.SMTP(host, cfg["SMTP_PORT"], timeout=10) as s:
            s.starttls()
            if cfg.get("SMTP_USER"):
                s.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
            s.send_message(msg)
        return True
    except Exception as e:  # pragma: no cover
        current_app.logger.warning("Lead email failed: %s", e)
        return False
