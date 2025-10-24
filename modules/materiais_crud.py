from supabase_client import supabase
import pandas as pd

def listar_materiais():
    res = supabase.table("materiais").select("*").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=["id","obra_id","data","material","custo","observacoes"])

def inserir_material(obra_id, data, material, custo, observacoes):
    supabase.table("materiais").insert({
        "obra_id": obra_id,
        "data": data,
        "material": material,
        "custo": custo,
        "observacoes": observacoes
    }).execute()
