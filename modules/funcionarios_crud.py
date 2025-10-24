from supabase_client import supabase
import pandas as pd

def listar_funcionarios():
    res = supabase.table("funcionarios").select("*").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=["id","obra_id","data","funcionario","presente","observacoes"])

def inserir_funcionario(obra_id, data, funcionario, presente, observacoes):
    supabase.table("funcionarios").insert({
        "obra_id": obra_id,
        "data": data,
        "funcionario": funcionario,
        "presente": presente,
        "observacoes": observacoes
    }).execute()
