import pandas as pd
import streamlit as st
from datetime import date

def adicionar_nota(obra, observacoes, data_reg=None):
    """Adiciona uma nova nota ao session_state"""
    if data_reg is None:
        data_reg = date.today()
    
    novo_registro = {
        "data": pd.to_datetime(data_reg),
        "obra": obra,
        "observacoes": observacoes
    }

    if "notas_data" not in st.session_state:
        st.session_state["notas_data"] = pd.DataFrame(columns=["data","obra","observacoes"])

    st.session_state["notas_data"] = pd.concat([
        st.session_state["notas_data"],
        pd.DataFrame([novo_registro])
    ], ignore_index=True)
    st.success("Nota adicionada com sucesso!")

def deletar_nota(index):
    """Remove nota pelo índice"""
    if "notas_data" in st.session_state and not st.session_state["notas_data"].empty:
        st.session_state["notas_data"] = st.session_state["notas_data"].drop(index).reset_index(drop=True)
        st.success("Nota removida com sucesso!")

def atualizar_nota(index, observacoes):
    """Atualiza a observação de uma nota existente"""
    if "notas_data" in st.session_state and not st.session_state["notas_data"].empty:
        st.session_state["notas_data"].at[index, "observacoes"] = observacoes
        st.success("Nota atualizada com sucesso!")
