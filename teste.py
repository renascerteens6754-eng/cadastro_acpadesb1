import os
from supabase import create_client, Client

# ======================================================
# !! SUBSTITUA PELAS SUAS CREDENCIAIS REAIS AQUI !!
# ======================================================
SUPABASE_URL = "https://jnpkspwxdbiveqkpualb.supabase.co"  # Ex: "https://exemplo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpucGtzcHd4ZGJpdmVxa3B1YWxiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU5MjAzNjEsImV4cCI6MjA5MTQ5NjM2MX0.tM0fGG0klToWNnt-HHsfT2cpIYTlwxrZRebZ07RSDbI"  # A chave longa

print(f"🔍 Testando conexão com: {SUPABASE_URL}")

try:
    # 1. Tenta criar o cliente
    print("1️⃣ Criando cliente Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente criado.")

    # 2. Tenta fazer uma consulta simples
    print("2️⃣ Consultando a tabela 'adolescentes'...")
    response = supabase.table("adolescentes").select("*", count="exact").execute()

    print(f"✅ Consulta bem-sucedida!")
    print(f"   Total de registros encontrados: {response.count}")

    if response.data:
        print(f"   Primeiro registro: {response.data[0]['nome']}")
    else:
        print("   ⚠️ A consulta funcionou, mas a tabela está vazia ou a RLS está bloqueando a leitura.")

except Exception as e:
    print(f"❌ Erro na conexão ou consulta:")
    print(f"   {e}")