"""Vercel serverless entry — exposes the Flask app as `app` (WSGI)."""
import os
import sys

# Make the project root importable so `app` package resolves on Vercel.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402

app = create_app()
