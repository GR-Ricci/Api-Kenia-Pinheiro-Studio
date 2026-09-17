import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


CAMINHO_ENV = Path(__file__).resolve().parent.parent / "database" / ".env"
load_dotenv(CAMINHO_ENV)


def conect_database():
    conexao = psycopg.connect(
        host="127.0.0.1",
        port=5433,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conexao