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
    """Retorna todos os registros diários com nome da obra"""
    res = (
        supabase.table("diario")
        .select("id, data, obra_id, categoria, custo, progresso, observacoes, obras(nome)")
        .execute()
    )

    df = pd.DataFrame(res.data) if res.data else pd.DataFrame(columns=[
        "id", "data", "obra_id", "categoria", "custo", "progresso", "observacoes", "obras"
    ])

    # Extrai nome da obra (Supabase retorna em dict dentro de 'obras')
    if "obras" in df.columns:
        df["obra"] = df["obras"].apply(lambda x: x["nome"] if isinstance(x, dict) else None)
        df.drop(columns=["obras"], inplace=True)

    return df

def inserir_diario(data, obra_id, categoria, custo, progresso, observacoes):
    """Insere registro diário e retorna DataFrame atualizado"""
    import numpy as np

    # --- Garantir tipos compatíveis com JSON ---
    if isinstance(data, (pd.Timestamp, pd.DatetimeIndex)):
        data = data.strftime("%Y-%m-%d")
    elif hasattr(data, "isoformat"):
        data = data.isoformat()
    else:
        data = str(data)

    # Converte NumPy → tipos nativos Python
    def to_native(value):
        if isinstance(value, (np.int64, np.int32)):
            return int(value)
        elif isinstance(value, (np.float64, np.float32)):
            return float(value)
        return value

    obra_id = to_native(obra_id)
    custo = to_native(custo)
    progresso = to_native(progresso)

    supabase.table("diario").insert({
        "data": data,
        "obra_id": obra_id,
        "categoria": categoria,
        "custo": custo,
        "progresso": progresso,
        "observacoes": observacoes
    }).execute()

    return listar_diario()

