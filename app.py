import streamlit as st
import pandas as pd

from filters import filter_data
from kpis import show_kpis
from diario import show_diario
from materiais import show_materiais
from funcionarios import show_funcionarios
from notas import show_notas
from exports import export_data

# ---------- Configurações ----------
st.set_page_config(layout="wide", page_title="Dashboard de Obras", page_icon="🏗️")

# ---------- Inicializar session_state ----------
if "obras" not in st.session_state:
    st.session_state["obras"] = pd.DataFrame(columns=["obra", "custo_inicial", "funcionarios_iniciais", "categoria"])

if "diario_data" not in st.session_state:
    st.session_state["diario_data"] = pd.DataFrame(columns=["data","obra","categoria","custo","progresso","observacoes"])

if "materiais_data" not in st.session_state:
    st.session_state["materiais_data"] = pd.DataFrame(columns=["data","obra","material","custo"])

if "funcionarios_data" not in st.session_state:
    st.session_state["funcionarios_data"] = pd.DataFrame(columns=["data","obra","funcionario","presente"])

if "notas_data" not in st.session_state:
    st.session_state["notas_data"] = pd.DataFrame(columns=["data","obra","observacoes"])

# ---------- Sidebar Filtros ----------
with st.sidebar.expander("Filtros de Obras"):
    date_filter = st.date_input("Intervalo de datas", [], key="sidebar_date_input")
    obra_filter = st.multiselect(
        "Selecione a obra",
        st.session_state["obras"]["obra"].unique() if not st.session_state["obras"].empty else [],
        key="sidebar_obra"
    )
    categoria_filter = st.multiselect(
        "Categoria",
        st.session_state["diario_data"]["categoria"].unique() if not st.session_state["diario_data"].empty else [],
        key="sidebar_categoria"
    )

# ---------- Aplicar filtros ----------
df_filtrado = filter_data(
    st.session_state["diario_data"],
    date_filter=date_filter,
    obra_filter=obra_filter,
    categoria_filter=categoria_filter
)

# ---------- KPIs ----------
show_kpis(df_filtrado, st.session_state["funcionarios_data"])
st.markdown("---")

# ---------- Abas ----------
tab_diario, tab_materiais, tab_funcionarios, tab_notas = st.tabs([
    "📋 Diário de Obras",
    "📦 Materiais",
    "👷 Funcionários",
    "📝 Notas"
])

with tab_diario:
    show_diario()

with tab_materiais:
    show_materiais(st.session_state["materiais_data"])

with tab_funcionarios:
    show_funcionarios(st.session_state["funcionarios_data"])

with tab_notas:
    show_notas(st.session_state["notas_data"])

# ---------- Exportação ----------
export_data(df_filtrado)
