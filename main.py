"""Vercel entrypoint and deployment compatibility adapter.

The API source under app/ is intentionally untouched. This module only adapts
its local import layout and database connection for a serverless runtime.
"""
import os
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "app"
UPLOAD_DIR = ROOT / "upload"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# The API imports `database` as a top-level module and currently hardcodes its
# Docker connection. Provide the same function name using Neon DATABASE_URL,
# without changing any file under app/.
database_compat = types.ModuleType("database")


def conect_database():
    import psycopg

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL não configurada")
    return psycopg.connect(database_url)


database_compat.conect_database = conect_database
sys.modules.setdefault("database", database_compat)

# StaticFiles validates the directory during import. Keep the API source
# unchanged while making the expected ephemeral directory available.
UPLOAD_DIR.mkdir(exist_ok=True)

from app.main import app  # noqa: E402
