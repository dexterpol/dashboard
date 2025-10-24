import streamlit as st
import pandas as pd
from datetime import date
from modules.diario_crud import listar_obras, inserir_obra, listar_diario, inserir_diario

def show_diario():
    st.subheader("📋 Diário de Obras")

    # ========== Carregar obras ==========
    if "obras" not in st.session_state or st.session_state["obras"].empty:
        obras_df = listar_obras()
        if not obras_df.empty:
            obras_df.rename(columns={"nome": "obra"}, inplace=True)
        st.session_state["obras"] = obras_df

    # ========== Carregar registros do diário ==========
    if "diario_data" not in st.session_state or st.session_state["diario_data"].empty:
        diario_df = listar_diario()
        if not diario_df.empty:
            diario_df["data"] = pd.to_datetime(diario_df["data"])
        st.session_state["diario_data"] = diario_df

    col1, col2 = st.columns([2, 3])

    # ========== Adicionar nova obra ==========
    with col1:
        st.markdown("### 🏗️ Adicionar nova obra")

        new_obra = st.text_input("Nome da obra", key="new_obra")
        new_custo = st.number_input("Custo inicial (R$)", min_value=0.0, step=100.0, key="new_custo")
        new_funcionarios = st.number_input("Funcionários iniciais", min_value=1, step=1, key="new_func")
        new_categoria = st.text_input("Categoria principal", key="new_cat")

        if st.button("Adicionar obra", key="btn_add_obra"):
            if new_obra.strip():
                inserir_obra(new_obra, new_custo, new_funcionarios, new_categoria)
                st.success(f"✅ Obra **{new_obra}** adicionada com sucesso!")
                # Atualizar lista de obras
                obras_df = listar_obras()
                if not obras_df.empty:
                    obras_df.rename(columns={"nome": "obra"}, inplace=True)
                st.session_state["obras"] = obras_df
            else:
                st.warning("⚠️ O nome da obra é obrigatório.")

    # ========== Adicionar registro diário ==========
    with col2:
        st.markdown("### 🧱 Adicionar registro diário")

        if st.session_state["obras"].empty:
            st.info("ℹ️ Adicione uma obra antes de registrar o diário.")
        else:
            obra_sel = st.selectbox("Selecione a obra", st.session_state["obras"]["obra"], key="diario_obra")
            data_reg = st.date_input("Data do registro", value=date.today(), key="diario_data_input")
            categoria = st.text_input("Categoria do registro", key="diario_categoria")
            custo = st.number_input("Custo do dia (R$)", min_value=0.0, step=50.0, key="diario_custo")
            progresso = st.slider("Progresso (%)", 0, 100, 0, key="diario_prog")
            obs = st.text_area("Observações", key="diario_obs")

            if st.button("Adicionar registro diário", key="btn_add_diario"):
                obra_id = st.session_state["obras"].loc[
                    st.session_state["obras"]["obra"] == obra_sel, "id"
                ].iloc[0]

                # ⚙️ Corrigido: converte date para string
                inserir_diario(data_reg.isoformat(), obra_id, categoria, custo, progresso, obs)

                st.success(f"✅ Registro do dia **{data_reg.strftime('%d/%m/%Y')}** adicionado para a obra **{obra_sel}**.")

                # Atualiza dados
                diario_df = listar_diario()
                if not diario_df.empty:
                    diario_df["data"] = pd.to_datetime(diario_df["data"])
                st.session_state["diario_data"] = diario_df

    # ========== Histórico de registros ==========
    if not st.session_state["diario_data"].empty:
        st.markdown("---")
        st.markdown("### 📆 Histórico de registros")

        diario_df = st.session_state["diario_data"].copy()
        diario_df = diario_df.sort_values("data", ascending=False)

        # Formata data e exibe colunas relevantes
        diario_df["data"] = diario_df["data"].dt.strftime("%d/%m/%Y")

        st.dataframe(
            diario_df[
                ["data", "obra", "categoria", "custo", "progresso", "observacoes"]
            ].rename(
                columns={
                    "data": "Data",
                    "obra": "Obra",
                    "categoria": "Categoria",
                    "custo": "Custo (R$)",
                    "progresso": "Progresso (%)",
                    "observacoes": "Observações"
                }
            ),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("📭 Nenhum registro diário encontrado.")
