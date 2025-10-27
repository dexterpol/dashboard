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
        if df is None:
            df = pd.DataFrame(columns=["data","obra_id","obra","nome","funcao","horas_trabalhadas","custo"])
        st.session_state["funcionarios_data"] = df
    else:
        df = st.session_state["funcionarios_data"]

    col1, col2 = st.columns([2, 3])

    # =========================================================
    #  ➕ Adicionar novo funcionário (mostra só após clicar)
    # =========================================================
    with col1:
        st.markdown("### ➕ Adicionar funcionário")

        if "show_form_func" not in st.session_state:
            st.session_state["show_form_func"] = False

        if not st.session_state["show_form_func"]:
            if st.button("➕ Novo lançamento", key="btn_abrir_form_func"):
                st.session_state["show_form_func"] = True
        else:
            # Campos só aparecem após clicar no botão acima
            obra_sel = st.selectbox(
                "Selecione a obra",
                st.session_state["obras"]["nome"] if "obra" not in st.session_state["obras"].columns else st.session_state["obras"]["obra"],
                key="select_obra_funcionarios"
            )
            # resolve o nome/obra -> id
            obras_df = st.session_state["obras"].rename(columns={"nome": "obra"}) if "obra" not in st.session_state["obras"].columns else st.session_state["obras"]
            obra_id = obras_df.loc[obras_df["obra"] == obra_sel, "id"].iloc[0]

            data_reg = st.date_input("Data de trabalho", value=date.today(), key="func_data")
            nome = st.text_input("Nome do funcionário", key="func_nome")
            funcao = st.text_input("Função", key="func_funcao")
            horas = st.number_input("Horas trabalhadas", min_value=0.0, step=1.0, key="func_horas")
            custo = st.number_input("Custo diário (R$)", min_value=0.0, step=50.0, key="func_custo")

            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 Salvar", key="btn_salvar_func"):
                    if nome.strip():
                        inserir_funcionario(
                            data_reg.isoformat(),  # evita erro de serialização
                            int(obra_id),
                            nome,
                            funcao,
                            float(horas) if pd.notna(horas) else 0.0,
                            float(custo) if pd.notna(custo) else 0.0
                        )
                        st.success(f"✅ Funcionário '{nome}' adicionado à obra '{obra_sel}'.")
                        st.session_state["funcionarios_data"] = listar_funcionarios() or pd.DataFrame()
                        st.session_state["show_form_func"] = False
                        st.experimental_rerun()
                    else:
                        st.warning("⚠️ O nome do funcionário é obrigatório.")
            with col_cancel:
                if st.button("✖️ Cancelar", key="btn_cancelar_func"):
                    st.session_state["show_form_func"] = False
                    st.experimental_rerun()

    # =========================================================
    #  📋 Exibir funcionários
    # =========================================================
    with col2:
        df = st.session_state["funcionarios_data"].copy()

        if df.empty:
            st.info("Ainda não há registros de funcionários.")
            return

        # garantir data
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce")

        # se não houver coluna 'obra', tenta derivar via obra_id + session_state["obras"]
        if "obra" not in df.columns and "obra_id" in df.columns:
            obras_df = st.session_state["obras"].rename(columns={"nome": "obra"}) if "obra" not in st.session_state["obras"].columns else st.session_state["obras"]
            obras_slim = obras_df[["id", "obra"]].rename(columns={"id": "obra_id"})
            df = df.merge(obras_slim, on="obra_id", how="left")

        # formatar data para exibir
        if "data" in df.columns:
            df["data_fmt"] = df["data"].dt.strftime("%d/%m/%Y")

        st.markdown("### 📋 Histórico de Funcionários")
        cols_show = [c for c in ["data_fmt", "obra", "nome", "funcao", "horas_trabalhadas", "custo"] if c in df.columns]
        st.dataframe(
            df[cols_show].rename(columns={"data_fmt": "Data"}),
            use_container_width=True,
            hide_index=True
        )

        # Gráfico: custo total por obra
        if {"obra", "custo"}.issubset(df.columns):
            st.markdown("### 💰 Custo total por obra (funcionários)")
            agg = (
                df[["obra", "custo"]]
                .dropna()
                .groupby("obra", as_index=False)["custo"]
                .sum()
                .sort_values("custo", ascending=False)
            )
            if not agg.empty:
                fig = px.bar(
                    agg,
                    x="obra",
                    y="custo",
                    title="Custo total por obra (funcionários)",
                    labels={"obra": "Obra", "custo": "Custo (R$)"}
                )
                st.plotly_chart(fig, use_container_width=True)
