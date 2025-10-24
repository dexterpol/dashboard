from supabase_client import supabase
import pandas as pd

# -------- Obras --------
def listar_obras():
    """Retorna todas as obras como DataFrame"""
    res = supabase.table("obras").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=["id","nome","custo_inicial","funcionarios_iniciais","categoria"])
    return df

def inserir_obra(nome, custo_inicial, funcionarios_iniciais, categoria):
    """Insere uma obra e retorna DataFrame atualizado"""
    supabase.table("obras").insert({
        "nome": nome,
        "custo_inicial": custo_inicial,
        "funcionarios_iniciais": funcionarios_iniciais,
        "categoria": categoria
    }).execute()
    return listar_obras()


# -------- Diário --------
def listar_diario():
    """Retorna todos os registros diários como DataFrame"""
    res = supabase.table("diario").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=["id","data","obra_id","categoria","custo","progresso","observacoes"])
    return df

def inserir_diario(data, obra_id, categoria, custo, progresso, observacoes):
    """Insere registro diário e retorna DataFrame atualizado"""
    supabase.table("diario").insert({
        "data": data,
        "obra_id": obra_id,
        "categoria": categoria,
        "custo": custo,
        "progresso": progresso,
        "observacoes": observacoes
    }).execute()
    return listar_diario()
