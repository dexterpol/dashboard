import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from modules.materiais_crud import listar_materiais, inserir_material
from modules.diario_crud import listar_obras  # garantir obras carregadas

def _to_dataframe_safe(obj, columns=None):
    """Converte obj em DataFrame de forma segura."""
    if isinstance(obj, pd.DataFrame):
        return obj
    if obj is None:
        return pd.DataFrame(columns=columns or [])
    if isinstance(obj, (list, dict)):
        return pd.DataFrame(obj)
    # fallback
    return pd.DataFrame(obj, columns=columns or [])

def show_materiais(df=None):
    st.subheader("📦 Materiais Utilizados")

    # ========== Garantir OBRAS no session_state ==========
    if "obras" not in st.session_state or st.session_state["obras"].empty:
        try:
            obras_df = listar_obras()  # precisa trazer ao menos: id, nome
        except Exception:
            obras_df = pd.DataFrame(columns=["id", "nome"])

        obras_df = _to_dataframe_safe(obras_df, columns=["id", "nome"])
        if not obras_df.empty and "obra" not in obras_df.columns and "nome" in obras_df.columns:
            obras_df = obras_df.rename(columns={"nome": "obra"})
        st.session_state["obras"] = obras_df

    if st.session_state["obras"].empty or "obra" not in st.session_state["obras"].columns:
        st.warning("⚠️ Nenhuma obra cadastrada. Cadastre uma antes de inserir materiais.")
        return

    obras_df = st.session_state["obras"].copy()

    # ========== Carregar MATERIAIS (robusto) ==========
    if "materiais_data" not in st.session_state or st.session_state["materiais_data"].empty:
        df_temp = listar_materiais()
        df_temp = _to_dataframe_safe(
            df_temp,
            columns=["data", "obra_id", "material", "quantidade", "unidade", "custo"],
        )
        st.session_state["materiais_data"] = df_temp
    else:
        df_temp = st.session_state["materiais_data"]

    df = df_temp.copy()

    # ========== Formulário recolhível ==========
    st.markdown("### ➕ Adicionar material")
    with st.expander("➕ Clique para adicionar um novo material", expanded=False):
        obra_sel = st.selectbox(
            "Selecione a obra",
            obras_df["obra"],
            key="materiais_select_obra",
        )
        obra_id = obras_df.loc[obras_df["obra"] == obra_sel, "id"].iloc[0]

        data_reg = st.date_input("Data do uso", value=date.today(), key="materiais_data_input")
        material = st.text_input("Nome do material", key="materiais_nome")
        quantidade = st.number_input("Quantidade", min_value=0.0, step=1.0, key="materiais_qtd")
        unidade = st.text_input("Unidade (ex: m², un, kg)", key="materiais_unidade")
        custo = st.number_input("Custo (R$)", min_value=0.0, step=50.0, key="materiais_custo")

        if st.button("Salvar material", key="materiais_btn_salvar"):
            if material.strip():
                try:
                    inserir_material(
                        data_reg.isoformat(),             # evita erro de serialização
                        int(obra_id),
                        material,
                        float(quantidade) if pd.notna(quantidade) else 0.0,
                        unidade,
                        float(custo) if pd.notna(custo) else 0.0,
                    )
                    st.success(f"✅ Material '{material}' adicionado à obra '{obra_sel}'.")
                    # recarregar materiais
                    rec = listar_materiais()
                    st.session_state["materiais_data"] = _to_dataframe_safe(
                        rec,
                        columns=["data", "obra_id", "material", "quantidade", "unidade", "custo"],
                    )
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar material: {e}")
            else:
                st.warning("⚠️ O nome do material é obrigatório.")

    st.divider()

    # ========== Exibir materiais ==========
    df = st.session_state["materiais_data"].copy()

    if df.empty:
        st.info("Ainda não há registros de materiais.")
        return

    # Garantir tipos
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Trazer nome da obra via obra_id, se necessário
    if "obra" not in df.columns:
        obras_slim = obras_df[["id", "obra"]].rename(columns={"id": "obra_id"})
        if "obra_id" in df.columns:
            # garantir tipos comparáveis
            df["obra_id"] = pd.to_numeric(df["obra_id"], errors="coerce")
            obras_slim["obra_id"] = pd.to_numeric(obras_slim["obra_id"], errors="coerce")
            df = df.merge(obras_slim, on="obra_id", how="left")
        else:
            df["obra"] = None

    # Ordenar e formatar data para exibição
    df = df.sort_values(by="data", ascending=False)
    if "data" in df.columns:
        df["Data"] = df["data"].dt.strftime("%d/%m/%Y")

    st.markdown("### 📋 Histórico de Materiais")
    cols_show = [c for c in ["Data", "obra", "material", "quantidade", "unidade", "custo"] if c in df.columns]
    st.dataframe(df[cols_show], use_container_width=True, hide_index=True)

    # ========== Gráficos ==========
    # 1) Custo total por material
    if {"material", "custo"}.issubset(df.columns):
        st.markdown("### 💰 Custo total por material")
        agg_mat = (
            df[["material", "custo"]]
            .dropna()
            .groupby("material", as_index=False)["custo"]
            .sum()
            .sort_values("custo", ascending=False)
        )
        if not agg_mat.empty:
            fig1 = px.bar(
                agg_mat,
                x="material",
                y="custo",
                title="Custo total por material",
                labels={"material": "Material", "custo": "Custo (R$)"},
            )
            st.plotly_chart(fig1, use_container_width=True)

    # 2) Custo total por obra
    if {"obra", "custo"}.issubset(df.columns):
        st.markdown("### 🏗️ Custo total por obra")
        agg_obra = (
            df[["obra", "custo"]]
            .dropna()
            .groupby("obra", as_index=False)["custo"]
            .sum()
            .sort_values("custo", ascending=False)
        )
        if not agg_obra.empty:
            fig2 = px.bar(
                agg_obra,
                x="obra",
                y="custo",
                title="Custo total de materiais por obra",
                labels={"obra": "Obra", "custo": "Custo (R$)"},
            )
            st.plotly_chart(fig2, use_container_width=True)
