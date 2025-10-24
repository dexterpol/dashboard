import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from modules.funcionarios_crud import listar_funcionarios, inserir_funcionario

def show_funcionarios(df=None):
    st.subheader("👷‍♂️ Funcionários da Obra")

    # ========== Verificar se há obras ==========
    if "obras" not in st.session_state or st.session_state["obras"].empty:
        st.warning("⚠️ Nenhuma obra cadastrada. Cadastre uma antes de inserir funcionários.")
        return

    # ========== Carregar funcionários ==========
    if "funcionarios_data" not in st.session_state or st.session_state["funcionarios_data"].empty:
        df = listar_funcionarios()
        st.session_state["funcionarios_data"] = df
    else:
        df = st.session_state["funcionarios_data"]

    col1, col2 = st.columns([2, 3])

    # ========== Adicionar novo funcionário ==========
    with col1:
        st.markdown("### ➕ Adicionar funcionário")

        obra_sel = st.selectbox(
            "Selecione a obra",
            st.session_state["obras"]["obra"],
            key="select_obra_funcionarios"
        )

        obra_id = st.session_state["obras"].loc[
            st.session_state["obras"]["obra"] == obra_sel, "id"
        ].iloc[0]

        data_reg = st.date_input(
            "Data de trabalho",
            value=date.today(),
            key="func_data"
        )

        nome = st.text_input("Nome do funcionário", key="func_nome")
        funcao = st.text_input("Função", key="func_funcao")
        horas = st.number_input("Horas trabalhadas", min_value=0.0, step=1.0, key="func_horas")
        custo = st.number_input("Custo diário (R$)", min_value=0.0, step=50.0, key="func_custo")

        if st.button("Salvar funcionário", key="btn_salvar_func"):
            if nome.strip():
                inserir_funcionario(data_reg, obra_id, nome, funcao, horas, custo)
                st.success(f"✅ Funcionário '{nome}' adicionado à obra '{obra_sel}'.")
                st.session_state["funcionarios_data"] = listar_funcionarios()
            else:
                st.warning("⚠️ O nome do funcionário é obrigatório.")

    # ========== Exibir funcionários ==========
    with col2:
        df = st.session_state["funcionarios_data"]

        if df.empty:
            st.info("Ainda não há registros de funcionários.")
            return

        # Formatar data
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.strftime("%d/%m/%Y")

        st.markdown("### 📋 Histórico de Funcionários")
        st.dataframe(
            df[["data", "obra", "nome", "funcao", "horas_trabalhadas", "custo"]],
            use_container_width=True,
            hide_index=True
        )

        # Gráfico de custo por obra
        if "obra" in df.columns and "custo" in df.columns:
            st.markdown("### 💰 Custo total por obra")
            agg = df.groupby("obra")["custo"].sum().reset_index()
            fig = px.bar(
                agg,
                x="obra",
                y="custo",
                title="Custo total por obra (funcionários)",
                labels={"obra": "Obra", "custo": "Custo (R$)"}
            )
            st.plotly_chart(fig, use_container_width=True)
