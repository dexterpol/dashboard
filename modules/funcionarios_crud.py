from supabase_client import supabase
import pandas as pd
import numpy as np

def listar_funcionarios():
    """Lista funcionários com o nome da obra"""
    res = (
        supabase.table("funcionarios")
        .select("id, data, obra_id, nome, funcao, horas_trabalhadas, custo, obras(nome)")
        .order("data", desc=True)
        .execute()
    )

    data = res.data
    if not data:
        return pd.DataFrame(columns=[
            "id", "data", "obra", "nome", "funcao", "horas_trabalhadas", "custo"
        ])

    df = pd.DataFrame(data)

    # Extrair nome da obra
    if "obras" in df.columns:
        df["obra"] = df["obras"].apply(lambda x: x.get("nome") if isinstance(x, dict) else None)
        df.drop(columns=["obras"], inplace=True)

    # Converter datas
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    return df


def inserir_funcionario(data, obra_id, nome, funcao, horas_trabalhadas, custo):
    """Insere funcionário vinculado a uma obra"""
    if hasattr(data, "isoformat"):
        data = data.isoformat()

    def to_native(val):
        if isinstance(val, (np.int64, np.int32)):
            return int(val)
        elif isinstance(val, (np.float64, np.float32)):
            return float(val)
        return val

    obra_id = to_native(obra_id)
    horas_trabalhadas = to_native(horas_trabalhadas)
    custo = to_native(custo)

    supabase.table("funcionarios").insert({
        "data": data,
        "obra_id": obra_id,
        "nome": nome,
        "funcao": funcao,
        "horas_trabalhadas": horas_trabalhadas,
        "custo": custo
    }).execute()

    return listar_funcionarios()
