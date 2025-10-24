import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from modules.notas_crud import listar_notas, inserir_nota

def show_notas(df=None):
    st.subheader("🗒️ Notas da Obra")

    # ========== Verificar obras ==========
    if "obras" not in st.session_state or st.session_state["obras"].empty:
        st.warning("⚠️ Nenhuma obra cadastrada. Cadastre uma antes de inserir notas.")
        return

    # ========== Carregar notas ==========
    if "notas_data" not in st.session_state or st.session_state["notas_data"].empty:
        df = listar_notas()
        st.session_state["notas_data"] = df
    else:
        df = st.session_state["notas_data"]

    col1, col2 = st.columns([2, 3])

    # ========== Adicionar nova nota ==========
    with col1:
        st.markdown("### ➕ Adicionar nota")

        obra_sel = st.selectbox(
            "Selecione a obra",
            st.session_state["obras"]["obra"],
            key="select_obra_notas"
        )

        obra_id = st.session_state["obras"].loc[
            st.session_state["obras"]["obra"] == obra_sel, "id"
        ].iloc[0]

        data_reg = st.date_input("Data da nota", value=date.today(), key="nota_data")
        titulo = st.text_input("Título da nota", key="nota_titulo")
        descricao = st.text_area("Descrição detalhada", key="nota_desc")
        custo = st.number_input("Custo associado (R$)", min_value=0.0, step=50.0, key="nota_custo")

        if st.button("Salvar nota", key="btn_salvar_nota"):
            if titulo.strip():
                inserir_nota(data_reg, obra_id, titulo, descricao, custo)
                st.success(f"✅ Nota '{titulo}' adicionada à obra '{obra_sel}'.")
                st.session_state["notas_data"] = listar_notas()
            else:
                st.warning("⚠️ O título da nota é obrigatório.")

    # ========== Exibir notas ==========
    with col2:
        df = st.session_state["notas_data"]

        if df.empty:
            st.info("Ainda não há notas registradas.")
            return

        # Formatar data
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.strftime("%d/%m/%Y")

        st.markdown("### 📋 Histórico de Notas")
        st.dataframe(
            df[["data", "obra", "titulo", "descricao", "custo"]],
            use_container_width=True,
            hide_index=True
        )

        # Gráfico de custos por obra
        if "obra" in df.columns and "custo" in df.columns:
            st.markdown("### 💰 Custo total por obra (notas)")
            agg = df.groupby("obra")["custo"].sum().reset_index()
            fig = px.bar(
                agg,
                x="obra",
                y="custo",
                title="Custo total de notas por obra",
                labels={"obra": "Obra", "custo": "Custo (R$)"}
            )
            st.plotly_chart(fig, use_container_width=True)
