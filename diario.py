import streamlit as st
import pandas as pd
from datetime import date
from modules.diario_crud import listar_obras, inserir_obra, listar_diario, inserir_diario

def show_diario():
    st.subheader("📋 Diário de Obras")

    # ---------- Carregar obras do Supabase ----------
    if "obras" not in st.session_state or st.session_state["obras"].empty:
        obras_df = listar_obras()  # Supabase retorna coluna 'nome'
        if not obras_df.empty:
            obras_df.rename(columns={"nome": "obra"}, inplace=True)  # renomeia para compatibilidade
        st.session_state["obras"] = obras_df

    # ---------- Carregar registros do diário ----------
    if "diario_data" not in st.session_state or st.session_state["diario_data"].empty:
        diario_df = listar_diario()
        if not diario_df.empty:
            diario_df["data"] = pd.to_datetime(diario_df["data"])  # garante datetime
        st.session_state["diario_data"] = diario_df

    col1, col2 = st.columns([2, 3])

    # ---------- Adicionar nova obra ----------
    with col1:
        st.markdown("### ➕ Adicionar nova obra")
        new_obra = st.text_input("Nome da obra", key="new_obra")
        new_custo = st.number_input("Custo inicial (R$)", min_value=0.0, step=100.0, key="new_custo")
        new_funcionarios = st.number_input("Funcionários iniciais", min_value=1, step=1, key="new_func")
        new_categoria = st.text_input("Categoria principal", key="new_cat")

        if st.button("Adicionar obra"):
            if new_obra:
                # Insere no Supabase
                inserir_obra(new_obra, new_custo, new_funcionarios, new_categoria)
                st.success(f"Obra '{new_obra}' adicionada com sucesso!")
                # Atualiza session_state
                obras_df = listar_obras()
                if not obras_df.empty:
                    obras_df.rename(columns={"nome": "obra"}, inplace=True)
                st.session_state["obras"] = obras_df

    # ---------- Adicionar registro diário ----------
    with col2:
        st.markdown("### ➕ Adicionar registro diário")

        if st.session_state["obras"].empty:
            st.info("Adicione uma obra primeiro.")
        else:
            # Selecionar obra existente
            obra_sel = st.selectbox("Selecione a obra", st.session_state["obras"]["obra"], key="diario_obra")
            data_reg = st.date_input("Data do registro", value=date.today(), key="diario_data_input")
            categoria = st.text_input("Categoria do registro", key="diario_categoria")
            custo = st.number_input("Custo do dia (R$)", min_value=0.0, step=50.0, key="diario_custo")
            progresso = st.slider("Progresso (%)", 0, 100, key="diario_prog")
            obs = st.text_area("Observações", key="diario_obs")

            if st.button("Adicionar registro diário"):
                # Busca ID da obra selecionada
                obra_id = st.session_state["obras"].loc[
                    st.session_state["obras"]["obra"] == obra_sel, "id"
                ].iloc[0]

                inserir_diario(data_reg, obra_id, categoria, custo, progresso, obs)
                st.success(f"Registro da obra '{obra_sel}' adicionado!")
                # Atualiza registros
                diario_df = listar_diario()
                if not diario_df.empty:
                    diario_df["data"] = pd.to_datetime(diario_df["data"])
                st.session_state["diario_data"] = diario_df

    # ---------- Histórico ----------
    if not st.session_state["diario_data"].empty:
        st.markdown("### Histórico de registros")
        st.dataframe(st.session_state["diario_data"].sort_values("data", ascending=False))
