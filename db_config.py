import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def connect_db() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY são obrigatórias")

    return create_client(url, key)