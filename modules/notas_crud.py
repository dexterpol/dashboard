from supabase_client import supabase
import pandas as pd
import numpy as np

def listar_notas():
    """Lista notas com o nome da obra"""
    res = (
        supabase.table("notas")
        .select("id, data, obra_id, titulo, descricao, custo, obras(nome)")
        .order("data", desc=True)
        .execute()
    )

    data = res.data
    if not data:
        return pd.DataFrame(columns=["id", "data", "obra", "titulo", "descricao", "custo"])

    df = pd.DataFrame(data)

    # Extrai nome da obra
    if "obras" in df.columns:
        df["obra"] = df["obras"].apply(lambda x: x.get("nome") if isinstance(x, dict) else None)
        df.drop(columns=["obras"], inplace=True)

    # Converte data
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    return df


def inserir_nota(data, obra_id, titulo, descricao, custo):
    """Insere nova nota"""
    if hasattr(data, "isoformat"):
        data = data.isoformat()

    def to_native(val):
        if isinstance(val, (np.int64, np.int32)):
            return int(val)
        elif isinstance(val, (np.float64, np.float32)):
            return float(val)
        return val

    obra_id = to_native(obra_id)
    custo = to_native(custo)

    supabase.table("notas").insert({
        "data": data,
        "obra_id": obra_id,
        "titulo": titulo,
        "descricao": descricao,
        "custo": custo
    }).execute()

    return listar_notas()
