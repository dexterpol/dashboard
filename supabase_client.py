# supabase_client.py
from supabase import create_client, Client

SUPABASE_URL = "https://ivymgddqrphzasqvegve.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2eW1nZGRxcnBoemFzcXZlZ3ZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyNDY3NTIsImV4cCI6MjA3NjgyMjc1Mn0.aMYTixxssGse2NSC7quESgWtviDCoCb-_ZdfwNBa8BU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
