from supabase import create_client, Client
from ..config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
# Use SERVICE_KEY for full access; for row-level security later, use anon key on client side.

