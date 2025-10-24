from supabase_client import supabase
import pandas as pd
import numpy as np


def listar_materiais():
    """Lista materiais com o nome da obra (join)"""
    res = (
        supabase.table("materiais")
        .select("id, data, obra_id, material, quantidade, unidade, custo, obras(nome)")
        .order("data", desc=True)
        .execute()
    )

    data = res.data
    if not data:
        return pd.DataFrame(columns=["id", "data", "obra", "material", "quantidade", "unidade", "custo"])

    df = pd.DataFrame(data)

    # ✅ Extrai o nome da obra do dicionário {"nome": "amab"}
    if "obras" in df.columns:
        df["obra"] = df["obras"].apply(lambda x: x.get("nome") if isinstance(x, dict) else None)
        df.drop(columns=["obras"], inplace=True)

    # ✅ Garante conversão de data
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    return df



def inserir_material(data, obra_id, material, quantidade, unidade, custo):
    """Insere um novo material"""
    # Converte valores para tipos nativos JSON-compatíveis
    if hasattr(data, "isoformat"):
        data = data.isoformat()

    def to_native(val):
        if isinstance(val, (np.int64, np.int32)):
            return int(val)
        elif isinstance(val, (np.float64, np.float32)):
            return float(val)
        return val

    obra_id = to_native(obra_id)
    quantidade = to_native(quantidade)
    custo = to_native(custo)

    supabase.table("materiais").insert({
        "data": data,
        "obra_id": obra_id,
        "material": material,
        "quantidade": quantidade,
        "unidade": unidade,
        "custo": custo
    }).execute()

    return listar_materiais()
