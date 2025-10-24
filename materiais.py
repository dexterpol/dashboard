import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from modules.materiais_crud import listar_materiais, inserir_material

def show_materiais(df=None):
    st.subheader("📦 Materiais Utilizados")

    # ========== Verificar se há obras cadastradas ==========
    if "obras" not in st.session_state or st.session_state["obras"].empty:
        st.warning("⚠️ Nenhuma obra cadastrada. Cadastre uma antes de inserir materiais.")
        return

    # ========== Carregar materiais ==========
    if "materiais_data" not in st.session_state or st.session_state["materiais_data"].empty:
        df = listar_materiais()
        st.session_state["materiais_data"] = df
    else:
        df = st.session_state["materiais_data"]

    col1, col2 = st.columns([2, 3])

    # ========== Adicionar novo material ==========
    with col1:
        st.markdown("### ➕ Adicionar material")

        obra_sel = st.selectbox("Selecione a obra", st.session_state["obras"]["obra"])
        obra_id = st.session_state["obras"].loc[
            st.session_state["obras"]["obra"] == obra_sel, "id"
        ].iloc[0]

        data_reg = st.date_input("Data do uso", value=date.today())
        material = st.text_input("Nome do material")
        quantidade = st.number_input("Quantidade", min_value=0.0, step=1.0)
        unidade = st.text_input("Unidade (ex: m², un, kg)")
        custo = st.number_input("Custo (R$)", min_value=0.0, step=50.0)

        if st.button("Salvar material"):
            if material.strip():
                inserir_material(data_reg, obra_id, material, quantidade, unidade, custo)
                st.success(f"✅ Material '{material}' adicionado à obra '{obra_sel}'.")
                st.session_state["materiais_data"] = listar_materiais()
            else:
                st.warning("⚠️ O nome do material é obrigatório.")

    # ========== Exibir materiais ==========
    with col2:
        df = st.session_state["materiais_data"]

        if df.empty:
            st.info("Ainda não há registros de materiais.")
            return

        # Formatar data
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.strftime("%d/%m/%Y")

        # Exibir tabela formatada
        st.markdown("### 📋 Histórico de Materiais")
        st.dataframe(
            df[["data", "obra", "material", "quantidade", "unidade", "custo"]],
            use_container_width=True,
            hide_index=True
        )

        # Gráfico de custo por material
        if "material" in df.columns and "custo" in df.columns:
            st.markdown("### 💰 Custo total por material")
            agg = df.groupby("material")["custo"].sum().reset_index()
            fig = px.bar(
                agg,
                x="material",
                y="custo",
                title="Custo total por material",
                labels={"material": "Material", "custo": "Custo (R$)"}
            )
            st.plotly_chart(fig, use_container_width=True)
