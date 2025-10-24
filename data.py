import pandas as pd
import numpy as np

def load_sample_data(n=100):
    rng = pd.date_range(end=pd.Timestamp.today(), periods=n, freq='D')
    df_obras = pd.DataFrame({
        "data": np.random.choice(rng, size=n),
        "obra": np.random.choice(["Obra A","Obra B","Obra C"], size=n),
        "categoria": np.random.choice(["Pintura","Alvenaria","Elétrica"], size=n),
        "custo": np.round(np.random.gamma(2, 1000, size=n),2),
        "progresso": np.random.randint(0, 101, size=n),
        "funcionarios": np.random.randint(1, 10, size=n),
        "lat": -10 + np.random.rand(n)*20,
        "lon": -60 + np.random.rand(n)*20,
        "observacoes": np.random.choice(["Tudo certo","Atraso","Falta de material"], size=n)
    })
    
    df_materiais = pd.DataFrame({
        "data": np.random.choice(rng, size=n),
        "obra": np.random.choice(["Obra A","Obra B","Obra C"], size=n),
        "material": np.random.choice(["Cimento","Areia","Tinta","Tijolo"], size=n),
        "quantidade": np.random.randint(1, 50, size=n),
        "custo": np.round(np.random.rand(n)*500,2)
    })
    
    df_funcionarios = pd.DataFrame({
        "data": np.random.choice(rng, size=n),
        "obra": np.random.choice(["Obra A","Obra B","Obra C"], size=n),
        "funcionario": np.random.choice(["João","Maria","Carlos","Ana"], size=n),
        "presente": np.random.choice([True, False], size=n),
        "funcao": np.random.choice(["Pedreiro","Encarregado","Eletricista"], size=n)
    })
    
    return df_obras, df_materiais, df_funcionarios
