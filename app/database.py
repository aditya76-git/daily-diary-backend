from supabase import create_client
from config import Config

supabase_db = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)