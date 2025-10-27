import streamlit as st
import pandas as pd
from datetime import date
from modules.diario_crud import listar_diario, inserir_diario, listar_obras
from modules.funcionarios_crud import listar_funcionarios
from modules.materiais_crud import listar_materiais
from modules.notas_crud import listar_notas


def show_diario():
    st.subheader("📋 Diário de Obras")

    # ========== 1) CARREGAR OBRAS ==========
    obras_df = listar_obras()  # precisa retornar pelo menos: id, nome
    if obras_df.empty:
        st.warning("⚠️ Nenhuma obra cadastrada. Cadastre uma antes de registrar o diário.")
        return

    # Garantir colunas e tipos
    # - id deve ser inteiro
    if "id" not in obras_df.columns or "nome" not in obras_df.columns:
        st.error("A tabela de obras precisa ter as colunas 'id' e 'nome'.")
        return

    obras_df = obras_df.copy()
    obras_df["id"] = pd.to_numeric(obras_df["id"], errors="coerce").astype("Int64")

    # Versão slim para merge (evita colisão de colunas 'id')
    obras_slim = obras_df[["id", "nome"]].rename(columns={"id": "obra_id", "nome": "obra_nome"})

    # ========== 2) FORMULÁRIO (RECOLHÍVEL) PARA NOVO REGISTRO ==========
    st.markdown("### ➕ Adicionar novo registro diário")
    with st.expander("➕ Clique para adicionar um novo registro", expanded=False):
        # Selectbox com nomes (mostra nomes, mas guardamos o id correspondente)
        obra_sel = st.selectbox("Selecione a obra", obras_df["nome"], key="diario_obra_sel")
        obra_id = obras_df.loc[obras_df["nome"] == obra_sel, "id"].iloc[0]

        data_reg = st.date_input("Data do registro", value=date.today(), key="diario_data_input")
        categoria = st.text_input("Categoria", key="diario_categoria")
        custo = st.number_input("Custo do dia (R$)", min_value=0.0, step=50.0, key="diario_custo")
        progresso = st.slider("Progresso (%)", 0, 100, 0, key="diario_prog")
        obs = st.text_area("Observações", key="diario_obs")

        if st.button("💾 Salvar registro diário", key="btn_add_diario"):
            inserir_diario(data_reg.isoformat(), int(obra_id), categoria, float(custo), int(progresso), obs)
            st.success(f"✅ Registro do dia {data_reg.strftime('%d/%m/%Y')} adicionado à obra '{obra_sel}'.")
            st.experimental_rerun()

    st.divider()

    # ========== 3) CARREGAR DIÁRIO E UNIR PELO obra_id ==========
    diario_df = listar_diario()  # precisa retornar ao menos: obra_id, data, categoria, custo, progresso, observacoes
    if diario_df.empty:
        st.info("Nenhum registro diário encontrado.")
        return

    diario_df = diario_df.copy()

    # Garantir que 'obra_id' exista e seja inteiro
    if "obra_id" not in diario_df.columns:
        st.error("Os registros do diário precisam ter a coluna 'obra_id'.")
        return

    diario_df["obra_id"] = pd.to_numeric(diario_df["obra_id"], errors="coerce").astype("Int64")

    # Datas como datetime
    if "data" in diario_df.columns:
        diario_df["data"] = pd.to_datetime(diario_df["data"], errors="coerce")
    else:
        st.error("Os registros do diário precisam ter a coluna 'data'.")
        return

    # Merge: diário (obra_id) x obras_slim (obra_id → obra_nome)
    diario_df = diario_df.merge(obras_slim, on="obra_id", how="left")

    # Ordenar
    diario_df = diario_df.sort_values("data", ascending=False)

    # ========== 4) HISTÓRICO ==========
    st.markdown("### 📅 Histórico de registros")
    for _, row in diario_df.iterrows():
        data_fmt = row["data"].strftime("%d/%m/%Y") if pd.notna(row["data"]) else "Data inválida"
        obra_nome = row.get("obra_nome") if pd.notna(row.get("obra_nome")) else "Obra não encontrada"

        with st.expander(f"📆 {data_fmt} — 🏗️ {obra_nome}"):
            st.write(f"**Categoria:** {row.get('categoria', '-')}")
            st.write(f"**Progresso:** {int(row.get('progresso', 0))}%")
            try:
                custo_val = float(row.get('custo', 0))
            except Exception:
                custo_val = 0.0
            st.write(f"**Custo do dia:** R$ {custo_val:,.2f}")
            st.write(f"**Observações:** {row.get('observacoes', '—')}")

            # ---------- Funcionários ----------
            st.markdown("#### 👷 Funcionários presentes")
            funcs = listar_funcionarios()
            if not funcs.empty and {"obra_id", "data"}.issubset(funcs.columns):
                funcs = funcs.copy()
                funcs["obra_id"] = pd.to_numeric(funcs["obra_id"], errors="coerce").astype("Int64")
                funcs["data"] = pd.to_datetime(funcs["data"], errors="coerce")
                funcs_dia = funcs[(funcs["obra_id"] == row["obra_id"]) &
                                  (funcs["data"].dt.date == row["data"].date())]
                if not funcs_dia.empty:
                    cols_show = [c for c in ["nome", "funcao", "horas_trabalhadas", "custo"] if c in funcs_dia.columns]
                    st.dataframe(funcs_dia[cols_show], use_container_width=True, hide_index=True)
                else:
                    st.write("_Nenhum funcionário registrado nesse dia._")
            else:
                st.write("_Nenhum funcionário registrado nesse dia._")

            # ---------- Materiais ----------
            st.markdown("#### 📦 Materiais utilizados")
            mats = listar_materiais()
            if not mats.empty and {"obra_id", "data"}.issubset(mats.columns):
                mats = mats.copy()
                mats["obra_id"] = pd.to_numeric(mats["obra_id"], errors="coerce").astype("Int64")
                mats["data"] = pd.to_datetime(mats["data"], errors="coerce")
                mats_dia = mats[(mats["obra_id"] == row["obra_id"]) &
                                (mats["data"].dt.date == row["data"].date())]
                if not mats_dia.empty:
                    cols_show = [c for c in ["material", "quantidade", "unidade", "custo"] if c in mats_dia.columns]
                    st.dataframe(mats_dia[cols_show], use_container_width=True, hide_index=True)
                else:
                    st.write("_Nenhum material lançado nesse dia._")
            else:
                st.write("_Nenhum material lançado nesse dia._")

            # ---------- Notas ----------
            st.markdown("#### 🗒️ Notas do dia")
            notas = listar_notas()
            if not notas.empty and {"obra_id", "data"}.issubset(notas.columns):
                notas = notas.copy()
                notas["obra_id"] = pd.to_numeric(notas["obra_id"], errors="coerce").astype("Int64")
                notas["data"] = pd.to_datetime(notas["data"], errors="coerce")
                notas_dia = notas[(notas["obra_id"] == row["obra_id"]) &
                                  (notas["data"].dt.date == row["data"].date())]
                if not notas_dia.empty:
                    for _, n in notas_dia.iterrows():
                        try:
                            custo_n = float(n.get("custo", 0))
                        except Exception:
                            custo_n = 0.0
                        st.markdown(f"**{n.get('titulo','(sem título)')}** — R$ {custo_n:,.2f}")
                        st.write(n.get("descricao", "—"))
                        st.markdown("---")
                else:
                    st.write("_Nenhuma nota registrada nesse dia._")
            else:
                st.write("_Nenhuma nota registrada nesse dia._")
