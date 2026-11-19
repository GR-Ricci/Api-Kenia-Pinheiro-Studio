import os

import psycopg
from dotenv import load_dotenv

load_dotenv()  # útil localmente; na Vercel, use Environment Variables


def conect_database():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não está configurada")

    return psycopg.connect(database_url)